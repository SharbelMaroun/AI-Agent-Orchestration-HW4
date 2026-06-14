"""TDD tests for the BugHunterAgent orchestration node (tasks 10.019-10.020)."""

from types import SimpleNamespace

from archlens.agents.bughunter_agent import make_bughunter_node
from archlens.agents.evidence import EvidenceFinding


class _SDK:
    def load_analysis_graph(self, source):
        return "G"

    def single_points_of_failure(self, graph):
        return [SimpleNamespace(node_id="ss", citations=[SimpleNamespace(source_file="ss.py")])]

    def classify_nodes(self, graph):
        return [SimpleNamespace(node_id="gate", verdict="BOTTLENECK", source_file="gate.py")]


def _findings():
    return make_bughunter_node(_SDK())({"graph_snapshot": {"graph_json": "g.json"}})["findings"]


def test_bughunter_emits_only_valid_evidence_findings():
    findings = _findings()
    assert findings
    for f in findings:
        EvidenceFinding(id=f["id"], category=f["category"], level=f["level"],
                        relation=f["relation"], confidence=f["confidence"], source_file=f["source_file"])


def test_bughunter_reports_spof_and_god_node():
    categories = {f["category"] for f in _findings()}
    assert "SPOF" in categories
    assert "god_node" in categories
