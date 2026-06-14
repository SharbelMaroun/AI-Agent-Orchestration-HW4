"""Moved-vs-removed load detector for SC-1 (task 11.040, Part C p21).

A bottleneck fix is genuine only if the targeted node truly shed dependencies; if the load
merely migrated to an adjacent node (its degree/betweenness rose to within 10% of the old
bottleneck's pre-fix value), the fix is rejected.
"""

from ..graphops.centrality import betweenness
from ..graphops.loader import load_graph

_MIGRATION_RATIO = 0.10


def _deg(graph, node) -> int:
    return graph.degree(node) if graph.has_node(node) else 0


def load_migrated(before, after, target: str, ratio: float = _MIGRATION_RATIO) -> bool:
    """True when load left the target but reappeared on another node (migration, not removal)."""
    g0, g1 = load_graph(before), load_graph(after)
    b0, b1 = betweenness(g0), betweenness(g1)
    deg_threshold = (1 - ratio) * _deg(g0, target)
    bet_threshold = (1 - ratio) * b0.get(target, 0.0)
    for node in g1.nodes:
        if node == target:
            continue
        gained_degree = _deg(g1, node) > _deg(g0, node) and _deg(g1, node) >= deg_threshold
        gained_between = b1.get(node, 0.0) > b0.get(node, 0.0) and b1.get(node, 0.0) >= bet_threshold
        if gained_degree or gained_between:
            return True
    return False


def dependencies_lost(before, after, target: str, ratio: float = _MIGRATION_RATIO) -> bool:
    """SC-1: target shed both degree and betweenness AND no other node absorbed the load."""
    g0, g1 = load_graph(before), load_graph(after)
    b0, b1 = betweenness(g0), betweenness(g1)
    shed = _deg(g1, target) < _deg(g0, target) and b1.get(target, 0.0) < b0.get(target, 0.0)
    return shed and not load_migrated(before, after, target, ratio)
