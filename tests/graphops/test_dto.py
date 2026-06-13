"""TDD tests for the frozen analysis DTOs and the Citation value object (tasks 6.006-6.007)."""

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from archlens.graphops.dto import (
    BridgeReport,
    CentralityRow,
    Citation,
    DuplicatePair,
    HubBottleneckVerdict,
    ReviewItem,
    SpofFinding,
    TriageItem,
)

DTO_CLASSES = [
    CentralityRow,
    HubBottleneckVerdict,
    BridgeReport,
    SpofFinding,
    TriageItem,
    DuplicatePair,
    ReviewItem,
]


@pytest.mark.parametrize("cls", [*DTO_CLASSES, Citation])
def test_every_dto_is_a_frozen_dataclass(cls):
    assert is_dataclass(cls)
    assert cls.__dataclass_params__.frozen


def test_citation_exposes_relation_confidence_source_file():
    citation = Citation(relation="calls", confidence=0.95, source_file="a.py")
    assert (citation.relation, citation.confidence, citation.source_file) == ("calls", 0.95, "a.py")
    with pytest.raises(FrozenInstanceError):
        citation.confidence = 0.1


def test_node_dtos_are_traceable_to_a_source_file():
    row = CentralityRow(
        node_id="hub", degree_in=3, degree_out=1, degree_total=4,
        betweenness=0.5, source_file="src/hub.py",
    )
    verdict = HubBottleneckVerdict(
        node_id="hub", verdict="HUB", degree_total=4, betweenness=0.5,
        bypass_count=2, rationale="alternatives exist", source_file="src/hub.py",
    )
    assert row.source_file == "src/hub.py"
    assert verdict.source_file == "src/hub.py"


def test_edge_finding_dtos_carry_a_citation():
    cite = Citation("calls", 0.95, "a.py")
    triage = TriageItem(src="a.py", dst="b.py", bucket="EXTRACTED", citation=cite)
    review = ReviewItem(src="a.py", dst="b.py", reason="ambiguous", citation=cite)
    duplicate = DuplicatePair(node_a="x", node_b="y", similarity=0.92, citation=cite)
    for finding in (triage, review, duplicate):
        assert finding.citation.relation == "calls"
        assert finding.citation.confidence == 0.95
        assert finding.citation.source_file == "a.py"


def test_spof_finding_carries_a_per_hop_citation_chain():
    chain = (Citation("validates", 0.95, "c.py"), Citation("writes_session", 0.95, "v.py"))
    finding = SpofFinding(node_id="session_store", broken_paths=1, citations=chain)
    assert all(c.source_file for c in finding.citations)


def test_bridge_report_separates_structural_from_connector():
    report = BridgeReport(
        structural=(Citation("calls", 0.95, "a.py"),),
        connector=(Citation("uses", 0.6, "b.py"),),
    )
    assert len(report.structural) == 1
    assert len(report.connector) == 1
