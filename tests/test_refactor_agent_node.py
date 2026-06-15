"""TDD tests for the RefactorAgent orchestration node (tasks 10.021-10.022)."""

from archlens.agents.refactor_agent import make_refactor_node


class _SDK:
    def __init__(self):
        self.writes = 0

    def apply_patch(self, *args, **kwargs):
        self.writes += 1

    def ask_llm(self, prompt, *, agent="orchestrator", max_tokens=512):
        return "extract the request-routing helper into its own module"


def _validated_bug():
    return {"from": "bughunter", "level": "VALIDATED", "status": "open", "category": "SPOF",
            "source_file": "ss.py", "id": "spof-ss", "relation": "critical_path", "confidence": 0.95}


def test_refactor_plans_the_top_validated_finding():
    out = make_refactor_node(_SDK())({"findings": [_validated_bug()]})
    update = out["findings"][0]
    assert update["status"] == "selected"
    assert update["plan"]["target"] == "ss.py"
    assert update["plan"]["action"]


def test_refactor_produces_plan_without_writing():
    sdk = _SDK()
    make_refactor_node(sdk)({"findings": [_validated_bug()]})
    assert sdk.writes == 0


def test_refactor_is_noop_without_a_validated_finding():
    assert make_refactor_node(_SDK())({"findings": []}) == {}


def test_refactor_rationale_is_authored_by_the_llm():
    out = make_refactor_node(_SDK())({"findings": [_validated_bug()]})
    assert out["findings"][0]["plan"]["rationale"].startswith("extract the request-routing")
