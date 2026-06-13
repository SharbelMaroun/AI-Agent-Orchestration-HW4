"""TDD tests for the RepoAgent orchestration node (tasks 10.013-10.014)."""

from pathlib import Path
from types import SimpleNamespace

from archlens.agents.repo_agent import make_repo_node


class _SDK:
    def __init__(self):
        self.calls = []

    def clone_target_repo(self, run_id, use_fallback=False):
        self.calls.append(("clone", run_id))
        return Path("/clone/repo")

    def validate_repo(self, path, use_fallback=False):
        self.calls.append(("validate", str(path)))
        return SimpleNamespace(passed=True)


def test_repo_node_writes_target_repo_payload():
    out = make_repo_node(_SDK())({"run_id": "r1"})
    assert out["target_repo"]["validated"] is True
    assert out["target_repo"]["local_path"]


def test_repo_node_delegates_clone_and_validate_to_sdk():
    sdk = _SDK()
    make_repo_node(sdk)({"run_id": "r1"})
    assert ("clone", "r1") in sdk.calls
    assert any(call[0] == "validate" for call in sdk.calls)
