"""TDD tests for the per-iteration Graphify re-run wrapper (task 11.029)."""

import pytest

from archlens.graphops.rerun import rerun_graphify
from archlens.shared.constants import GRAPH_HTML, GRAPH_JSON, REPORT_MD

_ARTIFACTS = (GRAPH_JSON, GRAPH_HTML, REPORT_MD)


def _good_runner(repo, out, stages):
    for name in _ARTIFACTS:
        (out / name).write_text("x", encoding="utf-8")


def test_rerun_runs_the_five_stages_in_order(tmp_path):
    seen = {}

    def runner(repo, out, stages):
        seen["stages"] = stages
        _good_runner(repo, out, stages)

    rerun_graphify(tmp_path / "repo", tmp_path / "runs", 1, runner)
    assert seen["stages"] == ["detect", "extract", "build", "cluster", "export"]


def test_rerun_creates_iteration_dir_with_fresh_graph_json(tmp_path):
    out = rerun_graphify(tmp_path / "repo", tmp_path / "runs", 3, _good_runner)
    assert out.name == "iteration_03"
    assert (out / GRAPH_JSON).is_file()


def test_rerun_raises_when_an_artifact_is_missing(tmp_path):
    def partial(repo, out, stages):
        (out / GRAPH_JSON).write_text("x", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        rerun_graphify(tmp_path / "repo", tmp_path / "runs", 1, partial)
