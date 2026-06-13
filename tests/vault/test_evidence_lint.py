"""TDD tests for the evidence-ladder language linter (tasks 7.033-7.034)."""

from archlens.vault.evidence_lint import lint_claims


def test_untagged_claim_is_a_violation():
    assert lint_claims(["The module is a hub."]) == ["The module is a hub."]


def test_single_tagged_claim_passes():
    assert lint_claims(["The module is a hub [EXTRACTED]."]) == []


def test_each_ladder_tag_is_accepted():
    for tag in ("OBSERVED", "INFERRED", "EXTRACTED", "VALIDATED"):
        assert lint_claims([f"A claim [{tag}]."]) == []


def test_two_tags_is_a_violation():
    assert lint_claims(["A claim [EXTRACTED] and also [INFERRED]."])
