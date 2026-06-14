"""TDD tests for SKILL.md schema validation (task 14.005)."""

from archlens.vault.skill_schema import parse_frontmatter, validate_skill_text

VALID = """---
name: graph-reading
description: Read the dependency graph to answer architecture questions.
allowed-tools: [Read, Grep, Glob]
---
# When to use
Use for read-only graph questions.
"""


def test_valid_skill_has_no_errors():
    assert validate_skill_text(VALID) == []


def test_missing_name_rejected():
    text = VALID.replace("name: graph-reading\n", "")
    assert any("name" in error for error in validate_skill_text(text))


def test_empty_description_rejected():
    text = VALID.replace(
        "description: Read the dependency graph to answer architecture questions.",
        "description:")
    assert any("description" in error for error in validate_skill_text(text))


def test_empty_allowed_tools_rejected():
    text = VALID.replace("allowed-tools: [Read, Grep, Glob]", "allowed-tools: []")
    assert any("allowed-tools" in error for error in validate_skill_text(text))


def test_parse_frontmatter_reads_lists_and_scalars():
    fields = parse_frontmatter(VALID)
    assert fields["name"] == "graph-reading"
    assert fields["allowed-tools"] == ["Read", "Grep", "Glob"]
