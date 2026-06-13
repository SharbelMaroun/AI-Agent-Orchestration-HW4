"""TDD tests for the GraphDiff model and computation (tasks 4.042-4.045)."""

from pathlib import Path

from archlens.graphops.diff import GraphDiff, compute_diff
from archlens.graphops.parser import parse_graph

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"

_NODES = [
    {"id": "x", "type": "code", "source_file": "x.py"},
    {"id": "hub", "type": "code", "source_file": "hub.py"},
]


def test_model_exposes_all_stop_condition_fields():
    fields = set(GraphDiff.model_fields)
    assert {
        "added_nodes",
        "removed_nodes",
        "added_edges",
        "removed_edges",
        "inter_community_edge_delta",
        "new_isolated_components",
        "bottleneck_dependency_loss",
    } <= fields


def test_diff_counts_between_fixtures():
    diff = compute_diff(
        parse_graph(FIXTURES / "diff_before.json"),
        parse_graph(FIXTURES / "diff_after.json"),
    )
    assert diff.added_edges == ["b->lonely:calls"]
    assert diff.removed_edges == ["b->hub:calls"]
    assert diff.inter_community_edge_delta == -1
    assert diff.new_isolated_components == []


def test_moved_load_is_not_reported_as_dependency_loss():
    diff = compute_diff(
        parse_graph(FIXTURES / "diff_before.json"),
        parse_graph(FIXTURES / "diff_after.json"),
        bottleneck="hub",
    )
    assert diff.bottleneck_dependency_loss is False


def test_true_dependency_loss_is_detected():
    before = parse_graph(
        {
            "nodes": _NODES,
            "edges": [
                {
                    "from": "x",
                    "to": "hub",
                    "relation": "calls",
                    "type": "EXTRACTED",
                    "confidence": 0.95,
                    "source_file": "x.py",
                }
            ],
        }
    )
    after = parse_graph({"nodes": _NODES, "edges": []})
    diff = compute_diff(before, after, bottleneck="hub")
    assert diff.bottleneck_dependency_loss is True
