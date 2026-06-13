"""Degree and betweenness centrality over a loaded DiGraph (tasks 6.009, 6.011)."""

import networkx as nx

from archlens.graphops.dto import CentralityRow


def betweenness(graph: nx.DiGraph) -> dict[str, float]:
    """Normalised betweenness centrality per node — a thin wrapper over networkx."""
    return nx.betweenness_centrality(graph)


def degree_centrality(graph: nx.DiGraph) -> list[CentralityRow]:
    """Return CentralityRow DTOs ranked by total degree (desc), then node id for stability."""
    between = betweenness(graph)
    rows = [
        CentralityRow(
            node_id=node,
            degree_in=graph.in_degree(node),
            degree_out=graph.out_degree(node),
            degree_total=graph.degree(node),
            betweenness=between[node],
            source_file=graph.nodes[node].get("source_file", ""),
        )
        for node in graph.nodes
    ]
    rows.sort(key=lambda row: (-row.degree_total, row.node_id))
    return rows
