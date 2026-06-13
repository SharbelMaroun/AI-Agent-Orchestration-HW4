"""TDD tests for structural bridges and community connectors (tasks 6.022-6.025)."""

from fixtures import build_barbell, build_two_community

from archlens.graphops.bridges import bridge_report, community_connectors, structural_bridges
from archlens.graphops.communities import detect_communities
from archlens.graphops.loader import load_graph


def test_structural_bridge_detected_on_barbell():
    graph = load_graph(build_barbell(3))
    assert structural_bridges(graph) == [("a0", "b0")]


def test_community_connector_detected_on_two_community():
    graph = load_graph(build_two_community())
    communities = detect_communities(graph)
    assert community_connectors(graph, communities) == [("x0", "y0")]


def test_bridge_report_keeps_structural_and_connector_in_separate_sections():
    graph = load_graph(build_two_community())
    communities = detect_communities(graph)
    report = bridge_report(graph, communities)
    assert isinstance(report.structural, tuple)
    assert isinstance(report.connector, tuple)
    assert len(report.structural) == 1
    assert len(report.connector) == 1
    assert report.connector[0].source_file == "pkgx/x0.py"
