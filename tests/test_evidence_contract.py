"""TDD tests for the BugHunter evidence-ladder output contract (tasks 10.005-10.006)."""

import pytest
from pydantic import ValidationError

from archlens.agents.evidence import EvidenceFinding


def _finding(**overrides):
    base = {"id": "f1", "category": "SPOF", "level": "EXTRACTED",
            "relation": "calls", "confidence": 0.9, "source_file": "x.py"}
    base.update(overrides)
    return base


def test_valid_finding_parses():
    finding = EvidenceFinding(**_finding())
    assert finding.level == "EXTRACTED"


@pytest.mark.parametrize("level", ["OBSERVED", "INFERRED", "EXTRACTED", "VALIDATED"])
def test_each_ladder_level_is_accepted(level):
    assert EvidenceFinding(**_finding(level=level)).level == level


def test_unknown_level_is_rejected():
    with pytest.raises(ValidationError):
        EvidenceFinding(**_finding(level="BOGUS"))


def test_confidence_below_floor_is_rejected():
    with pytest.raises(ValidationError):
        EvidenceFinding(**_finding(confidence=0.4))


def test_confidence_above_ceiling_is_rejected():
    with pytest.raises(ValidationError):
        EvidenceFinding(**_finding(confidence=0.99))


def test_missing_citation_triple_is_rejected():
    payload = _finding()
    del payload["source_file"]
    with pytest.raises(ValidationError):
        EvidenceFinding(**payload)
