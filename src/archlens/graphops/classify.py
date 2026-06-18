"""Hub-vs-bottleneck classification via node-disjoint bypass paths (tasks 6.019, 6.021)."""

import networkx as nx

from ..graphops.centrality import betweenness
from ..graphops.dto import HubBottleneckVerdict

# Surviving redundancy reported for a non-cut node. A non-articulation node sits in a biconnected
# block, so >=2 node-disjoint paths connect its neighbours after removal; the exact count above 2
# is cosmetic (the verdict turns only on 0-vs-nonzero) and computing it is all-pairs max-flow.
_REDUNDANCY_FLOOR = 2


def alternative_paths(graph: nx.DiGraph, node: str, undirected=None, articulation=None) -> int:
    """Node-disjoint bypass paths between ``node``'s neighbours once it is removed.

    Zero means the node is a cut vertex (a mandatory bottleneck / single point of failure); a
    positive value means redundancy survives its removal. Removing a node disconnects two of its
    neighbours **iff** that node is an articulation point, so the cut-vertex test is the exact
    O(V+E) ``articulation_points`` membership check. The surviving-redundancy count is reported
    as ``_REDUNDANCY_FLOOR`` (only 0 vs >=2
    drives the verdict, and the agent consumes the verdict, not the count).
    """
    undirected = undirected if undirected is not None else graph.to_undirected()
    if undirected.degree(node) < 2:
        return 0
    articulation = articulation if articulation is not None else set(nx.articulation_points(undirected))
    return 0 if node in articulation else _REDUNDANCY_FLOOR


def classify(graph: nx.DiGraph) -> list[HubBottleneckVerdict]:
    """Label every degree>=2 node HUB or BOTTLENECK, ranked by betweenness (desc)."""
    scores = betweenness(graph)
    undirected = graph.to_undirected()
    articulation = set(nx.articulation_points(undirected))
    verdicts = []
    for node in graph.nodes:
        degree = graph.degree(node)
        if degree < 2:
            continue
        bypass = alternative_paths(graph, node, undirected=undirected, articulation=articulation)
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
