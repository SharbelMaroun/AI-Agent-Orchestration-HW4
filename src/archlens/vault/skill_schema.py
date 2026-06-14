"""SKILL.md frontmatter schema parsing and validation (task 14.006).

Validates that a skill's YAML frontmatter declares non-empty name, description, and allowed-tools.
Hand-parses a minimal frontmatter subset (no YAML dependency); exposed via sdk.validate_skill.
"""

from pathlib import Path

REQUIRED_FIELDS = ("name", "description", "allowed-tools")


def _coerce(raw: str):
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip() for item in raw[1:-1].split(",") if item.strip()]
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    return raw


def parse_frontmatter(text: str) -> dict:
    """Parse the leading --- delimited block into a dict; ``[a, b]`` becomes a list."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, raw = line.partition(":")
            fields[key.strip()] = _coerce(raw.strip())
    return fields


def validate_skill_text(text: str) -> list[str]:
    """Return a list of error strings; an empty list means the frontmatter is valid."""
    fields = parse_frontmatter(text)
    errors = []
    for field in REQUIRED_FIELDS:
        value = fields.get(field)
        if value is None or value == "" or value == []:
            errors.append(f"missing or empty field: {field}")
    return errors


def validate_skill(path) -> list[str]:
    """Validate a SKILL.md file on disk; return error strings (empty = valid)."""
    return validate_skill_text(Path(path).read_text(encoding="utf-8"))
