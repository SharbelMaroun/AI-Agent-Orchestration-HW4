"""BugHunterAgent node — emit evidence-ladder findings, and have the LLM validate the top one.

Every finding is a valid EvidenceFinding. The worst bottleneck is additionally escalated to a
``VALIDATED`` finding carrying the LLM's architectural review — that is what hands a concrete
target to RefactorAgent in the improvement loop (task 10.020). The LLM is reached only via the
SDK, so this agent never imports a client.
"""

from ..agents import prompt_loader
from ..agents.evidence import EvidenceFinding
from ..shared.constants import EXTRACTED_CONFIDENCE

# System prompt loaded by id+version from the prompt book — no inline literal (PRD §9 / FR-AO-13).
_PROMPT = "bughunter"
_ARCHITECT_SYSTEM = prompt_loader.system_prompt(_PROMPT)
_PID = prompt_loader.prompt_id(_PROMPT)
_PVER = prompt_loader.version_of(_PROMPT)


def _finding(finding_id: str, category: str, source_file: str, relation: str,
             level: str = "EXTRACTED", confidence: float = EXTRACTED_CONFIDENCE, **extra) -> dict:
    evidence = EvidenceFinding(id=finding_id, category=category, level=level,
                               relation=relation, confidence=confidence, source_file=source_file)
    return {**evidence.model_dump(), "from": "bughunter", "status": "open", **extra}


def _spof_confidence(spof) -> float:
    """The weakest-link confidence along the SPOF's real per-hop citation chain (not a fixed 0.95)."""
    return min((getattr(c, "confidence", EXTRACTED_CONFIDENCE) for c in spof.citations),
               default=EXTRACTED_CONFIDENCE)


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
    review = sdk.ask_llm(prompt, system=_ARCHITECT_SYSTEM, agent="BugHunterAgent", max_tokens=500,
                         prompt_id=_PID, prompt_version=_PVER)
    return _finding(f"validated-{top.node_id}", "god_node", top.source_file, "betweenness",
                    level="VALIDATED", text=review)


def make_bughunter_node(sdk):
    """Factory: bind the SDK and return the bughunter node enforcing the evidence contract."""

    def bughunter_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        findings: list[dict] = []
        for spof in sdk.single_points_of_failure(graph):
            location = spof.citations[0].source_file if spof.citations else spof.node_id
            findings.append(_finding(f"spof-{spof.node_id}", "SPOF", location, "critical_path",
                                     confidence=_spof_confidence(spof)))
        verdicts = sdk.classify_nodes(graph)
        bottlenecks = [v for v in verdicts if v.verdict == "BOTTLENECK"]
        for verdict in bottlenecks:
            findings.append(_finding(f"god-{verdict.node_id}", "god_node",
                                     verdict.source_file, "betweenness"))
        for verdict in verdicts:
            if verdict.verdict != "BOTTLENECK":  # a healthy hub is an OBSERVED fact, not actionable
                findings.append(_finding(f"hub-{verdict.node_id}", "hub", verdict.source_file,
                                         "betweenness", level="OBSERVED"))
        if bottlenecks:
            findings.append(_validate_top(sdk, bottlenecks[0], graph))
        return {"findings": findings}

    return bughunter_node
