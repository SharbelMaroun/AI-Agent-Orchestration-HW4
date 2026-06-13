"""TDD tests for the graph.json parser and Graph aggregate (tasks 4.031-4.033)."""

from pathlib import Path

import pytest

from archlens.graphops.errors import GraphParseError
from archlens.graphops.parser import Graph, parse_graph

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"


def test_parse_full_fixture_counts():
    graph = parse_graph(FIXTURES / "full.json")
    assert isinstance(graph, Graph)
    assert len(graph.nodes) == 6
    assert len(graph.edges) == 5
    assert len(graph.communities) == 2
    assert len(graph.hyperedges) == 1
    assert len(graph.rationale_nodes) == 1


def test_parse_minimal_fixture():
    graph = parse_graph(FIXTURES / "minimal.json")
    assert len(graph.nodes) == 2
    assert graph.communities == []


def test_malformed_fixture_raises_graph_parse_error():
    with pytest.raises(GraphParseError, match="edges"):
        parse_graph(FIXTURES / "malformed.json")


def test_unknown_community_member_raises():
    bad = {
        "nodes": [{"id": "a.py", "type": "code", "source_file": "a.py"}],
        "communities": [{"community_id": "c1", "label": "x", "node_ids": ["ghost.py"]}],
    }
    with pytest.raises(GraphParseError, match="ghost.py"):
        parse_graph(bad)


def test_non_object_root_raises():
    with pytest.raises(GraphParseError):
        parse_graph([1, 2, 3])
