"""Enforce the 150 effective-line cap per code file (blank and comment lines excluded)."""

import sys
from pathlib import Path

LINE_CAP = 150  # mirrors archlens.shared.constants.LINE_CAP; standalone so the hook needs no install
DEFAULT_ROOTS = ("src", "tests")


def effective_lines(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def scan(roots: list[Path] | tuple[Path, ...]) -> list[tuple[Path, int]]:
    over = []
    for root in roots:
        for py_file in sorted(Path(root).rglob("*.py")):
            if "fixtures" in py_file.parts:  # test data (e.g. planted oversized modules) is exempt
                continue
            n = effective_lines(py_file.read_text(encoding="utf-8"))
            if n > LINE_CAP:
                over.append((py_file, n))
    return over


def main(argv: list[str] | None = None) -> int:
    roots = [Path(a) for a in (argv or DEFAULT_ROOTS)]
    offenders = scan([r for r in roots if r.exists()])
    for path, n in offenders:
        print(f"{path}: {n} effective lines exceeds the cap of {LINE_CAP}")
    if offenders:
        return 1
    print(f"line cap OK: all files within {LINE_CAP} effective lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
