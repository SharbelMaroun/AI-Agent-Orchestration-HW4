"""Modularity and inter-community edge metrics feeding the improvement-loop diff (task 6.017)."""

import networkx as nx
from networkx.algorithms.community import modularity as nx_modularity


def _membership(communities: list[set[str]]) -> dict[str, int]:
    return {node: index for index, members in enumerate(communities) for node in members}


def modularity(graph: nx.DiGraph, communities: list[set[str]]) -> float:
    """Modularity of the partition over the undirected projection of the graph."""
    return nx_modularity(graph.to_undirected(), [set(c) for c in communities])


def inter_community_edge_count(graph: nx.DiGraph, communities: list[set[str]]) -> int:
    """Count edges whose endpoints fall in different communities (Part C stop conditions)."""
    member = _membership(communities)
    return sum(1 for src, dst in graph.edges if member.get(src) != member.get(dst))
