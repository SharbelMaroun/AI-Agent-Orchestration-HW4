"""BugHunterAgent node — emit evidence-ladder findings, and have the LLM validate the top one.

Every finding is a valid EvidenceFinding. The worst bottleneck is additionally escalated to a
``VALIDATED`` finding carrying the LLM's architectural review — that is what hands a concrete
target to RefactorAgent in the improvement loop (task 10.020). The LLM is reached only via the
SDK, so this agent never imports a client.
"""

from ..agents.evidence import EvidenceFinding


def _finding(finding_id: str, category: str, source_file: str, relation: str,
             level: str = "EXTRACTED", **extra) -> dict:
    evidence = EvidenceFinding(id=finding_id, category=category, level=level,
                               relation=relation, confidence=0.95, source_file=source_file)
    return {**evidence.model_dump(), "from": "bughunter", "status": "open", **extra}


def _validate_top(sdk, top) -> dict:
    """Ask the LLM to review the worst bottleneck, escalated to a VALIDATED refactor target."""
    review = sdk.ask_llm(
        f"As a software architect, in one sentence assess whether '{top.node_id}' "
        f"({top.source_file}) is a genuine architectural bottleneck worth refactoring.",
        agent="BugHunterAgent")
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
            findings.append(_validate_top(sdk, bottlenecks[0]))
        return {"findings": findings}

    return bughunter_node
