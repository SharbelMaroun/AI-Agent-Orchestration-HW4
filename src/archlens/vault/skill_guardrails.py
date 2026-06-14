"""Guardrail classification for SKILL.md files (task 14.008).

Maps declared tools and step markers to exactly one guardrail level:
  human_only   -- disable-model-invocation set (never auto-invocable)
  irreversible -- declares an [irreversible] step (each must carry an APPROVAL REQUIRED marker)
  reversible   -- declares an [reversible] step or a write tool (each reversible step needs undo:)
  auto         -- read-only tools only
"""

from pathlib import Path

from .skill_schema import parse_frontmatter

WRITE_TOOLS = {"Write", "Edit", "Bash", "Apply"}
_APPROVAL_MARKER = "APPROVAL REQUIRED"


def _tagged_steps(text: str, tag: str) -> list[str]:
    return [line for line in text.splitlines() if f"[{tag}]" in line]


def classify_text(text: str) -> str:
    """Classify a skill into one guardrail level from its frontmatter and step tags."""
    fields = parse_frontmatter(text)
    if fields.get("disable-model-invocation") is True:
        return "human_only"
    if _tagged_steps(text, "irreversible"):
        return "irreversible"
    tools = set(fields.get("allowed-tools") or [])
    if _tagged_steps(text, "reversible") or (tools & WRITE_TOOLS):
        return "reversible"
    return "auto"


def reversible_steps_missing_undo(text: str) -> list[str]:
    """Every [reversible] step must document an explicit ``undo:`` command."""
    return [step for step in _tagged_steps(text, "reversible") if "undo:" not in step.lower()]


def irreversible_steps_missing_approval(text: str) -> list[str]:
    """Every [irreversible] step must carry an APPROVAL REQUIRED marker."""
    return [step for step in _tagged_steps(text, "irreversible") if _APPROVAL_MARKER not in step]


def classify(path) -> str:
    """Classify a SKILL.md file on disk into its guardrail level."""
    return classify_text(Path(path).read_text(encoding="utf-8"))
