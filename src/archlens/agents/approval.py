"""Human-in-the-loop approval gate for irreversible actions (tasks 10.037-10.038).

The shipped HITL mechanism is a DYNAMIC ``langgraph.types.interrupt()`` raised inside this node — the
supervisor routes here whenever an approval is pending — not a static ``interrupt_before`` edge. An
interactive run suspends at the interrupt for a human decision (see tests/test_approval_interrupt.py)
and resumes via ``Command(resume=...)``. An autonomous run (``auto_approve=True``, used by the
headless improvement loop) records an explicit policy grant instead of pausing, so the loop can make
progress — but EVERY applied refactor still carries a recorded ``granted`` approval, satisfying the
"no source modification without a recorded decision" governance rule.
"""

from langgraph.types import interrupt

from ..agents.guardrails import requires_approval

_AUTO_APPROVER = "auto-approval-policy"


def _unresolved_pending(state: dict) -> list[dict]:
    """Approval requests whose LATEST recorded status is still ``pending``.

    ``approvals`` is an append reducer, so a granted request keeps its earlier ``pending`` record;
    collapsing to the last record per finding stops a resolved request from re-firing the gate.
    """
    latest: dict = {}
    for a in (state.get("approvals") or []):
        latest[a.get("finding")] = a
    return [a for a in latest.values()
            if a.get("status") == "pending" and requires_approval(a.get("action", ""))]


def make_approval_node(auto_approve: bool = False):
    """Return the approval gate node. ``auto_approve`` records a policy grant instead of pausing."""

    def approval_node(state: dict) -> dict:
        pending = _unresolved_pending(state)
        if not pending:
            return {}
        request = pending[-1]
        if auto_approve:
            decision = {"status": "granted", "approver": _AUTO_APPROVER, "timestamp": "auto"}
        else:
            decision = interrupt({"approval_request": request}) or {}
        return {"approvals": [{
            **request,
            "status": decision.get("status", "denied"),
            "approver": decision.get("approver"),
            "timestamp": decision.get("timestamp"),
        }]}

    return approval_node
