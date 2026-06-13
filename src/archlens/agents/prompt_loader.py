"""Load and render the 7 versioned agent prompt templates (task 10.045)."""

import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
AGENTS = ("repo", "graph", "analyst", "bughunter", "refactor", "qa", "metrics")


def load_prompt(name: str) -> str:
    """Return the raw template text for an agent."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def declared_variables(name: str) -> list[str]:
    """Parse the declared `Variables:` header line into a list of placeholder names."""
    match = re.search(r"^Variables:\s*(.*)$", load_prompt(name), re.MULTILINE)
    if not match or not match.group(1).strip():
        return []
    return [variable.strip() for variable in match.group(1).split(",")]


def render_prompt(name: str, **values) -> str:
    """Render a template by substituting all declared variables."""
    return load_prompt(name).format(**values)
