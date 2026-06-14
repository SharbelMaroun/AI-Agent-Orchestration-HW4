"""TDD tests for the GraphAgent orchestration node (tasks 10.015-10.016)."""

import json
from types import SimpleNamespace

from archlens.agents.graph_agent import make_graph_node


class _SDK:
    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(graph_json="g.json", node_count=10, edge_count=8, report_md="R.md")


class _ManifestSDK:
    """Mirrors the real SDK: returns a manifest with no graph_json/count attributes."""

    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(run_id="r1")


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


def test_resolves_real_graphify_output_path_and_counts(tmp_path):
    # With no count attrs on the manifest, the node points at <repo>/graphify-out/graph.json
    # and derives node/edge counts by reading the file Graphify actually wrote.
    out = tmp_path / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(
        json.dumps({"nodes": [{"id": "a"}, {"id": "b"}], "links": [{"source": "a", "target": "b"}]}),
        encoding="utf-8")
    snap = make_graph_node(_ManifestSDK())(
        {"target_repo": {"local_path": str(tmp_path)}})["graph_snapshot"]
    assert snap["graph_json"] == str(out / "graph.json")
    assert (snap["node_count"], snap["edge_count"]) == (2, 1)
    assert snap["report_md"].endswith("GRAPH_REPORT.md")
