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

    def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512, **kwargs):
        return "the gate node funnels every request — a real bottleneck"


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


def test_bughunter_escalates_the_top_bottleneck_to_a_validated_llm_review():
    validated = [f for f in _findings() if f["level"] == "VALIDATED"]
    assert len(validated) == 1                       # exactly one refactor target
    assert validated[0]["status"] == "open"
    assert validated[0]["text"].startswith("the gate node")  # the LLM's review is attached


def test_spof_finding_carries_real_citation_confidence_not_a_fixed_0_95():
    class _Conf(_SDK):
        def single_points_of_failure(self, graph):
            return [SimpleNamespace(node_id="ss", citations=[
                SimpleNamespace(source_file="ss.py", confidence=0.7),
                SimpleNamespace(source_file="ss.py", confidence=0.9)])]

        def classify_nodes(self, graph):
            return []  # isolate the SPOF finding (no god-node escalation)

    findings = make_bughunter_node(_Conf())({"graph_snapshot": {"graph_json": "g.json"}})["findings"]
    spof = next(f for f in findings if f["category"] == "SPOF")
    assert spof["confidence"] == 0.7  # weakest hop of the real citation chain, not hardcoded 0.95


def test_healthy_hubs_are_emitted_as_observed_findings():
    class _Hub(_SDK):
        def classify_nodes(self, graph):
            return [SimpleNamespace(node_id="util", verdict="HUB", source_file="util.py")]

    findings = make_bughunter_node(_Hub())({"graph_snapshot": {"graph_json": "g.json"}})["findings"]
    hub = next(f for f in findings if f["category"] == "hub")
    assert hub["level"] == "OBSERVED"  # the bottom rung of the evidence ladder is now genuinely used
    assert not [f for f in findings if f["level"] == "VALIDATED"]  # a healthy hub is not escalated
