"""Integration: Analyst -> BugHunter -> Refactor chain in mock mode (task 10.049)."""

from archlens.agents.evidence import EvidenceFinding
from archlens.agents.guardrails import ActionTier, classify_action
from archlens.agents.runner import make_runner


def test_analysis_chain_enforces_evidence_and_guardrails(tmp_path, mock_sdk, blocked_sockets):
    graph = make_runner(mock_sdk, db_path=str(tmp_path / "a.sqlite"),
                        interrupt_after=["BugHunterAgent"])
    config = {"configurable": {"thread_id": "a1"}}
    graph.invoke({}, config)
    findings = graph.get_state(config).values["findings"]

    bug_findings = [f for f in findings if f.get("from") == "bughunter"]
    assert bug_findings
    for f in bug_findings:
        EvidenceFinding(id=f["id"], category=f["category"], level=f["level"],
                        relation=f["relation"], confidence=f["confidence"], source_file=f["source_file"])

    assert classify_action("split_module in file") is ActionTier.REVERSIBLE
