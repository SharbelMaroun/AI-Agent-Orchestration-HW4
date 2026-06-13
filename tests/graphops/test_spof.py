"""TDD tests for critical-path extraction and the SPOF detector (tasks 6.026-6.030)."""

from fixtures import build_auth_path

from archlens.graphops.loader import load_graph
from archlens.graphops.spof import critical_paths, spof_detect


def test_critical_path_extracted_from_the_auth_chain():
    graph = load_graph(build_auth_path())
    paths = critical_paths(graph)
    assert paths == [["controller", "validator", "session_store", "policy"]]


def test_spof_detector_flags_session_store_with_per_hop_citations():
    graph = load_graph(build_auth_path())
    findings = {finding.node_id: finding for finding in spof_detect(graph)}
    assert "session_store" in findings
    finding = findings["session_store"]
    assert finding.broken_paths == 1
    assert [c.relation for c in finding.citations] == [
        "validates",
        "writes_session",
        "checks_policy",
    ]
    assert all(c.source_file for c in finding.citations)


def test_spof_detector_empty_when_no_critical_edges():
    graph = load_graph({
        "nodes": [{"id": "a", "type": "code", "source_file": "a.py"}],
        "edges": [],
    })
    assert spof_detect(graph) == []
