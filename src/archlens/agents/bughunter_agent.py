"""BugHunterAgent node — emit only evidence-ladder findings via the SDK (task 10.020)."""

from ..agents.evidence import EvidenceFinding


def _finding(finding_id: str, category: str, source_file: str, relation: str) -> dict:
    evidence = EvidenceFinding(id=finding_id, category=category, level="EXTRACTED",
                               relation=relation, confidence=0.95, source_file=source_file)
    return {**evidence.model_dump(), "from": "bughunter", "status": "open"}


def make_bughunter_node(sdk):
    """Factory: bind the SDK and return the bughunter node enforcing the evidence contract."""

    def bughunter_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        findings: list[dict] = []
        for spof in sdk.single_points_of_failure(graph):
            location = spof.citations[0].source_file if spof.citations else spof.node_id
            findings.append(_finding(f"spof-{spof.node_id}", "SPOF", location, "critical_path"))
        for verdict in sdk.classify_nodes(graph):
            if verdict.verdict == "BOTTLENECK":
                findings.append(_finding(f"god-{verdict.node_id}", "god_node",
                                         verdict.source_file, "betweenness"))
        return {"findings": findings}

    return bughunter_node
