"""TDD tests for the human-approval interrupt and resume (tasks 10.036-10.038)."""

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from archlens.agents.approval import make_approval_node
from archlens.agents.runner import make_checkpointer
from archlens.agents.state import AgentState

_PENDING = [{"action": "git push --force", "finding": "spof-ss", "status": "pending"}]


def _graph(tmp_path, thread):
    builder = StateGraph(AgentState)
    builder.add_node("approval", make_approval_node())
    builder.add_edge(START, "approval")
    builder.add_edge("approval", END)
    saver = make_checkpointer(str(tmp_path / f"{thread}.sqlite"))
    graph = builder.compile(checkpointer=saver)
    return graph, {"configurable": {"thread_id": thread}}


def test_pause_on_irreversible_action(tmp_path):
    graph, config = _graph(tmp_path, "pause")
    graph.invoke({"approvals": _PENDING}, config)
    assert graph.get_state(config).next  # graph halted at the interrupt


def test_approve_path_records_decision(tmp_path):
    graph, config = _graph(tmp_path, "approve")
    graph.invoke({"approvals": _PENDING}, config)
    graph.invoke(Command(resume={"status": "granted", "approver": "lecturer", "timestamp": "t0"}), config)
    final = graph.get_state(config).values["approvals"][-1]
    assert final["status"] == "granted"
    assert final["approver"] == "lecturer"


def test_reject_path_blocks_the_write(tmp_path):
    graph, config = _graph(tmp_path, "reject")
    graph.invoke({"approvals": _PENDING}, config)
    graph.invoke(Command(resume={"status": "denied", "approver": "lecturer", "timestamp": "t0"}), config)
    assert graph.get_state(config).values["approvals"][-1]["status"] == "denied"
