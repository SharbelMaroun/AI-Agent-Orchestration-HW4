"""One-idea-per-note linter: at most one H1 per generated note (tasks 5.012-5.013)."""


class NoteLintError(ValueError):
    """A note violates the one-idea-per-note rule (more than one H1)."""


def check_one_idea(markdown: str) -> None:
    """Raise NoteLintError when a note declares more than one top-level (H1) heading."""
    h1 = [line for line in markdown.splitlines() if line.startswith("# ")]
    if len(h1) > 1:
        raise NoteLintError(f"note has {len(h1)} H1 headings; exactly one is allowed")
