"""Human-in-the-loop approval interrupt for irreversible actions (tasks 10.037-10.038)."""

from langgraph.types import interrupt

from archlens.agents.guardrails import requires_approval


def make_approval_node():
    """Return a node that pauses on a pending irreversible approval and records the decision."""

    def approval_node(state: dict) -> dict:
        pending = [a for a in (state.get("approvals") or [])
                   if a.get("status") == "pending" and requires_approval(a.get("action", ""))]
        if not pending:
            return {}
        request = pending[-1]
        decision = interrupt({"approval_request": request}) or {}
        return {"approvals": [{
            **request,
            "status": decision.get("status", "denied"),
            "approver": decision.get("approver"),
            "timestamp": decision.get("timestamp"),
        }]}

    return approval_node
