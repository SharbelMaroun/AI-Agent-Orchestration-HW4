"""Graph-diff metrics between two graph.json snapshots (tasks 11.032-11.038, Part C p21).

Answers the guiding question — did the structure change, or just the appearance? — by diffing
degree, betweenness, inter-community edges, and connected components across consecutive runs.
"""

import networkx as nx

from ..graphops.centrality import betweenness
from ..graphops.communities import detect_communities
from ..graphops.graph_metrics import inter_community_edge_count
from ..graphops.loader import load_graph


def degree_delta(before, after) -> dict[str, int]:
    """Per-node change in total degree (after - before); nodes absent on a side count as 0."""
    g0, g1 = load_graph(before), load_graph(after)
    d0 = {n: g0.degree(n) for n in g0.nodes}
    d1 = {n: g1.degree(n) for n in g1.nodes}
    return {n: d1.get(n, 0) - d0.get(n, 0) for n in set(d0) | set(d1)}


def betweenness_delta(before, after) -> dict[str, float]:
    """Per-node change in betweenness centrality (after - before)."""
    b0, b1 = betweenness(load_graph(before)), betweenness(load_graph(after))
    return {n: b1.get(n, 0.0) - b0.get(n, 0.0) for n in set(b0) | set(b1)}


def inter_community_edge_delta(before, after) -> int:
    """Change in inter-community edge count (after - before); negative means tighter modularity."""
    g0, g1 = load_graph(before), load_graph(after)
    c0 = inter_community_edge_count(g0, detect_communities(g0))
    c1 = inter_community_edge_count(g1, detect_communities(g1))
    return c1 - c0


def modularity_improved(before, after) -> bool:
    """SC-2: True only when inter-community edges strictly decreased."""
    return inter_community_edge_delta(before, after) < 0


def isolated_nodes(graph: nx.DiGraph) -> set[str]:
    """Nodes with total degree 0."""
    return {n for n in graph.nodes if graph.degree(n) == 0}


def new_isolated_components(before, after) -> bool:
    """SC-3: True when the post-fix graph has more isolated nodes or more weak components."""
    g0, g1 = load_graph(before), load_graph(after)
    more_isolated = len(isolated_nodes(g1)) > len(isolated_nodes(g0))
    grew = nx.number_weakly_connected_components(g1) > nx.number_weakly_connected_components(g0)
    return more_isolated or grew
