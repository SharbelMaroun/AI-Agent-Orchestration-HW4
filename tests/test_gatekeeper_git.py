"""Mocked-subprocess TDD tests for the gatekeeper git-clone wrapper (tasks 3.022, 3.024)."""

import subprocess
from types import SimpleNamespace

import pytest

from archlens.gatekeeper import git_ops
from archlens.shared.config import RepoBlock
from archlens.shared.errors import CloneNetworkError, CloneTimeoutError


def _repo(**overrides) -> RepoBlock:
    data = {
        "url": "https://github.com/org/repo",
        "branch": "main",
        "pinned_commit": "abc1234",
        "workdir_root": "runs",
        "clone_depth": 2,
        "timeout_s": 7,
        "max_size_mb": 50,
    }
    data.update(overrides)
    return RepoBlock.model_validate(data)


def test_success_invokes_mocked_git_only(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(git_ops.subprocess, "run", fake_run)
    git_ops.run_git_clone(_repo(), tmp_path / "dest")
    assert calls, "the mocked subprocess.run was never invoked"
    assert calls[0][0] == "git" and calls[0][1] == "clone"


def test_command_line_contains_depth_branch_and_pinned_commit(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(git_ops.subprocess, "run", fake_run)
    git_ops.run_git_clone(_repo(), tmp_path / "dest")
    clone_cmd = calls[0]
    assert clone_cmd[2:4] == ["--depth", "2"]
    assert "--branch" in clone_cmd and "main" in clone_cmd
    fetch_cmd = calls[1]
    assert fetch_cmd[:4] == ["git", "-C", str(tmp_path / "dest"), "fetch"]
    assert fetch_cmd[-1] == "abc1234"
    checkout_cmd = calls[2]
    assert checkout_cmd[:2] == ["git", "-C"] and checkout_cmd[-1] == "abc1234"


def test_head_pinning_skips_checkout(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(git_ops.subprocess, "run", fake_run)
    git_ops.run_git_clone(_repo(pinned_commit="HEAD"), tmp_path / "dest")
    assert len(calls) == 1


def test_nonzero_exit_maps_to_typed_error(monkeypatch, tmp_path):
    def fake_run(cmd, **kwargs):
        return SimpleNamespace(returncode=128, stdout="", stderr="fatal: Could not resolve host")

    monkeypatch.setattr(git_ops.subprocess, "run", fake_run)
    with pytest.raises(CloneNetworkError):
        git_ops.run_git_clone(_repo(), tmp_path / "dest")


def test_timeout_raises_clone_timeout_error(monkeypatch, tmp_path):
    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd="git clone", timeout=7)

    monkeypatch.setattr(git_ops.subprocess, "run", fake_run)
    with pytest.raises(CloneTimeoutError):
        git_ops.run_git_clone(_repo(), tmp_path / "dest")
