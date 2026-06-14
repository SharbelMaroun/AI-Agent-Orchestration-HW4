"""TDD tests for FixPriorityPolicy (task 11.007)."""

import pytest
from pydantic import ValidationError

from archlens.agents.fix_policy import FixCandidate, FixPriorityPolicy
from archlens.shared.config import load_setup
from archlens.shared.constants import FixPriority

ORDER = ["P1", "P2", "P3", "P4", "P5"]


def _cand(fix_id="f", kind="spof", confidence=0.8):
    return FixCandidate(
        fix_id=fix_id, kind=kind, level="VALIDATED",
        relation="calls", confidence=confidence, source_file="m.py",
    )


def test_priority_of_maps_each_kind():
    policy = FixPriorityPolicy(ORDER)
    expected = {
        "spof": FixPriority.P1, "bottleneck": FixPriority.P2, "oversized": FixPriority.P3,
        "duplicate": FixPriority.P4, "misalignment": FixPriority.P5,
    }
    for kind, prio in expected.items():
        assert policy.priority_of(_cand(kind=kind)) == prio


def test_order_places_p1_before_p4():
    ordered = FixPriorityPolicy(ORDER).order([_cand("dup", "duplicate"), _cand("spof", "spof")])
    assert [c.fix_id for c in ordered] == ["spof", "dup"]


def test_order_breaks_ties_by_confidence_desc():
    ordered = FixPriorityPolicy(ORDER).order([_cand("lo", "spof", 0.6), _cand("hi", "spof", 0.9)])
    assert [c.fix_id for c in ordered] == ["hi", "lo"]


def test_from_config_reads_priority_order():
    policy = FixPriorityPolicy.from_config(load_setup())
    ordered = policy.order([_cand("p3", "oversized"), _cand("p1", "spof")])
    assert [c.fix_id for c in ordered] == ["p1", "p3"]


def test_unknown_kind_rejected():
    with pytest.raises(ValidationError):
        _cand(kind="nonsense")
