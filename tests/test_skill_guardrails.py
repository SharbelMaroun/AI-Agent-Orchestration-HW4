"""TDD tests for skill guardrail classification (task 14.007)."""

from pathlib import Path

from archlens.vault.skill_guardrails import (
    classify,
    classify_text,
    irreversible_steps_missing_approval,
    reversible_steps_missing_undo,
)

READONLY = ("---\nname: r\ndescription: d\nallowed-tools: [Read, Grep]\n---\n"
            "# Procedure\n- read the graph\n")
REVERSIBLE = ("---\nname: r\ndescription: d\nallowed-tools: [Edit]\n---\n"
              "# Procedure\n- [reversible] edit file; undo: git revert HEAD\n")
IRREVERSIBLE = ("---\nname: r\ndescription: d\nallowed-tools: [Bash]\n---\n"
                "# Procedure\n- [irreversible] delete file. APPROVAL REQUIRED\n")
HUMAN_ONLY = ("---\nname: r\ndescription: d\nallowed-tools: [Edit]\n"
              "disable-model-invocation: true\n---\n# Procedure\n- [reversible] x; undo: git revert\n")


def test_readonly_is_auto():
    assert classify_text(READONLY) == "auto"


def test_write_tool_with_reversible_step_is_reversible():
    assert classify_text(REVERSIBLE) == "reversible"


def test_irreversible_step_is_irreversible():
    assert classify_text(IRREVERSIBLE) == "irreversible"


def test_disable_model_invocation_is_human_only():
    assert classify_text(HUMAN_ONLY) == "human_only"


def test_reversible_step_without_undo_flagged():
    bad = REVERSIBLE.replace("; undo: git revert HEAD", "")
    assert reversible_steps_missing_undo(bad)
    assert reversible_steps_missing_undo(REVERSIBLE) == []


def test_irreversible_step_without_approval_flagged():
    bad = IRREVERSIBLE.replace(" APPROVAL REQUIRED", "")
    assert irreversible_steps_missing_approval(bad)
    assert irreversible_steps_missing_approval(IRREVERSIBLE) == []


def test_classify_reads_from_disk(tmp_path):
    path = Path(tmp_path) / "SKILL_x.md"
    path.write_text(READONLY, encoding="utf-8")
    assert classify(path) == "auto"


_SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"


def test_graph_reading_skill_file_is_auto():
    """Expected: the shipped SKILL_graph_reading.md classifies as auto / read-only (task 14.012)."""
    assert classify(_SKILLS_DIR / "SKILL_graph_reading.md") == "auto"


def test_refactor_skill_file_guardrails():
    """Expected: SKILL_refactor.md is human-only with undo paths + approval markers (task 14.017)."""
    text = (_SKILLS_DIR / "SKILL_refactor.md").read_text(encoding="utf-8")
    assert classify_text(text) == "human_only"
    assert reversible_steps_missing_undo(text) == []
    assert irreversible_steps_missing_approval(text) == []
