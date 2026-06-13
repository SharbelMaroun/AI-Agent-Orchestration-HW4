"""TDD tests for the orphan-module detector (tasks 7.024-7.025)."""

from pathlib import Path

from archlens.graphops.orphan_detector import detect_orphans
from archlens.graphops.req_matcher import Match

FULL = Path(__file__).resolve().parents[1] / "fixtures" / "graphify" / "full.json"
MATCHES = [Match("FR-01", "checkout_service.py", 0.85)]


def test_module_without_a_requirement_is_an_orphan():
    modules = {o.module for o in detect_orphans(FULL, MATCHES)}
    assert "session_store.py" in modules


def test_matched_module_is_excluded():
    assert all(o.module != "checkout_service.py" for o in detect_orphans(FULL, MATCHES))


def test_orphans_sorted_by_degree_descending():
    degrees = [o.degree for o in detect_orphans(FULL, MATCHES)]
    assert degrees == sorted(degrees, reverse=True)
