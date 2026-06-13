"""TDD tests for the FR-xx/NFR-xx requirement parser (tasks 7.018-7.019)."""

from pathlib import Path

from archlens.graphops.req_parser import parse_requirements

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "prd_sample.md"


def test_parses_fr_and_nfr_ids():
    ids = {r.id for r in parse_requirements(FIXTURE)}
    assert {"FR-01", "FR-02", "NFR-01", "NFR-02"} <= ids


def test_captures_requirement_titles():
    reqs = {r.id: r for r in parse_requirements(FIXTURE)}
    assert "checkout" in reqs["FR-01"].title.lower()


def test_captures_section_context():
    reqs = {r.id: r for r in parse_requirements(FIXTURE)}
    assert reqs["FR-01"].section == "Functional Requirements"
    assert reqs["NFR-01"].section == "Non-Functional Requirements"
