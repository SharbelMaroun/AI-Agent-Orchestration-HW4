"""Skill router: match prompts to skills by trigger phrase (task 14.019).

A prompt routes to the single auto-invocable skill whose declared trigger phrase it contains.
Zero or multiple matches return None (ambiguous); disable-model-invocation skills never auto-return.
"""

from dataclasses import dataclass
from pathlib import Path

from .skill_schema import parse_frontmatter


@dataclass(frozen=True)
class Skill:
    """A routable skill: its name, lowercased trigger phrases, and auto-invocability."""

    name: str
    triggers: tuple[str, ...]
    auto_invocable: bool


def load_skill(path) -> Skill:
    """Load a Skill from a SKILL.md file (triggers from frontmatter; human-only if disabled)."""
    fields = parse_frontmatter(Path(path).read_text(encoding="utf-8"))
    triggers = tuple(str(trigger).lower() for trigger in (fields.get("triggers") or []))
    auto = fields.get("disable-model-invocation") is not True
    return Skill(str(fields.get("name", "")), triggers, auto)


def load_skills(skills_dir) -> list[Skill]:
    """Load every SKILL_*.md in a directory, sorted by filename."""
    return [load_skill(path) for path in sorted(Path(skills_dir).glob("SKILL_*.md"))]


def route(prompt: str, skills: list[Skill]) -> str | None:
    """Return the single matching auto-invocable skill name, else None (ambiguous/no match)."""
    low = prompt.lower()
    matched = [skill for skill in skills
               if skill.auto_invocable and any(trigger in low for trigger in skill.triggers)]
    return matched[0].name if len(matched) == 1 else None
