"""Compile the multi-agent orchestration StateGraph (task 10.011)."""

from langgraph.graph import END, START, StateGraph

from archlens.agents.analyst_agent import make_analyst_node
from archlens.agents.bughunter_agent import make_bughunter_node
from archlens.agents.graph_agent import make_graph_node
from archlens.agents.metrics_agent import make_metrics_node
from archlens.agents.qa_agent import make_qa_node
from archlens.agents.refactor_agent import make_refactor_node
from archlens.agents.repo_agent import make_repo_node
from archlens.agents.routing import route_from_supervisor
from archlens.agents.state import AgentState
from archlens.agents.stop_eval import make_stop_eval_node

_AGENTS = {
    "RepoAgent": make_repo_node,
    "GraphAgent": make_graph_node,
    "AnalystAgent": make_analyst_node,
    "BugHunterAgent": make_bughunter_node,
    "RefactorAgent": make_refactor_node,
    "QAAgent": make_qa_node,
    "MetricsAgent": make_metrics_node,
}


def _supervisor(state: dict) -> dict:
    """Routing hub node: the conditional edge reads the decision; no state mutation here."""
    return {}


def build_orchestration_graph(sdk):
    """Build and compile the StateGraph: supervisor hub plus the 7 agent nodes."""
    builder = StateGraph(AgentState)
    builder.add_node("supervisor", _supervisor)
    for name, factory in _AGENTS.items():
        builder.add_node(name, factory(sdk))
    builder.add_node("stop_eval", make_stop_eval_node(sdk))
    builder.add_edge(START, "supervisor")
    mapping = {name: name for name in _AGENTS}
    mapping["stop_eval"] = "stop_eval"
    mapping[END] = END
    builder.add_conditional_edges("supervisor", route_from_supervisor, mapping)
    for name in (*_AGENTS, "stop_eval"):
        builder.add_edge(name, "supervisor")
    return builder.compile()
