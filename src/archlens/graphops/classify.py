"""Hub-vs-bottleneck classification via node-disjoint bypass paths (tasks 6.019, 6.021)."""

import networkx as nx

from archlens.graphops.centrality import betweenness
from archlens.graphops.dto import HubBottleneckVerdict


def alternative_paths(graph: nx.DiGraph, node: str) -> int:
    """Minimum node-disjoint paths between any two of ``node``'s neighbours once it is removed.

    Zero means the node is a cut vertex (a mandatory bottleneck); a higher value quantifies how
    much redundancy survives its removal.
    """
    undirected = graph.to_undirected()
    neighbours = sorted(undirected.neighbors(node))
    if len(neighbours) < 2:
        return 0
    pruned = undirected.copy()
    pruned.remove_node(node)
    best: int | None = None
    for i, src in enumerate(neighbours):
        for dst in neighbours[i + 1:]:
            paths = nx.node_connectivity(pruned, src, dst) if src in pruned and dst in pruned else 0
            best = paths if best is None else min(best, paths)
    return best or 0


def classify(graph: nx.DiGraph) -> list[HubBottleneckVerdict]:
    """Label every degree>=2 node HUB or BOTTLENECK, ranked by betweenness (desc)."""
    scores = betweenness(graph)
    verdicts = []
    for node in graph.nodes:
        degree = graph.degree(node)
        if degree < 2:
            continue
        bypass = alternative_paths(graph, node)
        verdict = "BOTTLENECK" if bypass == 0 else "HUB"
        rationale = (
            f"degree={degree}, betweenness={scores[node]:.3f}, bypass_paths={bypass} -> {verdict}"
        )
        verdicts.append(
            HubBottleneckVerdict(
                node_id=node,
                verdict=verdict,
                degree_total=degree,
                betweenness=scores[node],
                bypass_count=bypass,
                rationale=rationale,
                source_file=graph.nodes[node].get("source_file", ""),
            )
        )
    verdicts.sort(key=lambda v: (-v.betweenness, v.node_id))
    return verdicts
