"""Read a bounded source excerpt from the cloned repo so agents can give the LLM the real code.

Bounded by ``max_chars`` to keep token cost (and latency) predictable on large modules; the excerpt
is what turns the LLM step from graph-summary interpretation into genuine code-level reverse
engineering. Missing/unreadable files degrade to an empty string (the agent still runs).
"""

from pathlib import Path

_MAX_CHARS = 6000  # ~1.5k tokens — enough context for a module, bounded for cost


def read_source_excerpt(repo_path: str, source_file: str, max_chars: int = _MAX_CHARS) -> str:
    """Return up to ``max_chars`` of the file at ``<repo_path>/<source_file>`` (or '' if unavailable)."""
    if not repo_path or not source_file:
        return ""
    path = Path(repo_path) / source_file
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n# ... (truncated)\n"
