"""TDD tests for modularity and inter-community edge-count metrics (tasks 6.016-6.017)."""

from fixtures import build_two_community

from archlens.graphops.graph_metrics import inter_community_edge_count, modularity
from archlens.graphops.loader import load_graph

# The two_community fixture: two triangles (3 intra edges each) plus one connector x0->y0.
COMMUNITIES = [{"x0", "x1", "x2"}, {"y0", "y1", "y2"}]


def test_inter_community_edge_count_is_one():
    graph = load_graph(build_two_community())
    assert inter_community_edge_count(graph, COMMUNITIES) == 1


def test_modularity_matches_hand_computed_value():
    """Undirected projection: m=7, each block has L=3 intra edges and total degree k=7.

    Q = 2 * [ L/m - (k/2m)^2 ] = 2 * [ 3/7 - (7/14)^2 ] = 0.35714285714285715.
    """
    graph = load_graph(build_two_community())
    assert abs(modularity(graph, COMMUNITIES) - 0.35714285714285715) < 1e-9


def test_inter_community_count_zero_for_single_community():
    graph = load_graph(build_two_community())
    assert inter_community_edge_count(graph, [{"x0", "x1", "x2", "y0", "y1", "y2"}]) == 0
