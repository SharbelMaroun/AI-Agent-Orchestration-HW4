"""TDD tests for the GraphAgent orchestration node (tasks 10.015-10.016)."""

from types import SimpleNamespace

from archlens.agents.graph_agent import make_graph_node


class _SDK:
    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(graph_json="g.json", node_count=10, edge_count=8, report_md="R.md")


def test_graph_node_stores_snapshot():
    out = make_graph_node(_SDK())({"target_repo": {"local_path": "/x"}})
    snap = out["graph_snapshot"]
    assert snap["graph_json"] == "g.json"
    assert (snap["node_count"], snap["edge_count"]) == (10, 8)
    assert snap["report_md"] == "R.md"
    assert snap["snapshot_id"] == 1


def test_snapshot_id_increments_per_run():
    state = {"target_repo": {"local_path": "/x"}, "graph_snapshot": {"snapshot_id": 2}}
    assert make_graph_node(_SDK())(state)["graph_snapshot"]["snapshot_id"] == 3
