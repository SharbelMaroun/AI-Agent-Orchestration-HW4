"""Gatekeeper — the sole path for every external API and network call.

LLM calls and git remote operations all route through this class; no other module
may touch the network (enforced by tests/test_no_direct_git.py).
"""

import logging
from pathlib import Path

from archlens.gatekeeper.git_ops import clone_with_retry
from archlens.gatekeeper.graphify_ops import run_stage
from archlens.shared.config import RepoBlock
from archlens.shared.constants import LOGGER_NAME
from archlens.shared.rate_limits import RateLimitsConfig, load_rate_limits

logger = logging.getLogger(f"{LOGGER_NAME}.gatekeeper")


class Gatekeeper:
    """Loads rate-limit policy at construction; all external calls route through here."""

    def __init__(self, config: RateLimitsConfig | None = None) -> None:
        self._config = config if config is not None else load_rate_limits()

    @property
    def limits(self) -> RateLimitsConfig:
        return self._config

    def git_clone(self, repo: RepoBlock, dest: Path) -> Path:
        """Clone a remote repository under the retry policy from rate_limits.json."""
        limits = self._config.rate_limits.services.default
        logger.info("git clone %s -> %s (depth=%s)", repo.url, dest, repo.clone_depth)
        return clone_with_retry(repo, dest, limits)

    def run_graphify_stage(self, argv: list[str], stage: str, timeout_s: int) -> str:
        """Execute one Graphify pipeline stage through the gatekeeper egress."""
        logger.info("graphify stage %s: %s", stage, " ".join(argv[:3]))
        return run_stage(argv, stage, timeout_s)
