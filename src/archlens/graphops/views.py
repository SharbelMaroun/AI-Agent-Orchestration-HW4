"""Macro, meso, and micro reading APIs over the loaded graph (tasks 6.042, 6.044, 6.046)."""

import networkx as nx

from ..graphops.bridges import community_connectors
from ..graphops.centrality import degree_centrality
from ..graphops.dto import Citation, CommunitySummary, MacroView, Neighborhood


def macro_view(graph: nx.DiGraph) -> MacroView:
    """Whole-graph summary: counts, density, weak components, and the top-5 hubs."""
    ranked = degree_centrality(graph)
    return MacroView(
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        density=nx.density(graph),
        component_count=nx.number_weakly_connected_components(graph),
        top_hubs=tuple(row.node_id for row in ranked[:5]),
    )


def meso_view(graph: nx.DiGraph, communities: list[set[str]]) -> list[CommunitySummary]:
    """One CommunitySummary per community, each carrying the connectors that touch it."""
    connectors = community_connectors(graph, communities)
    summaries = []
    for community_id, members in enumerate(communities):
        touching = tuple((u, v) for u, v in connectors if u in members or v in members)
        summaries.append(
            CommunitySummary(community_id, len(members), tuple(sorted(members)), touching)
        )
    return summaries


def micro_view(graph: nx.DiGraph, node: str) -> Neighborhood:
    """Single-node neighbourhood with one citation per incident edge."""
    citations = [
        Citation(data.get("relation", ""), data.get("confidence", 0.0), data.get("source_file", ""))
        for _, _, data in list(graph.in_edges(node, data=True)) + list(graph.out_edges(node, data=True))
    ]
    return Neighborhood(
        node_id=node,
        predecessors=tuple(sorted(graph.predecessors(node))),
        successors=tuple(sorted(graph.successors(node))),
        citations=tuple(citations),
    )
