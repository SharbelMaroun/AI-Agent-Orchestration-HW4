"""TDD tests for loading a graph.json into a networkx DiGraph (tasks 6.001-6.004)."""

from pathlib import Path

import networkx as nx
import pytest

from archlens.graphops.errors import GraphSchemaError
from archlens.graphops.loader import load_graph

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def _two_nodes() -> list[dict]:
    return [
        {"id": "a.py", "type": "code", "source_file": "a.py"},
        {"id": "b.py", "type": "code", "source_file": "b.py"},
    ]


def test_load_minimal_returns_digraph():
    graph = load_graph(FIXTURES / "minimal.json")
    assert isinstance(graph, nx.DiGraph)
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1


def test_load_preserves_node_ids_and_type_and_source_file():
    graph = load_graph(FIXTURES / "full.json")
    assert set(graph.nodes) == {
        "checkout_service.py",
        "billing_api.py",
        "auth_controller.py",
        "session_store.py",
        "PRD_payments.md",
        "test_checkout.py",
    }
    node = graph.nodes["checkout_service.py"]
    assert node["type"] == "code"
    assert node["source_file"] == "src/payments/checkout_service.py"


def test_load_preserves_edge_relation_type_confidence_source_file():
    graph = load_graph(FIXTURES / "full.json")
    data = graph.edges["checkout_service.py", "billing_api.py"]
    assert data["relation"] == "calls"
    assert data["type"] == "EXTRACTED"
    assert data["confidence"] == 0.95
    assert data["source_file"] == "src/payments/checkout_service.py"


def test_load_accepts_a_dict_source():
    raw = {
        "nodes": [{"id": "a.py", "type": "code", "source_file": "a.py"}],
        "edges": [],
    }
    graph = load_graph(raw)
    assert list(graph.nodes) == ["a.py"]
    assert graph.number_of_edges() == 0


def test_rejects_edge_with_missing_source_file():
    bad = {"nodes": _two_nodes(), "edges": [
        {"from": "a.py", "to": "b.py", "relation": "calls", "type": "EXTRACTED", "confidence": 0.95},
    ]}
    with pytest.raises(GraphSchemaError, match=r"a\.py->b\.py"):
        load_graph(bad)


def test_rejects_confidence_above_one():
    bad = {"nodes": _two_nodes(), "edges": [
        {"from": "a.py", "to": "b.py", "relation": "calls", "type": "EXTRACTED",
         "confidence": 1.5, "source_file": "a.py"},
    ]}
    with pytest.raises(GraphSchemaError, match="1.5"):
        load_graph(bad)


def test_rejects_confidence_below_zero():
    bad = {"nodes": _two_nodes(), "edges": [
        {"from": "a.py", "to": "b.py", "relation": "calls", "type": "INFERRED",
         "confidence": -0.1, "source_file": "a.py"},
    ]}
    with pytest.raises(GraphSchemaError, match="a\\.py->b\\.py"):
        load_graph(bad)


def test_rejects_unknown_relation():
    bad = {"nodes": _two_nodes(), "edges": [
        {"from": "a.py", "to": "b.py", "relation": "frobnicate", "type": "INFERRED",
         "confidence": 0.8, "source_file": "a.py"},
    ]}
    with pytest.raises(GraphSchemaError, match="frobnicate"):
        load_graph(bad)


def _native(links: list[dict]) -> dict:
    """A Graphify networkx node-link export (edges under ``links``, no strict ``edges``)."""
    return {
        "directed": False, "multigraph": False, "graph": {}, "hyperedges": [],
        "nodes": [{"id": "a", "file_type": "code", "source_file": "a.py", "community": 1},
                  {"id": "b", "file_type": "document", "source_file": "b.md", "community": 1}],
        "links": links,
    }


def test_loads_real_graphify_node_link_format():
    # Graphify emits source/target, a string evidence tier, and a wider relation vocab
    # ("contains") that the canonical strict schema would reject — it must load anyway.
    graph = load_graph(_native([
        {"source": "a", "target": "b", "relation": "contains",
         "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "a.py"},
    ]))
    assert (graph.number_of_nodes(), graph.number_of_edges()) == (2, 1)
    edge = graph.edges["a", "b"]
    assert edge["relation"] == "contains"      # wider vocab preserved, not rejected
    assert edge["type"] == "EXTRACTED"          # tier -> triage bucket
    assert edge["confidence"] == 1.0            # numeric confidence_score


def test_native_unknown_tier_falls_back_to_ambiguous():
    graph = load_graph(_native([
        {"source": "a", "target": "b", "relation": "calls", "confidence": "WEIRD",
         "source_file": "a.py"},
    ]))
    assert graph.edges["a", "b"]["type"] == "AMBIGUOUS"


def test_error_lists_every_offending_edge():
    nodes = _two_nodes() + [
        {"id": "c.py", "type": "code", "source_file": "c.py"},
        {"id": "d.py", "type": "code", "source_file": "d.py"},
    ]
    bad = {"nodes": nodes, "edges": [
        {"from": "a.py", "to": "b.py", "relation": "nope", "type": "INFERRED",
         "confidence": 0.8, "source_file": "a.py"},
        {"from": "c.py", "to": "d.py", "relation": "calls", "type": "EXTRACTED",
         "confidence": 9.0, "source_file": "c.py"},
    ]}
    with pytest.raises(GraphSchemaError) as exc:
        load_graph(bad)
    message = str(exc.value)
    assert "a.py->b.py" in message
    assert "c.py->d.py" in message
