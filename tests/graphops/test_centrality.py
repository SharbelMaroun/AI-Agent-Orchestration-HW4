"""TDD tests for degree and betweenness centrality (tasks 6.008-6.011)."""

from fixtures import build_barbell, build_star

from archlens.graphops.centrality import betweenness, degree_centrality
from archlens.graphops.loader import load_graph


def test_degree_centrality_hub_and_leaves_on_star():
    graph = load_graph(build_star(5))
    rows = {row.node_id: row for row in degree_centrality(graph)}
    hub = rows["n0"]
    assert (hub.degree_out, hub.degree_in, hub.degree_total) == (4, 0, 4)
    for i in range(1, 5):
        leaf = rows[f"n{i}"]
        assert (leaf.degree_in, leaf.degree_out, leaf.degree_total) == (1, 0, 1)


def test_degree_rows_are_ranked_by_total_descending():
    graph = load_graph(build_star(5))
    rows = degree_centrality(graph)
    totals = [row.degree_total for row in rows]
    assert totals == sorted(totals, reverse=True)
    assert rows[0].node_id == "n0"


def test_degree_row_cites_its_source_file():
    graph = load_graph(build_star(3))
    rows = {row.node_id: row for row in degree_centrality(graph)}
    assert rows["n0"].source_file == "n0"


def test_betweenness_on_barbell_matches_hand_computed():
    """Manual directed betweenness for build_barbell(3); normalised by 1/((n-1)(n-2)) = 1/20.

    Every cross-bell shortest path runs through the bridge endpoints a0 and b0. Counting
    intermediate appearances over all 24 ordered reachable pairs gives unnormalised scores
    a0=7, a2=4, a1=1, b0=7, b1=4, b2=1; dividing by 20 yields the expected values below.
    """
    graph = load_graph(build_barbell(3))
    scores = betweenness(graph)
    expected = {"a0": 0.35, "a1": 0.05, "a2": 0.20, "b0": 0.35, "b1": 0.20, "b2": 0.05}
    for node, value in expected.items():
        assert abs(scores[node] - value) < 1e-9


def test_betweenness_matches_centrality_row_values():
    graph = load_graph(build_barbell(3))
    scores = betweenness(graph)
    for row in degree_centrality(graph):
        assert abs(row.betweenness - scores[row.node_id]) < 1e-9
