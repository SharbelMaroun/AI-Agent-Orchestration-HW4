"""TDD tests for the PRD->Module->Test traceability chain builder (tasks 7.029-7.030)."""

from pathlib import Path

from archlens.graphops.req_matcher import Match
from archlens.graphops.traceability import build_traceability

FULL = Path(__file__).resolve().parents[1] / "fixtures" / "graphify" / "full.json"
MATCHES = [
    Match("FR-01", "checkout_service.py", 0.85),
    Match("FR-02", "billing_api.py", 0.75),
]


def _chains() -> dict:
    return {(c.req_id, c.module): c for c in build_traceability(MATCHES, FULL)}


def test_chain_links_requirement_module_and_test():
    chain = _chains()[("FR-01", "checkout_service.py")]
    assert chain.module_confidence == 0.85
    assert "test_checkout.py" in chain.tests


def test_module_to_test_link_carries_confidence():
    assert _chains()[("FR-01", "checkout_service.py")].test_confidence == 0.95


def test_module_without_test_has_empty_tests():
    assert _chains()[("FR-02", "billing_api.py")].tests == ()


def test_one_chain_per_match():
    assert len(build_traceability(MATCHES, FULL)) == 2
