"""Run the configured Graphify command and record the outcome (tasks 4.016-4.017, 4.047).

Graphify performs its own incremental caching (it logs an "incremental scan" of changed vs
unchanged files), so ArchLens no longer reimplements stage-level skip logic.
"""

import logging

from ..graphops.cli_wrapper import GraphifyCLI
from ..graphops.errors import GraphifyError
from ..graphops.stages import StageResult, StageStatus
from ..shared.constants import LOGGER_NAME

logger = logging.getLogger(f"{LOGGER_NAME}.graphops")


def run_pipeline(cli: GraphifyCLI, repo_path) -> list[StageResult]:
    """Run the Graphify command; return a failed StageResult instead of crashing the agent loop."""
    try:
        cli.run(repo_path)
        return [StageResult(stage=cli.command, status=StageStatus.OK)]
    except GraphifyError as exc:
        logger.warning("graphify %s failed: %s", cli.command, exc)
        return [StageResult(stage=cli.command, status=StageStatus.FAILED, message=str(exc))]
