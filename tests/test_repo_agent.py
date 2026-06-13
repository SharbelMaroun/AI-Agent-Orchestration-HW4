"""TDD tests for the RepoAgent LangGraph node with the SDK mocked (tasks 3.038, 3.040)."""

from pathlib import Path
from typing import TypedDict

import pytest
from langgraph.graph import StateGraph

from archlens.agents.repo_agent import make_repo_agent
from archlens.sdk.validation import CheckResult, ValidationResult
from archlens.shared.errors import CloneNetworkError


def _result(passed: bool) -> ValidationResult:
    checks = [CheckResult(n, passed, "checked") for n in ("is_python", "size_bounds", "has_tests", "license")]
    return ValidationResult(checks=checks)


class FakeSDK:
    def __init__(self, clone_fail_primary=False, clone_fail_all=False, invalid_primary=False):
        self.clone_calls: list[tuple[str, bool]] = []
        self._cfp, self._cfa, self._inv = clone_fail_primary, clone_fail_all, invalid_primary

    def clone_target_repo(self, run_id: str, use_fallback: bool = False) -> Path:
        self.clone_calls.append((run_id, use_fallback))
        if self._cfa or (self._cfp and not use_fallback):
            raise CloneNetworkError("clone failed")
        return Path("sandbox") / run_id / "target"

    def validate_repo(self, repo_dir: Path, use_fallback: bool = False) -> ValidationResult:
        return _result(not (self._inv and not use_fallback))


def test_node_writes_expected_state_keys_without_real_clone():
    sdk = FakeSDK()
    out = make_repo_agent(sdk)({"run_id": "r1"})
    assert set(out) >= {"target_repo", "validation", "fallback_used"}
    assert out["fallback_used"] is False
    assert sdk.clone_calls == [("r1", False)]


def test_clone_failure_triggers_exactly_one_fallback_attempt():
    sdk = FakeSDK(clone_fail_primary=True)
    out = make_repo_agent(sdk)({"run_id": "r1"})
    assert out["fallback_used"] is True
    assert sdk.clone_calls == [("r1", False), ("r1", True)]


def test_validation_failure_triggers_fallback():
    sdk = FakeSDK(invalid_primary=True)
    out = make_repo_agent(sdk)({"run_id": "r2"})
    assert out["fallback_used"] is True and out["validation"]["passed"] is True


def test_fallback_failure_propagates():
    sdk = FakeSDK(clone_fail_all=True)
    with pytest.raises(CloneNetworkError):
        make_repo_agent(sdk)({"run_id": "r3"})
    assert sdk.clone_calls == [("r3", False), ("r3", True)]


def test_node_registers_in_stategraph():
    class S(TypedDict, total=False):
        run_id: str
        target_repo: str
        validation: dict
        fallback_used: bool

    graph = StateGraph(S)
    graph.add_node("RepoAgent", make_repo_agent(FakeSDK()))
    graph.set_entry_point("RepoAgent")
    graph.set_finish_point("RepoAgent")
    assert graph.compile() is not None
