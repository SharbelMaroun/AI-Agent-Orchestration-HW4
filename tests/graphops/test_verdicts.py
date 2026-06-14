"""TDD tests for the evidence-grounded verdict generator (tasks 7.031-7.032)."""

from pathlib import Path

from archlens.graphops.req_matcher import Match
from archlens.graphops.traceability import build_traceability
from archlens.graphops.verdicts import generate_verdicts

FULL = Path(__file__).resolve().parents[1] / "fixtures" / "graphify" / "full.json"
MATCHES = [
    Match("FR-01", "checkout_service.py", 0.85),
    Match("FR-02", "billing_api.py", 0.75),
]


def _verdicts() -> dict:
    return {v.req_id: v for v in generate_verdicts(build_traceability(MATCHES, FULL), FULL)}


def test_verdict_is_three_or_four_sentences():
    assert all(3 <= len(v.sentences) <= 4 for v in _verdicts().values())


def test_verdict_cites_relation_confidence_and_source_file():
    text = _verdicts()["FR-01"].text
    assert "->" in text
    assert "0.85" in text
    assert "checkout_service.py" in text


def test_full_traceability_label_when_tested():
    assert _verdicts()["FR-01"].label == "full traceability"


def test_possible_gap_label_when_untested():
    assert _verdicts()["FR-02"].label == "possible gap"
