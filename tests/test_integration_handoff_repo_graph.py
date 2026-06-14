"""Integration: supervisor -> RepoAgent -> GraphAgent handoff in mock mode (task 10.048)."""

from archlens.agents.runner import make_runner


def test_repo_graph_handoff_payloads(tmp_path, mock_sdk, blocked_sockets):
    graph = make_runner(mock_sdk, db_path=str(tmp_path / "h.sqlite"), interrupt_after=["GraphAgent"])
    config = {"configurable": {"thread_id": "h1"}}
    graph.invoke({}, config)
    state = graph.get_state(config).values
    assert state["target_repo"]["validated"] is True
    assert {"graph_json", "node_count", "edge_count", "snapshot_id"} <= set(state["graph_snapshot"])
