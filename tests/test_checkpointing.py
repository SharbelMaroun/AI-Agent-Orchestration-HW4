"""TDD tests for SqliteSaver checkpointing and interrupted-resume (tasks 10.030-10.032)."""

from pathlib import Path
from types import SimpleNamespace

from archlens.agents.runner import make_checkpointer, make_runner, resume_run


class _MockSDK:
    def clone_target_repo(self, run_id, use_fallback=False):
        return Path("/clone")

    def validate_repo(self, path, use_fallback=False):
        return SimpleNamespace(passed=True)

    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(graph_json="g.json", node_count=10, edge_count=8, report_md="R.md")

    def load_analysis_graph(self, source):
        return "G"

    def density_communities(self, graph):
        return [{"a"}]

    def node_centrality(self, graph):
        return [SimpleNamespace(node_id="hub", degree_total=4, betweenness=0.5)]

    def classify_nodes(self, graph):
        return [SimpleNamespace(node_id="gate", verdict="BOTTLENECK", source_file="gate.py")]

    def triage_edges(self, graph):
        return {"EXTRACTED": [1], "INFERRED": [], "AMBIGUOUS": []}

    def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512):
        return "canned llm reply"


def test_saver_uses_the_configured_db_path(tmp_path):
    saver = make_checkpointer(str(tmp_path / "db.sqlite"))
    assert saver is not None


def test_interrupt_after_graph_resumes_at_analyst_with_restored_state(tmp_path):
    graph = make_runner(_MockSDK(), db_path=str(tmp_path / "ck.sqlite"),
                        interrupt_after=["GraphAgent", "AnalystAgent"])
    config = {"configurable": {"thread_id": "t1"}}
    graph.invoke({}, config)

    paused = graph.get_state(config).values
    assert "graph_snapshot" in paused
    assert not paused.get("findings")
    snapshot_before = paused["graph_snapshot"]

    resume_run(graph, "t1")
    resumed = graph.get_state(config).values
    assert resumed.get("findings")
    assert resumed["graph_snapshot"] == snapshot_before
