"""TDD tests for the RefactorAgent orchestration node (tasks 10.021-10.022).

A source modification is irreversible-tier (ADR-009): the node must NOT write until a ``granted``
approval is recorded in ``state.approvals``. Without a grant it defers (pending + awaiting_approval);
with a grant it authors a plan and applies the fix through the SDK.
"""

from types import SimpleNamespace

from archlens.agents.refactor_agent import make_refactor_node


class _SDK:
    def __init__(self, applied=False):
        self._applied = applied
        self.apply_calls = []

    def _config(self):
        return SimpleNamespace(
            improvement_loop=SimpleNamespace(allowed_evidence_levels=["EXTRACTED", "VALIDATED"]))

    def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512, **kwargs):
        return "extract the request-routing helper into its own module"

    def apply_fix(self, finding, repo_path, graph_json=None):
        self.apply_calls.append((finding["id"], repo_path))
        return self._applied


def _validated_bug():
    return {"from": "bughunter", "level": "VALIDATED", "status": "open", "category": "SPOF",
            "source_file": "ss.py", "id": "spof-ss", "relation": "critical_path", "confidence": 0.95}


def _granted(finding="spof-ss"):
    return [{"action": "apply spof fix to ss.py", "finding": finding,
             "tier": "irreversible", "status": "granted", "approver": "lecturer"}]


def _state(applied_repo="/clone", approvals=None):
    """A state with one validated bug, optionally pre-approved (granted)."""
    state = {"findings": [_validated_bug()], "target_repo": {"local_path": applied_repo}}
    if approvals is not None:
        state["approvals"] = approvals
    return state


def _approved_state(applied_repo="/clone"):
    return _state(applied_repo, approvals=_granted())


def test_refactor_defers_a_source_modification_until_approved():
    sdk = _SDK(applied=True)
    out = make_refactor_node(sdk)(_state())  # no recorded approval
    assert sdk.apply_calls == []  # never writes without a grant
    assert out["findings"][0]["status"] == "awaiting_approval"
    assert out["approvals"][0]["status"] == "pending"
    assert out["approvals"][0]["tier"] == "irreversible"  # source mod -> irreversible, not auto-OK


def test_refactor_plans_the_top_validated_finding_once_approved():
    out = make_refactor_node(_SDK())(_approved_state())
    update = out["findings"][0]
    assert update["plan"]["target"] == "ss.py"
    assert update["plan"]["action"]


def test_refactor_marks_fixed_when_the_sdk_applies_an_approved_fix():
    out = make_refactor_node(_SDK(applied=True))(_approved_state())
    assert out["findings"][0]["status"] == "fixed"
    assert out["findings"][0]["applied"] is True


def test_refactor_stays_selected_when_an_approved_fix_cannot_be_applied():
    out = make_refactor_node(_SDK(applied=False))(_approved_state())
    assert out["findings"][0]["status"] == "selected"


def test_refactor_delegates_the_write_to_the_sdk_after_approval():
    sdk = _SDK()
    make_refactor_node(sdk)(_approved_state("/repo"))
    assert sdk.apply_calls == [("spof-ss", "/repo")]  # the node never writes; the SDK does


def test_refactor_is_noop_without_a_validated_finding():
    assert make_refactor_node(_SDK())({"findings": []}) == {}


def test_refactor_rationale_is_authored_by_the_llm():
    out = make_refactor_node(_SDK())(_approved_state())
    assert out["findings"][0]["plan"]["rationale"].startswith("extract the request-routing")


def test_refactor_blocks_a_finding_without_a_full_citation():
    bug = {**_validated_bug(), "relation": ""}  # no relation -> evidence gate blocks execution
    sdk = _SDK(applied=True)
    out = make_refactor_node(sdk)({"findings": [bug], "target_repo": {"local_path": "/c"},
                                   "approvals": _granted()})
    assert out["findings"][0]["status"] == "selected"
    assert out["findings"][0]["blocked_by"] == "evidence_gate"
    assert sdk.apply_calls == []  # gated findings never reach the writer, even when pre-approved


def test_refactor_does_not_re_request_after_a_grant():
    # A granted finding must NOT emit a fresh pending record (which would re-loop the approval gate).
    out = make_refactor_node(_SDK(applied=True))(_approved_state())
    assert "approvals" not in out


def test_refactor_skips_a_finding_whose_approval_was_denied():
    state = {**_state(), "approvals": [{"finding": "spof-ss", "status": "denied"}]}
    assert make_refactor_node(_SDK())(state) == {}
