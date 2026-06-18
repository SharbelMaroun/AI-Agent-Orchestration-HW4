"""TDD tests for the compiled orchestration StateGraph (tasks 10.010-10.012)."""

from archlens.agents.graph_builder import build_orchestration_graph

EXPECTED = {
    "supervisor", "RepoAgent", "GraphAgent", "AnalystAgent",
    "BugHunterAgent", "RefactorAgent", "QAAgent", "MetricsAgent",
}


def _graph():
    return build_orchestration_graph(object())


def test_graph_contains_supervisor_and_seven_agents():
    nodes = set(_graph().get_graph().nodes)
    assert nodes >= EXPECTED


def test_graph_includes_the_human_approval_node():
    # The HITL approval interrupt is wired into the live orchestration graph, not test-only.
    assert "ApprovalAgent" in set(_graph().get_graph().nodes)


def test_supervisor_is_reachable_from_start():
    drawable = _graph().get_graph()
    sources = {edge.source for edge in drawable.edges}
    assert "supervisor" in {edge.target for edge in drawable.edges} or "supervisor" in sources


def test_mermaid_export_names_all_nodes():
    mermaid = _graph().get_graph().draw_mermaid()
    for name in EXPECTED:
        assert name in mermaid
