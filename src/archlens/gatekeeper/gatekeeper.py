"""Gatekeeper — the sole path for every external API and network call.

LLM calls and git remote operations all route through this class; no other module
may touch the network (enforced by tests/test_no_direct_git.py).
"""

import logging
from pathlib import Path

from ..gatekeeper.git_ops import clone_with_retry, run_local_git
from ..gatekeeper.graphify_ops import run_command
from ..gatekeeper.proc import run_capture
from ..shared.config import RepoBlock
from ..shared.constants import DEFAULT_TIMEOUT_S, LOGGER_NAME
from ..shared.rate_limits import RateLimitsConfig, load_rate_limits

logger = logging.getLogger(f"{LOGGER_NAME}.gatekeeper")


class Gatekeeper:
    """Loads rate-limit policy at construction; all external calls route through here."""

    def __init__(self, config: RateLimitsConfig | None = None, executor=None) -> None:
        self._config = config if config is not None else load_rate_limits()
        self._executor = executor

    @property
    def limits(self) -> RateLimitsConfig:
        return self._config

    def _build_executor(self):
        from .clock import SystemClock
        from .executor import RateLimitedExecutor
        from .mock_client import MockAnthropicClient

        return RateLimitedExecutor(MockAnthropicClient(), SystemClock(), self._config)

    def execute(self, model, messages, **kwargs):
        """Single entry point for every outbound LLM call, under the rate_limits.json policy."""
        if self._executor is None:
            self._executor = self._build_executor()
        return self._executor.execute(model, messages, **kwargs)

    def git_clone(self, repo: RepoBlock, dest: Path) -> Path:
        """Clone a remote repository under the retry policy from rate_limits.json."""
        limits = self._config.rate_limits.services.default
        logger.info("git clone %s -> %s (depth=%s)", repo.url, dest, repo.clone_depth)
        return clone_with_retry(repo, dest, limits)

    def run_graphify(self, argv: list[str], label: str, timeout_s: int) -> str:
        """Execute a Graphify command (e.g. update/extract) through the gatekeeper egress."""
        logger.info("graphify %s: %s", label, " ".join(argv[:2]))
        return run_command(argv, label, timeout_s)

    def git_local(self, args: list[str], cwd: Path, timeout_s: int | None = None) -> str:
        """Run a local git command (branch/revert/inspect) through the gatekeeper egress."""
        timeout = timeout_s if timeout_s is not None else DEFAULT_TIMEOUT_S
        logger.info("git local %s in %s", args[:2], cwd)
        return run_local_git(args, cwd, timeout)

    def run_subprocess(self, argv: list[str], cwd, timeout_s: int | None = None):
        """Run a non-network command (e.g. the target repo's test suite) through the egress."""
        timeout = timeout_s if timeout_s is not None else DEFAULT_TIMEOUT_S
        logger.info("subprocess %s in %s", argv[:3], cwd)
        return run_capture(argv, cwd, timeout)
