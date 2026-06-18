"""Supervisor node: inspect AgentState and decide the next agent (task 10.008)."""

from ..shared.constants import MAX_LOOP_ITERATIONS


def _decision(node: str, reason: str) -> dict:
    return {"next": node, "reason": reason}


def _findings(state: dict) -> list:
    return state.get("findings") or []


def _bug_findings(state: dict) -> list:
    return [f for f in _findings(state) if f.get("from") == "bughunter"]


def _open_validated(state: dict) -> list:
    # Exclude findings already picked up by RefactorAgent (the append reducer keeps the original
    # "open" record around), so each validated bug is routed to a refactor exactly once.
    handled = {f.get("id") for f in _findings(state) if f.get("status") in ("selected", "fixed")}
    return [f for f in _bug_findings(state)
            if f.get("level") == "VALIDATED" and f.get("status") == "open"
            and f.get("id") not in handled]


def _pending_approval(state: dict) -> bool:
    return any(a.get("status") == "pending" for a in (state.get("approvals") or []))


def supervise(state: dict) -> dict:
    """Return the next-agent decision plus a reason string from the current state."""
    if state.get("loop_iteration", 0) >= MAX_LOOP_ITERATIONS:
        return _decision("END", "hard cap of 5 iterations reached")
    stop = state.get("stop_eval") or {}
    if stop.get("met") is True:
        return _decision("END", "stop conditions met")
    if _pending_approval(state):  # an irreversible action awaits human sign-off (Part B guardrails)
        return _decision("ApprovalAgent", "pending approval: human sign-off required")
    if not state.get("target_repo"):
        return _decision("RepoAgent", "initial: clone the target repo")
    if not state.get("graph_snapshot"):
        return _decision("GraphAgent", "repo validated: build the graph")
    if not _findings(state):
        return _decision("AnalystAgent", "graph ready: run analysis")
    if not _bug_findings(state):
        return _decision("BugHunterAgent", "analysis done: hunt bugs with evidence")
    if _open_validated(state):
        return _decision("RefactorAgent", "validated bug: plan and apply a fix")
    if any(f.get("status") == "fixed" for f in _findings(state)) \
            and not state["graph_snapshot"].get("post_fix"):
        return _decision("GraphAgent", "patch applied: re-run the graph")
    if "tests_green" not in stop:
        return _decision("QAAgent", "graph refreshed: run QA")
    if not state.get("token_ledger"):
        return _decision("MetricsAgent", "QA done: aggregate token metrics")
    return _decision("stop_eval", "metrics done: evaluate the stop conditions")
