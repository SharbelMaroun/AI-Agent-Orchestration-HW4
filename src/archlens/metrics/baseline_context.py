"""Naive baseline context builder — the no-Graphify control (task 12.018).

Concatenates every .py source in the target repo into one prompt context, in deterministic
(sorted) order. This is the expensive baseline the Graphify-assisted protocol is measured against.
"""

from pathlib import Path


def collect_python_sources(repo_path: str | Path) -> list[Path]:
    """Every .py file under repo_path, in deterministic sorted order."""
    return sorted(Path(repo_path).rglob("*.py"))


def build_baseline_context(repo_path: str | Path) -> str:
    """Concatenate every .py file (with a path header) into one full-context string."""
    root = Path(repo_path)
    parts = []
    for path in collect_python_sources(root):
        body = path.read_text(encoding="utf-8", errors="replace")
        parts.append(f"# FILE: {path.relative_to(root)}\n{body}")
    return "\n\n".join(parts)


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars/token) for budgeting without an API round-trip."""
    return len(text) // 4 if text else 0
