"""TDD tests for the macro, meso, and micro reading APIs (tasks 6.041-6.046)."""

from fixtures import build_composite, build_two_community

from archlens.graphops.communities import detect_communities
from archlens.graphops.loader import load_graph
from archlens.graphops.views import macro_view, meso_view, micro_view


def test_macro_view_counts_and_top_hub_on_composite():
    view = macro_view(load_graph(build_composite()))
    assert view.node_count == 9
    assert view.edge_count == 8
    assert view.component_count == 2
    assert abs(view.density - 8 / 72) < 1e-9
    assert view.top_hubs[0] == "hub"
    assert len(view.top_hubs) == 5


def test_meso_view_one_summary_per_community_with_connectors():
    graph = load_graph(build_two_community())
    communities = detect_communities(graph)
    summaries = meso_view(graph, communities)
    assert len(summaries) == 2
    all_connectors = {edge for summary in summaries for edge in summary.connectors}
    assert ("x0", "y0") in all_connectors


def test_micro_view_neighbourhood_has_cited_edges():
    view = micro_view(load_graph(build_composite()), "hub")
    assert set(view.predecessors) == {"c1", "c2", "c3", "PRD"}
    assert set(view.successors) == {"mid"}
    assert len(view.citations) == 5
    assert all(c.source_file for c in view.citations)
