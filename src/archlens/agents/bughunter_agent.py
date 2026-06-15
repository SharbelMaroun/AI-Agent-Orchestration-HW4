"""BugHunterAgent node — emit evidence-ladder findings, and have the LLM validate the top one.

Every finding is a valid EvidenceFinding. The worst bottleneck is additionally escalated to a
``VALIDATED`` finding carrying the LLM's architectural review — that is what hands a concrete
target to RefactorAgent in the improvement loop (task 10.020). The LLM is reached only via the
SDK, so this agent never imports a client.
"""

from ..agents.evidence import EvidenceFinding
from ..agents.source_reader import read_source_excerpt

_ARCHITECT_SYSTEM = (
    "You are a senior software architect reverse-engineering an unfamiliar Python codebase from its "
    "dependency graph plus the actual source. Be concrete and specific: name the real architectural "
    "risks (high coupling, single points of failure, god objects, hidden dependencies) and the "
    "exact behaviour-preserving refactor that relieves them. No filler.")


def _finding(finding_id: str, category: str, source_file: str, relation: str,
             level: str = "EXTRACTED", **extra) -> dict:
    evidence = EvidenceFinding(id=finding_id, category=category, level=level,
                               relation=relation, confidence=0.95, source_file=source_file)
    return {**evidence.model_dump(), "from": "bughunter", "status": "open", **extra}


def _validate_top(sdk, top, repo_path: str) -> dict:
    """LLM reverse-engineers the worst bottleneck FROM ITS REAL SOURCE; escalate to a VALIDATED target."""
    code = read_source_excerpt(repo_path, top.source_file)
    body = f"\n\nIts source:\n```python\n{code}\n```" if code else " (source not available)."
    prompt = (
        f"'{top.node_id}' in {top.source_file} is the highest-betweenness bottleneck — many paths "
        f"route through it.{body}\n\nIn 3-4 sentences: what is the concrete architectural problem, "
        "and what specific behaviour-preserving refactor would relieve it?")
    review = sdk.ask_llm(prompt, system=_ARCHITECT_SYSTEM, agent="BugHunterAgent", max_tokens=600)
    return _finding(f"validated-{top.node_id}", "god_node", top.source_file, "betweenness",
                    level="VALIDATED", text=review)


def make_bughunter_node(sdk):
    """Factory: bind the SDK and return the bughunter node enforcing the evidence contract."""

    def bughunter_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        repo_path = (state.get("target_repo") or {}).get("local_path", "")
        findings: list[dict] = []
        for spof in sdk.single_points_of_failure(graph):
            location = spof.citations[0].source_file if spof.citations else spof.node_id
            findings.append(_finding(f"spof-{spof.node_id}", "SPOF", location, "critical_path"))
        bottlenecks = [v for v in sdk.classify_nodes(graph) if v.verdict == "BOTTLENECK"]
        for verdict in bottlenecks:
            findings.append(_finding(f"god-{verdict.node_id}", "god_node",
                                     verdict.source_file, "betweenness"))
        if bottlenecks:
            findings.append(_validate_top(sdk, bottlenecks[0], repo_path))
        return {"findings": findings}

    return bughunter_node
