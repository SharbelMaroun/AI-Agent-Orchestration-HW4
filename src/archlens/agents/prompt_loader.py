"""Load and render the 7 versioned agent prompt templates (task 10.045)."""

import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
AGENTS = ("repo", "graph", "analyst", "bughunter", "refactor", "qa", "metrics")


def load_prompt(name: str) -> str:
    """Return the raw template text for an agent."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def _header(name: str, key: str) -> str:
    """Parse a single-line ``Key: value`` header from the prompt file."""
    match = re.search(rf"^{key}:[ \t]*(.*)$", load_prompt(name), re.MULTILINE)
    return match.group(1).strip() if match else ""


def prompt_id(name: str) -> str:
    """The PROMPT_BOOK id of an agent prompt (e.g. ``PB-analyst-01``)."""
    return _header(name, "Id")


def version_of(name: str) -> str:
    """The version string of an agent prompt (e.g. ``1.00``)."""
    return _header(name, "Version")


def system_prompt(name: str) -> str:
    """The agent's system-role prompt: the ``System:`` section up to the ``Task:`` section.

    Agents load this by id+version instead of inlining a string literal (PRD §9 / FR-AO-13).
    """
    after = load_prompt(name).split("System:", 1)
    body = after[1] if len(after) > 1 else after[0]
    return body.split("\nTask:", 1)[0].strip()


def declared_variables(name: str) -> list[str]:
    """Parse the declared `Variables:` header line into a list of placeholder names."""
    match = re.search(r"^Variables:\s*(.*)$", load_prompt(name), re.MULTILINE)
    if not match or not match.group(1).strip():
        return []
    return [variable.strip() for variable in match.group(1).split(",")]


def render_prompt(name: str, **values) -> str:
    """Render a template by substituting all declared variables."""
    return load_prompt(name).format(**values)
