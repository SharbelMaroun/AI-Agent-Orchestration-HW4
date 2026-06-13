"""Stage orchestrator: runs the five stages, halts on first failure (tasks 4.016-4.017, 4.047)."""

import logging
from pathlib import Path

from archlens.graphops.cli_wrapper import GraphifyCLI
from archlens.graphops.errors import GraphifyError
from archlens.graphops.stages import StageResult, StageStatus, ordered_stages
from archlens.shared.constants import LOGGER_NAME

logger = logging.getLogger(f"{LOGGER_NAME}.graphops")


def run_pipeline(cli: GraphifyCLI, repo_path: Path, skip_extract: bool = False) -> list[StageResult]:
    """Execute stages in order; on the first typed failure, stop and return results so far."""
    results: list[StageResult] = []
    for stage in ordered_stages():
        if skip_extract and stage.value == "extract":
            results.append(
                StageResult(stage=stage, status=StageStatus.SKIPPED, message="cache hit")
            )
            logger.info("skipping extract for unchanged subtree")
            continue
        try:
            cli.run_stage(stage.value, repo_path)
            results.append(StageResult(stage=stage, status=StageStatus.OK))
        except GraphifyError as exc:
            results.append(StageResult(stage=stage, status=StageStatus.FAILED, message=str(exc)))
            logger.warning("stage %s failed: %s", stage.value, exc)
            break
    return results
