"""Scan tracked files for forbidden tooling commands, allowlisting prohibition contexts (16.004).

Flags actual usages of pip / virtualenv / `python -m` / requirements.txt across code, docs, and CI.
Lines that quote the guideline prohibition (forbidden, prohibited, must not, compliance) are
allowlisted, and the scanner's own files plus MATERIALS/ and .venv/ are skipped.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(r"\bpip install\b|\bpip3 \b|\bpython -m \b|\bvirtualenv\b|requirements\.txt")
_ALLOW = re.compile(
    r"forbid|prohibit|compliance|never use|not allowed|must not|zero occurrences|"
    r"uv[\s-]?only|single (?:dependency )?source|\bno (?:pip|requirements|virtualenv|venv)",
    re.IGNORECASE)
_SKIP_PREFIXES = ("MATERIALS/", ".venv/")
_SKIP_FILES = {"uv.lock", "scripts/check_forbidden_tools.py", "tests/test_check_forbidden_tools.py"}


def is_violation(line: str) -> bool:
    """True when a line uses forbidden tooling and is not an allowlisted prohibition statement."""
    return bool(FORBIDDEN.search(line)) and not _ALLOW.search(line)


def _tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


def scan(files: list[str] | None = None) -> list[str]:
    """Return `path:line: text` hits for forbidden tooling usage (allowlisted lines skipped)."""
    hits = []
    for rel in (files if files is not None else _tracked_files()):
        if rel.startswith(_SKIP_PREFIXES) or rel in _SKIP_FILES:
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_violation(line):
                hits.append(f"{rel}:{lineno}: {line.strip()}")
    return hits


def main() -> int:
    hits = scan()
    for hit in hits:
        print(hit)
    print(f"forbidden-tooling hits: {len(hits)}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
