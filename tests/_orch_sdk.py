"""Test SDK: ArchLensSDK with canned granular methods for orchestration tests."""

from pathlib import Path
from types import SimpleNamespace

from archlens.sdk.sdk import ArchLensSDK


class OrchSDK(ArchLensSDK):
    """ArchLensSDK whose granular methods are canned so the orchestration runs without I/O."""

    def clone_target_repo(self, run_id, use_fallback=False):
        return Path("/clone")

    def validate_repo(self, path, use_fallback=False):
        return SimpleNamespace(passed=True)

    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(graph_json="g.json", node_count=10, edge_count=8, report_md="R.md")

    def load_analysis_graph(self, source):
        return "G"

    def density_communities(self, graph):
        return [{"a"}, {"b"}]

    def node_centrality(self, graph):
        return [SimpleNamespace(node_id="hub", degree_total=4, betweenness=0.5)]

    def classify_nodes(self, graph):
        return [SimpleNamespace(node_id="gate", verdict="BOTTLENECK", source_file="gate.py")]

    def triage_edges(self, graph):
        return {"EXTRACTED": [1], "INFERRED": [], "AMBIGUOUS": []}

    def single_points_of_failure(self, graph):
        return [SimpleNamespace(node_id="ss", citations=[SimpleNamespace(source_file="ss.py")])]

    def run_quality_gates(self, repo_path=None):
        return SimpleNamespace(tests_green=True, coverage_pct=97.0, ruff_violations=0)

    def token_usage(self):
        return {"baseline": 100, "assisted": 30, "rows": [{"model": "x"}]}

    def ask_llm(self, prompt, *, agent="orchestrator", max_tokens=512):
        return "canned llm reply"
