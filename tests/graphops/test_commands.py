"""TDD tests for the query, path, explain, and diff commands (tasks 6.047-6.050)."""

from fixtures import build_composite

from archlens.graphops.commands import diff, explain, path, query
from archlens.graphops.loader import load_graph


def _three_chain(edges: list[tuple[str, str]]) -> dict:
    nodes = [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in ("a", "b", "c")]
    return {
        "nodes": nodes,
        "edges": [
            {"from": u, "to": v, "relation": "calls", "type": "EXTRACTED",
             "confidence": 0.95, "source_file": f"{u}.py"}
            for u, v in edges
        ],
    }


def test_query_filters_nodes_and_edges_by_attribute():
    graph = load_graph(build_composite())
    result = query(graph, node={"type": "doc"}, edge={"type": "AMBIGUOUS"})
    assert result["nodes"] == ["PRD"]
    assert result["edges"] == [("c3", "sink")]


def test_path_returns_shortest_path_with_per_edge_citations():
    graph = load_graph(build_composite())
    citations = path(graph, "c1", "sink")
    assert [c.relation for c in citations] == ["calls", "calls", "calls"]
    assert all(c.source_file for c in citations)


def test_explain_returns_the_edge_citation():
    graph = load_graph(build_composite())
    citation = explain(graph, "PRD", "hub")
    assert citation.relation == "implements"
    assert citation.confidence == 0.82


def test_diff_reports_dependency_loss_and_isolation():
    before = load_graph(_three_chain([("a", "b"), ("b", "c")]))
    after = load_graph(_three_chain([("a", "b")]))
    report = diff(before, after)
    assert report.dependency_loss == 1
    assert report.isolated_after == 1
