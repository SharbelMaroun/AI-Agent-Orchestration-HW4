"""Shared LangGraph orchestration state with per-key reducers (task 10.002).

Field names are normative (PRD_agent_orchestration §3.2). ``findings`` and ``approvals`` use
an append reducer (records are immutable and accumulate); all other fields are last-write-wins.
"""

from typing import Annotated, TypedDict


def append_records(existing: list | None, new: list | None) -> list:
    """Append reducer: accumulate immutable records across node updates."""
    return list(existing or []) + list(new or [])


class AgentState(TypedDict, total=False):
    """The single shared state passed between the supervisor and agent nodes."""

    target_repo: dict
    graph_snapshot: dict
    findings: Annotated[list[dict], append_records]
    loop_iteration: int
    stop_eval: dict
    token_ledger: dict
    approvals: Annotated[list[dict], append_records]
