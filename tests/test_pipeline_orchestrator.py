"""TDD tests for the orchestrator: real command run + typed-error handling (4.016-4.017, 4.047)."""

from pathlib import Path

from archlens.graphops.errors import GraphifyNotFoundError, GraphifyStageError
from archlens.graphops.orchestrator import run_pipeline
from archlens.graphops.stages import StageStatus


class FakeCLI:
    def __init__(self, command: str = "update", error=None) -> None:
        self.command = command
        self._error = error
        self.ran = False

    def run(self, repo_path):
        self.ran = True
        if self._error:
            raise self._error
        return "ok"


def test_successful_run_records_ok_stage():
    cli = FakeCLI()
    results = run_pipeline(cli, Path("/repo"))
    assert cli.ran
    assert len(results) == 1
    assert results[0].stage == "update"
    assert results[0].status is StageStatus.OK


def test_stage_error_returns_failed_not_crash():
    results = run_pipeline(FakeCLI(error=GraphifyStageError("update", "boom")), Path("/repo"))
    assert results[0].status is StageStatus.FAILED
    assert "boom" in results[0].message


def test_missing_binary_returns_failed_not_crash():
    results = run_pipeline(FakeCLI(error=GraphifyNotFoundError("nope")), Path("/repo"))
    assert results[0].status is StageStatus.FAILED
