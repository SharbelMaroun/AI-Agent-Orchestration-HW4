"""TDD tests for the requirement-to-module matcher (tasks 7.020-7.021)."""

from pathlib import Path

from archlens.graphops.req_matcher import match_requirements
from archlens.graphops.req_parser import Requirement

FULL = Path(__file__).resolve().parents[1] / "fixtures" / "graphify" / "full.json"

REQS = [
    Requirement("FR-01", "Process checkout service payments", "Functional"),
    Requirement("FR-99", "Quantum teleportation subsystem", "Functional"),
]


def test_match_produces_req_module_confidence_tuples():
    matches = match_requirements(REQS, FULL)
    assert matches
    assert all(m.req_id and m.module and isinstance(m.confidence, float) for m in matches)


def test_confidence_bounded_between_floor_and_strong():
    assert all(0.55 <= m.confidence <= 0.95 for m in match_requirements(REQS, FULL))


def test_keyword_links_requirement_to_module():
    modules = {m.module for m in match_requirements(REQS, FULL) if m.req_id == "FR-01"}
    assert "checkout_service.py" in modules


def test_threshold_above_max_confidence_excludes_all():
    assert match_requirements(REQS, FULL, threshold=0.99) == []
