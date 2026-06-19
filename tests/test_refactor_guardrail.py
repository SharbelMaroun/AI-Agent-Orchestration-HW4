"""Guardrail invariant (PRD_agent_orchestration §11.1 / acceptance §12.4).

RefactorAgent must never execute a source modification without a granted approval, and every
applied refactor must carry a matching recorded grant in ``state.approvals``. These run the REAL
compiled orchestration StateGraph end-to-end (only the granular SDK I/O is canned).
"""

from _orch_sdk import OrchSDK

from archlens.agents.runner import make_runner


class _TrackSDK(OrchSDK):
    """OrchSDK that records every apply_fix call so we can prove the writer is gated."""

    def __init__(self):
        super().__init__()
        self.apply_calls: list = []

    def apply_fix(self, finding, repo_path, graph_json=None):
        self.apply_calls.append(finding.get("id"))
        return True


def _run(sdk, tmp_path, *, auto_approve, thread):
    graph = make_runner(sdk, db_path=str(tmp_path / f"{thread}.sqlite"), auto_approve=auto_approve)
    config = {"configurable": {"thread_id": thread}, "recursion_limit": 150}
    graph.invoke({}, config)
    return graph, config


def test_refactor_pauses_for_human_approval_before_any_write(tmp_path):
    # Default (interactive) mode: the graph must HALT at the HITL interrupt before any source write.
    sdk = _TrackSDK()
    graph, config = _run(sdk, tmp_path, auto_approve=False, thread="hitl")
    state = graph.get_state(config)
    assert state.next  # graph suspended at the approval interrupt
    assert sdk.apply_calls == []  # no source modification before a human decision
    assert any(a.get("status") == "pending" for a in state.values.get("approvals", []))


def test_every_applied_refactor_carries_a_recorded_grant(tmp_path):
    # Autonomous mode: fixes apply, but only AFTER the ApprovalAgent records a granted decision.
    sdk = _TrackSDK()
    graph, config = _run(sdk, tmp_path, auto_approve=True, thread="auto")
    values = graph.get_state(config).values
    granted = {a.get("finding") for a in values.get("approvals", []) if a.get("status") == "granted"}
    fixed_ids = {f.get("id") for f in values.get("findings", []) if f.get("status") == "fixed"}
    assert sdk.apply_calls  # the loop did apply at least one fix
    assert fixed_ids and fixed_ids <= granted  # §12.4: every applied refactor has a granted approval
