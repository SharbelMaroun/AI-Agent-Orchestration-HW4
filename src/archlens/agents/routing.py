"""Conditional routing function mapping a supervisor decision to a node name (task 10.009)."""

from langgraph.graph import END

from archlens.agents.supervisor import supervise


def route_from_supervisor(state: dict) -> str:
    """Map the supervisor's decision to the next node name, or END to finish the run."""
    decision = supervise(state)["next"]
    return END if decision == "END" else decision
