"""TDD tests for alternative paths and the hub-vs-bottleneck classifier (tasks 6.018-6.021)."""

from fixtures import build_bottleneck, build_healthy_hub

from archlens.graphops.classify import alternative_paths, classify
from archlens.graphops.loader import load_graph


def test_alternative_paths_on_healthy_hub_is_at_least_two():
    graph = load_graph(build_healthy_hub())
    assert alternative_paths(graph, "h") >= 2


def test_alternative_paths_on_bottleneck_is_zero():
    graph = load_graph(build_bottleneck())
    assert alternative_paths(graph, "gate") == 0


def test_verdict_labels_healthy_hub_as_hub():
    graph = load_graph(build_healthy_hub())
    verdicts = {v.node_id: v for v in classify(graph)}
    assert verdicts["h"].verdict == "HUB"
    assert verdicts["h"].bypass_count >= 2


def test_verdict_labels_bottleneck_as_bottleneck():
    graph = load_graph(build_bottleneck())
    verdicts = {v.node_id: v for v in classify(graph)}
    gate = verdicts["gate"]
    assert gate.verdict == "BOTTLENECK"
    assert gate.bypass_count == 0
    assert "degree" in gate.rationale
    assert "betweenness" in gate.rationale
    assert "bypass" in gate.rationale
