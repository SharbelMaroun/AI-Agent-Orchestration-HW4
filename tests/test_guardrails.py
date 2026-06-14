"""TDD tests for the three-tier guardrail classifier and undo registry (10.033-10.035)."""

from archlens.agents.guardrails import (
    ActionTier,
    UndoRegistry,
    classify_action,
    requires_approval,
    requires_undo_path,
)


def test_classifier_read_only_executes_automatically():
    assert classify_action("analyze the graph") is ActionTier.READ_ONLY
    assert not requires_approval("analyze the graph")
    assert not requires_undo_path("analyze the graph")


def test_classifier_reversible_requires_undo_path():
    assert classify_action("edit a module file") is ActionTier.REVERSIBLE
    assert requires_undo_path("edit a module file")


def test_classifier_irreversible_requires_human_approval():
    assert classify_action("git push --force") is ActionTier.IRREVERSIBLE
    assert requires_approval("git push --force")


def test_undo_registry_rolls_back_byte_identically(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("original\n", encoding="utf-8")
    registry = UndoRegistry()
    registry.snapshot(target)
    target.write_text("edited content\n", encoding="utf-8")
    registry.rollback(target)
    assert target.read_text(encoding="utf-8") == "original\n"
