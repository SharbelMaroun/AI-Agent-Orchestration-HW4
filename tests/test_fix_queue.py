"""TDD tests for the fix-candidate queue builder (task 11.011)."""

from archlens.agents.evidence_gate import EvidenceGate
from archlens.agents.fix_policy import FixCandidate, FixPriorityPolicy
from archlens.agents.fix_queue import FixQueueBuilder
from archlens.shared.config import load_setup

ORDER = ["P1", "P2", "P3", "P4", "P5"]
ALLOWED = ["EXTRACTED", "VALIDATED"]


def _cand(fix_id, kind, level="VALIDATED", confidence=0.8):
    return FixCandidate(
        fix_id=fix_id, kind=kind, level=level,
        relation="calls", confidence=confidence, source_file="m.py",
    )


def _builder():
    return FixQueueBuilder(FixPriorityPolicy(ORDER), EvidenceGate(ALLOWED))


def test_build_filters_blocked_then_sorts():
    cands = [
        _cand("dup", "duplicate", confidence=0.9),
        _cand("spof", "spof", confidence=0.6),
        _cand("blocked", "spof", level="OBSERVED", confidence=0.95),
    ]
    out = _builder().build(cands)
    assert [c.fix_id for c in out] == ["spof", "dup"]


def test_build_returns_empty_when_all_blocked():
    cands = [_cand("a", "spof", level="OBSERVED"), _cand("b", "duplicate", level="INFERRED")]
    assert _builder().build(cands) == []


def test_build_from_config():
    builder = FixQueueBuilder.from_config(load_setup())
    out = builder.build([_cand("p4", "duplicate"), _cand("p1", "spof")])
    assert [c.fix_id for c in out] == ["p1", "p4"]
