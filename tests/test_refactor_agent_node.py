"""TDD tests for the RefactorAgent orchestration node (tasks 10.021-10.022)."""

from archlens.agents.refactor_agent import make_refactor_node


class _SDK:
    def __init__(self, applied=False):
        self._applied = applied
        self.apply_calls = []

    def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512):
        return "extract the request-routing helper into its own module"

    def apply_fix(self, finding, repo_path, graph_json=None):
        self.apply_calls.append((finding["id"], repo_path))
        return self._applied


def _validated_bug():
    return {"from": "bughunter", "level": "VALIDATED", "status": "open", "category": "SPOF",
            "source_file": "ss.py", "id": "spof-ss", "relation": "critical_path", "confidence": 0.95}


def _state(applied_repo="/clone"):
    return {"findings": [_validated_bug()], "target_repo": {"local_path": applied_repo}}


def test_refactor_plans_the_top_validated_finding():
    out = make_refactor_node(_SDK())(_state())
    update = out["findings"][0]
    assert update["plan"]["target"] == "ss.py"
    assert update["plan"]["action"]


def test_refactor_marks_fixed_when_the_sdk_applies_the_fix():
    out = make_refactor_node(_SDK(applied=True))(_state())
    assert out["findings"][0]["status"] == "fixed"
    assert out["findings"][0]["applied"] is True


def test_refactor_stays_selected_when_the_fix_cannot_be_applied():
    out = make_refactor_node(_SDK(applied=False))(_state())
    assert out["findings"][0]["status"] == "selected"


def test_refactor_delegates_the_write_to_the_sdk():
    sdk = _SDK()
    make_refactor_node(sdk)(_state("/repo"))
    assert sdk.apply_calls == [("spof-ss", "/repo")]  # the node never writes; the SDK does


def test_refactor_is_noop_without_a_validated_finding():
    assert make_refactor_node(_SDK())({"findings": []}) == {}


def test_refactor_rationale_is_authored_by_the_llm():
    out = make_refactor_node(_SDK())(_state())
    assert out["findings"][0]["plan"]["rationale"].startswith("extract the request-routing")
