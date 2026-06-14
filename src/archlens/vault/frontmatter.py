"""YAML frontmatter renderer for vault notes (tasks 5.008-5.009)."""

from ..shared.constants import FRONTMATTER_KEYS


def render_frontmatter(type_: str, status: str, project: str) -> str:
    """Render a --- delimited YAML block with the mandatory type/status/project keys."""
    values = dict(zip(FRONTMATTER_KEYS, (type_, status, project), strict=True))
    body = "\n".join(f"{key}: {values[key]}" for key in FRONTMATTER_KEYS)
    return f"---\n{body}\n---\n"
