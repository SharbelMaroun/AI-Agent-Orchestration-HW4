"""TDD tests for the unimplemented-requirement (gap) detector (tasks 7.022-7.023)."""

from archlens.graphops.gap_detector import detect_gaps
from archlens.graphops.req_matcher import Match
from archlens.graphops.req_parser import Requirement

REQS = [
    Requirement("FR-01", "Process checkout payments", "Functional"),
    Requirement("FR-99", "Quantum teleportation subsystem", "Functional"),
]
MATCHES = [Match("FR-01", "checkout_service.py", 0.85)]


def test_unimplemented_requirement_is_listed():
    assert {g.req_id for g in detect_gaps(REQS, MATCHES)} == {"FR-99"}


def test_implemented_requirement_is_not_listed():
    assert "FR-01" not in {g.req_id for g in detect_gaps(REQS, MATCHES)}


def test_gap_records_the_searched_evidence():
    gaps = {g.req_id: g for g in detect_gaps(REQS, MATCHES)}
    assert gaps["FR-99"].searched
