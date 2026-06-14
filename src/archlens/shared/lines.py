"""Effective-line counting (non-blank, non-comment) — the project's 150-line metric."""


def effective_lines(text: str) -> int:
    """Count non-blank lines that are not pure comments (matches scripts/check_line_cap.py)."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count
