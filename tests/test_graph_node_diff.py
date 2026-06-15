"""GraphAgent node computes a REAL before/after diff on the post-fix re-graphify (loop closure)."""

import json
from types import SimpleNamespace

from archlens.agents.graph_agent import make_graph_node


def _edge(src, dst):
    return {"from": src, "to": dst, "relation": "calls", "type": "EXTRACTED",
            "confidence": 0.9, "source_file": f"{src}.py"}


def _graph(extra_bridges: int) -> dict:
    # Two triangles {a,b,c} and {d,e,f}; `extra_bridges` cross-edges between them.
    nodes = [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in "abcdef"]
    edges = [_edge("a", "b"), _edge("b", "c"), _edge("c", "a"),
             _edge("d", "e"), _edge("e", "f"), _edge("f", "d")]
    bridges = [_edge("a", "d"), _edge("b", "e"), _edge("c", "f")][:extra_bridges]
    return {"nodes": nodes, "edges": edges + bridges}


def test_post_fix_regraph_computes_modularity_improvement(tmp_path):
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    before.write_text(json.dumps(_graph(3)), encoding="utf-8")   # 3 inter-community bridges
    after.write_text(json.dumps(_graph(1)), encoding="utf-8")    # fix removed 2 bridges

    class _SDK:
        def run_graphify_pipeline(self, repo):
            return SimpleNamespace(graph_json=str(after), node_count=6, edge_count=7)

    state = {"target_repo": {"local_path": str(tmp_path)},
             "graph_snapshot": {"graph_json": str(before), "snapshot_id": 1},
             "findings": [{"status": "fixed"}]}
    diff = make_graph_node(_SDK())(state)["graph_snapshot"]["diff"]
    assert diff["modularity_improved"] is True      # inter-community edges strictly decreased
    assert diff["new_isolates"] is False


def test_first_graph_has_no_diff(tmp_path):
    class _SDK:
        def run_graphify_pipeline(self, repo):
            return SimpleNamespace(graph_json="g.json", node_count=1, edge_count=0)

    out = make_graph_node(_SDK())({"target_repo": {"local_path": str(tmp_path)}})
    assert out["graph_snapshot"]["diff"] == {}      # no prior snapshot, no fix -> no diff
    assert out["graph_snapshot"]["post_fix"] is False
