"""TDD tests for the RefactorAgent orchestration node (tasks 10.021-10.022)."""

from types import SimpleNamespace

from archlens.agents.refactor_agent import make_refactor_node


class _SDK:
    def __init__(self, applied=False):
        self._applied = applied
        self.apply_calls = []

    def _config(self):
        return SimpleNamespace(
            improvement_loop=SimpleNamespace(allowed_evidence_levels=["EXTRACTED", "VALIDATED"]))

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


def test_refactor_blocks_a_finding_without_a_full_citation():
    bug = {**_validated_bug(), "relation": ""}  # no relation -> evidence gate blocks execution
    sdk = _SDK(applied=True)
    out = make_refactor_node(sdk)({"findings": [bug], "target_repo": {"local_path": "/c"}})
    assert out["findings"][0]["status"] == "selected"
    assert out["findings"][0]["blocked_by"] == "evidence_gate"
    assert sdk.apply_calls == []  # gated findings never reach the writer


def test_refactor_defers_an_irreversible_action_to_human_approval():
    bug = {**_validated_bug(), "source_file": "deploy.py"}  # 'deploy' -> irreversible guardrail tier
    sdk = _SDK(applied=True)
    out = make_refactor_node(sdk)({"findings": [bug], "target_repo": {"local_path": "/c"}})
    assert sdk.apply_calls == []  # irreversible work is never auto-applied
    assert out["approvals"][0]["status"] == "pending"
    assert out["findings"][0]["status"] == "selected"


def test_refactor_records_an_auto_approved_guardrail_for_a_reversible_fix():
    out = make_refactor_node(_SDK(applied=True))(_state())
    assert out["approvals"][0]["status"] == "auto-approved"
    assert out["approvals"][0]["tier"] == "reversible"


def test_refactor_skips_a_finding_whose_approval_was_denied():
    state = {**_state(), "approvals": [{"finding": "spof-ss", "status": "denied"}]}
    assert make_refactor_node(_SDK())(state) == {}
