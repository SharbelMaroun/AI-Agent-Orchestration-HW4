"""Synthetic graph fixtures with known answers for graphops analysis tests (task 6.005).

Each builder returns a canonical graph.json dict (nodes + edges) that ``load_graph`` accepts.
The known structural answers are documented per builder so analysis tests assert against them.
"""

from archlens.shared.constants import EvidenceType


def _node(node_id: str, source_file: str | None = None, node_type: str = "code") -> dict:
    return {"id": node_id, "type": node_type, "source_file": source_file or node_id}


def _edge(
    src: str,
    dst: str,
    relation: str = "calls",
    evidence: EvidenceType = EvidenceType.EXTRACTED,
    confidence: float = 0.95,
    source_file: str | None = None,
) -> dict:
    return {
        "from": src,
        "to": dst,
        "relation": relation,
        "type": evidence.value,
        "confidence": confidence,
        "source_file": source_file or src,
    }


def build_star(n: int = 5) -> dict:
    """Star: center ``n0`` calls ``n-1`` leaves. ``n`` nodes, ``n-1`` edges.

    Hub ``n0`` has total degree ``n-1``; every leaf has total degree 1.
    """
    nodes = [_node(f"n{i}") for i in range(n)]
    edges = [_edge("n0", f"n{i}") for i in range(1, n)]
    return {"nodes": nodes, "edges": edges}


def build_chain(n: int = 4) -> dict:
    """Chain ``n0->n1->...->n{n-1}``. ``n`` nodes, ``n-1`` edges; source ``n0``, sink ``n{n-1}``."""
    nodes = [_node(f"n{i}") for i in range(n)]
    edges = [_edge(f"n{i}", f"n{i + 1}") for i in range(n - 1)]
    return {"nodes": nodes, "edges": edges}


def build_barbell(m: int = 3) -> dict:
    """Two directed ``m``-cycles joined by a single bridge ``a0->b0``.

    ``2*m`` nodes, ``2*m + 1`` edges. The bridge ``a0->b0`` is the only inter-bell edge and
    the only structural bridge in the undirected projection.
    """
    nodes = [_node(f"a{i}") for i in range(m)] + [_node(f"b{i}") for i in range(m)]
    edges = [_edge(f"a{i}", f"a{(i + 1) % m}") for i in range(m)]
    edges += [_edge(f"b{i}", f"b{(i + 1) % m}") for i in range(m)]
    edges.append(_edge("a0", "b0"))
    return {"nodes": nodes, "edges": edges}


def build_two_community() -> dict:
    """Two 3-node communities (cycles) with one connector ``x0->y0``.

    6 nodes, 7 edges. Known partition: ``{x0,x1,x2}`` and ``{y0,y1,y2}``.
    ``x`` nodes live under folder ``pkgx/`` and ``y`` nodes under ``pkgy/``.
    """
    xs = [_node(f"x{i}", f"pkgx/x{i}.py") for i in range(3)]
    ys = [_node(f"y{i}", f"pkgy/y{i}.py") for i in range(3)]
    edges = [_edge(f"x{i}", f"x{(i + 1) % 3}", source_file=f"pkgx/x{i}.py") for i in range(3)]
    edges += [_edge(f"y{i}", f"y{(i + 1) % 3}", source_file=f"pkgy/y{i}.py") for i in range(3)]
    edges.append(_edge("x0", "y0", source_file="pkgx/x0.py"))
    return {"nodes": xs + ys, "edges": edges}


def build_auth_path() -> dict:
    """Login critical path using the critical relations. 4 nodes, 3 edges.

    ``controller -validates-> validator -writes_session-> session_store -checks_policy-> policy``.
    Removing ``session_store`` breaks the only path (a single point of failure).
    """
    nodes = [_node(n, f"src/auth/{n}.py") for n in ("controller", "validator", "session_store", "policy")]
    edges = [
        _edge("controller", "validator", "validates", source_file="src/auth/controller.py"),
        _edge("validator", "session_store", "writes_session", source_file="src/auth/validator.py"),
        _edge("session_store", "policy", "checks_policy", source_file="src/auth/session_store.py"),
    ]
    return {"nodes": nodes, "edges": edges}


def build_healthy_hub() -> dict:
    """Hub ``h`` wired to a 4-cycle of neighbours a-b-c-d. 5 nodes, 8 edges.

    Removing ``h`` leaves a,b,c,d connected with node-disjoint redundancy 2, so ``h`` is a HUB
    (degree 4) whose bypass-path count is 2 — not a single point of failure.
    """
    ring = ["a", "b", "c", "d"]
    nodes = [_node("h"), *[_node(x) for x in ring]]
    edges = [_edge("h", x) for x in ring]
    edges += [_edge(ring[i], ring[(i + 1) % 4]) for i in range(4)]
    return {"nodes": nodes, "edges": edges}


def build_bottleneck() -> dict:
    """``gate`` is the sole link between {l1,l2} and {r1,r2}. 5 nodes, 4 edges.

    Removing ``gate`` splits the graph, so ``gate`` is a BOTTLENECK (degree 4) with bypass count 0.
    """
    nodes = [_node(n) for n in ("l1", "l2", "gate", "r1", "r2")]
    edges = [
        _edge("l1", "gate"),
        _edge("l2", "gate"),
        _edge("gate", "r1"),
        _edge("gate", "r2"),
    ]
    return {"nodes": nodes, "edges": edges}


def build_composite() -> dict:
    """Kitchen-sink graph: a hub, a bottleneck, a duplicate pair, and all three evidence types.

    9 nodes, 8 edges. Evidence mix: 5 EXTRACTED, 2 INFERRED, 1 AMBIGUOUS.
    ``hub`` has in-degree 3 (god node); ``mid`` is the lone hop from ``hub`` to ``sink``.
    ``dupA`` and ``dupB`` are a near-duplicate pair (similarity 0.92).
    """
    ids = ["hub", "c1", "c2", "c3", "mid", "sink", "dupA", "dupB", "PRD"]
    nodes = [_node(i, node_type="doc" if i == "PRD" else "code") for i in ids]
    edges = [
        _edge("c1", "hub"),
        _edge("c2", "hub"),
        _edge("c3", "hub"),
        _edge("hub", "mid"),
        _edge("mid", "sink"),
        _edge("PRD", "hub", "implements", EvidenceType.INFERRED, 0.82),
        _edge("c3", "sink", "uses", EvidenceType.AMBIGUOUS, 0.6),
        _edge("dupA", "dupB", "semantically_similar_to", EvidenceType.INFERRED, 0.92),
    ]
    return {"nodes": nodes, "edges": edges}
