"""TDD tests for the stage orchestrator: happy path, halt, cache skip, error paths (4.016-4.047)."""

from pathlib import Path

from archlens.graphops.errors import GraphifyNotFoundError, GraphifyStageError
from archlens.graphops.orchestrator import run_pipeline
from archlens.graphops.stages import StageStatus


class SpyCLI:
    def __init__(self, fail_on=None, error=None) -> None:
        self.calls: list[str] = []
        self._fail_on = fail_on
        self._error = error

    def run_stage(self, stage, repo_path):
        self.calls.append(stage)
        if stage == self._fail_on:
            raise self._error
        return "ok"


def test_happy_path_runs_five_stages():
    cli = SpyCLI()
    results = run_pipeline(cli, Path("/repo"))
    assert [r.stage.value for r in results] == ["detect", "extract", "build", "cluster", "export"]
    assert all(r.status is StageStatus.OK for r in results)


def test_halt_on_first_failure_skips_later_stages():
    cli = SpyCLI(fail_on="build", error=GraphifyStageError("build", "boom"))
    results = run_pipeline(cli, Path("/repo"))
    assert [r.stage.value for r in results] == ["detect", "extract", "build"]
    assert results[-1].status is StageStatus.FAILED
    assert cli.calls == ["detect", "extract", "build"]


def test_cache_hit_skips_extract_without_invoking_it():
    cli = SpyCLI()
    results = run_pipeline(cli, Path("/repo"), skip_extract=True)
    assert "extract" not in cli.calls
    extract = next(r for r in results if r.stage.value == "extract")
    assert extract.status is StageStatus.SKIPPED


def test_missing_binary_returns_failed_result_not_crash():
    cli = SpyCLI(fail_on="detect", error=GraphifyNotFoundError("nope"))
    results = run_pipeline(cli, Path("/repo"))
    assert results[0].status is StageStatus.FAILED
    assert len(results) == 1
