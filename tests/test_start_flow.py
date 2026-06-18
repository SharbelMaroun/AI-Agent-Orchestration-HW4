"""Tests for the interactive `start` flow: pick -> clone -> report -> analyze, plus clone_url."""

from types import SimpleNamespace

import pytest

from archlens.__main__ import run_start
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup
from archlens.shared.errors import CloneNetworkError


class _SDK:
    def __init__(self, clone=None):
        self._clone = clone or (lambda url: "runs/manual/target")
        self.reset_called = False
        self.analyzed_path = None

    def suggested_repos(self):
        return [SimpleNamespace(
            name="buggy-python",
            url="https://github.com/andela/buggy-python",
            note="primary",
        )]

    def clone_url(self, url):
        return self._clone(url)

    def reset_run_state(self):
        self.reset_called = True

    def analyze(self, repo_path=None):
        self.analyzed_path = repo_path
        return f"AnalysisReport(path={repo_path})"


def test_run_start_clones_then_analyzes_the_chosen_repo():
    out = []
    sdk = _SDK()
    rc = run_start(sdk, input_fn=lambda _p: "1", output_fn=out.append)
    assert rc == 0
    assert sdk.reset_called and sdk.analyzed_path == "runs/manual/target"
    assert any("Cloned to" in line for line in out)
    assert any("AnalysisReport(path=" in line for line in out)


def test_run_start_reports_a_clone_failure_and_stops():
    def boom(url):
        raise CloneNetworkError("network down")

    out = []
    rc = run_start(_SDK(clone=boom), input_fn=lambda _p: "1", output_fn=out.append)
    assert rc == 1
    assert any("Could not clone" in line for line in out)


def test_run_start_rejects_an_invalid_choice():
    rc = run_start(_SDK(), input_fn=lambda _p: "garbage", output_fn=lambda _line: None)
    assert rc == 1


class _GK:
    def __init__(self):
        self.clones = []

    def git_clone(self, repo, dest):
        self.clones.append(repo.url)
        return dest


def test_clone_url_builds_a_repoblock_and_clones_via_the_gatekeeper(tmp_path):
    gk = _GK()
    sdk = ArchLensSDK(gatekeeper=gk)
    sdk._config().target_repo.workdir_root = str(tmp_path)  # redirect the sandbox to tmp
    dest = sdk.clone_url("https://github.com/foo/bar", run_id="t1")
    assert gk.clones == ["https://github.com/foo/bar"]
    assert dest.name == "target"


def test_clone_url_rejects_a_disallowed_url_scheme():
    with pytest.raises(ValueError):
        ArchLensSDK().clone_url("ftp://example.com/x")


def test_config_exposes_the_lecturers_suggested_repos():
    names = {r.name for r in load_setup().suggested_repos}
    assert {"buggy-python", "broken-python", "requests"} <= names
