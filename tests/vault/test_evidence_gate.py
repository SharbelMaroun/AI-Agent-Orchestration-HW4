"""TDD tests for the evidence-lint generation gate (task 7.035)."""

import pytest

from archlens.vault.evidence_lint import EvidenceLintError, enforce_evidence


def test_gate_passes_when_every_claim_is_tagged():
    enforce_evidence(["A bridge was found [EXTRACTED].", "A risk is inferred [INFERRED]."])


def test_gate_aborts_on_an_untagged_claim():
    with pytest.raises(EvidenceLintError):
        enforce_evidence(["A bridge was found [EXTRACTED].", "This claim has no tag."])
