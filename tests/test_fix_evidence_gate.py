"""TDD tests for the evidence-level gate (task 11.009)."""

from archlens.agents.evidence_gate import EvidenceGate
from archlens.agents.fix_policy import FixCandidate
from archlens.shared.config import load_setup

ALLOWED = ["EXTRACTED", "VALIDATED"]


def _cand(fix_id="f", level="VALIDATED", relation="calls", source_file="m.py"):
    return FixCandidate(
        fix_id=fix_id, kind="spof", level=level,
        relation=relation, confidence=0.8, source_file=source_file,
    )


def test_rejects_observed_and_inferred():
    gate = EvidenceGate(ALLOWED)
    assert gate.admits(_cand(level="OBSERVED")) is False
    assert gate.admits(_cand(level="INFERRED")) is False


def test_admits_extracted_and_validated():
    gate = EvidenceGate(ALLOWED)
    assert gate.admits(_cand(level="EXTRACTED")) is True
    assert gate.admits(_cand(level="VALIDATED")) is True


def test_rejects_missing_citation():
    gate = EvidenceGate(ALLOWED)
    assert gate.admits(_cand(relation="")) is False
    assert gate.admits(_cand(source_file="")) is False


def test_filter_drops_blocked_levels():
    gate = EvidenceGate(ALLOWED)
    out = gate.filter([_cand("a", level="OBSERVED"), _cand("b", level="VALIDATED")])
    assert [c.fix_id for c in out] == ["b"]


def test_from_config_uses_allowed_levels():
    gate = EvidenceGate.from_config(load_setup())
    assert gate.admits(_cand(level="VALIDATED")) is True
    assert gate.admits(_cand(level="OBSERVED")) is False
