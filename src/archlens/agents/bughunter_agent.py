"""BugHunterAgent node — emit evidence-ladder findings, and have the LLM validate the top one.

Every finding is a valid EvidenceFinding. The worst bottleneck is additionally escalated to a
``VALIDATED`` finding carrying the LLM's architectural review — that is what hands a concrete
target to RefactorAgent in the improvement loop (task 10.020). The LLM is reached only via the
SDK, so this agent never imports a client.
"""

from ..agents.evidence import EvidenceFinding

_ARCHITECT_SYSTEM = (
    "You are a senior software architect reverse-engineering an unfamiliar codebase from its "
    "dependency GRAPH (not its source). Reason from graph structure — degree, who depends on whom, "
    "communities — to name the real architectural risks (coupling, single points of failure, god "
    "objects) and the refactor that relieves them. Be concrete and brief; no filler.")


def _finding(finding_id: str, category: str, source_file: str, relation: str,
             level: str = "EXTRACTED", **extra) -> dict:
    evidence = EvidenceFinding(id=finding_id, category=category, level=level,
                               relation=relation, confidence=0.95, source_file=source_file)
    return {**evidence.model_dump(), "from": "bughunter", "status": "open", **extra}


def _graph_context(graph, node_id: str) -> str:
    """A compact textual view of the node's GRAPH neighbourhood — the LLM reasons from this, not code."""
    if not hasattr(graph, "predecessors") or node_id not in graph:
        return f"'{node_id}' is the highest-betweenness bottleneck (many graph paths route through it)."
    callers = sorted(graph.predecessors(node_id))[:15]
    uses = sorted(graph.successors(node_id))[:15]
    return (f"'{node_id}' has in-degree {graph.in_degree(node_id)} and out-degree "
            f"{graph.out_degree(node_id)}. Nodes that depend on it (callers): {callers}. "
            f"It depends on: {uses}.")


def _validate_top(sdk, top, graph) -> dict:
    """LLM judges the worst bottleneck FROM THE GRAPH neighbourhood; escalate to a VALIDATED target."""
    prompt = (
        f"{_graph_context(graph, top.node_id)}\n\nReasoning only from this graph structure, in 3-4 "
        "sentences: what architectural problem does this indicate (coupling, single point of "
        "failure, god object), and what refactor would relieve it?")
    review = sdk.ask_llm(prompt, system=_ARCHITECT_SYSTEM, agent="BugHunterAgent", max_tokens=500)
    return _finding(f"validated-{top.node_id}", "god_node", top.source_file, "betweenness",
                    level="VALIDATED", text=review)


def make_bughunter_node(sdk):
    """Factory: bind the SDK and return the bughunter node enforcing the evidence contract."""

    def bughunter_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        findings: list[dict] = []
        for spof in sdk.single_points_of_failure(graph):
            location = spof.citations[0].source_file if spof.citations else spof.node_id
            findings.append(_finding(f"spof-{spof.node_id}", "SPOF", location, "critical_path"))
        bottlenecks = [v for v in sdk.classify_nodes(graph) if v.verdict == "BOTTLENECK"]
        for verdict in bottlenecks:
            findings.append(_finding(f"god-{verdict.node_id}", "god_node",
                                     verdict.source_file, "betweenness"))
        if bottlenecks:
            findings.append(_validate_top(sdk, bottlenecks[0], graph))
        return {"findings": findings}

    return bughunter_node
