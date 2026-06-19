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
    # Reversible == a low-stakes write to a *derived* artifact (vault note/report), undo-snapshotted.
    assert classify_action("save the obsidian note") is ActionTier.REVERSIBLE
    assert requires_undo_path("save the obsidian note")


def test_classifier_irreversible_requires_human_approval():
    assert classify_action("git push --force") is ActionTier.IRREVERSIBLE
    assert requires_approval("git push --force")


def test_source_modification_is_irreversible_and_needs_approval():
    # ADR-009: any modification of the target's source is irreversible-tier -> human approval.
    assert classify_action("apply bottleneck fix to snippets/__init__.py") is ActionTier.IRREVERSIBLE
    assert requires_approval("edit a module file")
    assert requires_approval("split_module in core.py")


def test_classifier_follows_the_verb_not_the_target_path():
    # A loaded word in the *path* (after the verb) must not change the tier.
    assert classify_action("apply spof fix to deploy.py") is ActionTier.IRREVERSIBLE  # 'apply', not 'deploy'
    assert classify_action("save the note to deploy_guide.md") is ActionTier.REVERSIBLE  # not 'deploy'
    assert classify_action("inspect the module at delete_helper.py") is ActionTier.READ_ONLY  # not 'delete'


def test_undo_registry_rolls_back_byte_identically(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("original\n", encoding="utf-8")
    registry = UndoRegistry()
    registry.snapshot(target)
    target.write_text("edited content\n", encoding="utf-8")
    registry.rollback(target)
    assert target.read_text(encoding="utf-8") == "original\n"
