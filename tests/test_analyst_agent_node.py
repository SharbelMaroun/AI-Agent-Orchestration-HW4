"""TDD tests for the AnalystAgent orchestration node (tasks 10.017-10.018)."""

from types import SimpleNamespace

from archlens.agents.analyst_agent import make_analyst_node


class _SDK:
    def load_analysis_graph(self, source):
        return "G"

    def density_communities(self, graph):
        return [{"a"}, {"b"}]

    def node_centrality(self, graph):
        return [SimpleNamespace(node_id="hub", degree_total=4, betweenness=0.5)]

    def classify_nodes(self, graph):
        return [SimpleNamespace(node_id="gate", verdict="BOTTLENECK")]

    def triage_edges(self, graph):
        return {"EXTRACTED": [1, 2], "INFERRED": [], "AMBIGUOUS": [1]}


def _findings():
    return make_analyst_node(_SDK())({"graph_snapshot": {"graph_json": "g.json"}})["findings"]


def test_analyst_emits_expected_categories():
    categories = {f["category"] for f in _findings()}
    assert {"centrality", "hub_vs_bottleneck", "triage", "community_count"} <= categories


def test_analyst_findings_are_tagged_from_analyst():
    assert all(f["from"] == "analyst" for f in _findings())
