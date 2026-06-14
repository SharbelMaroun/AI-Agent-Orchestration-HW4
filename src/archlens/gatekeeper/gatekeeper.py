"""Gatekeeper — the sole path for every external API and network call.

LLM calls and git remote operations all route through this class; no other module
may touch the network (enforced by tests/test_no_direct_git.py).
"""

import logging
from pathlib import Path

from ..gatekeeper.git_ops import clone_with_retry, run_local_git
from ..gatekeeper.graphify_ops import run_command
from ..gatekeeper.proc import run_capture
from ..metrics.ledger import TokenLedger
from ..metrics.ledger_model import TokenLedgerEntry
from ..shared.config import RepoBlock
from ..shared.constants import DEFAULT_TIMEOUT_S, LOGGER_NAME, PROTOCOL_BASELINE
from ..shared.rate_limits import RateLimitsConfig, load_rate_limits

logger = logging.getLogger(f"{LOGGER_NAME}.gatekeeper")


class Gatekeeper:
    """Loads rate-limit policy at construction; all external calls route through here."""

    def __init__(self, config: RateLimitsConfig | None = None, executor=None,
                 usage_ledger: TokenLedger | None = None) -> None:
        self._config = config if config is not None else load_rate_limits()
        self._executor = executor
        self.usage_ledger = usage_ledger if usage_ledger is not None else TokenLedger()
        self.budget_alerts: list[dict] = []

    @property
    def limits(self) -> RateLimitsConfig:
        return self._config

    def get_queue_status(self) -> dict:
        """Return overflow-queue depth and capacity (the §5.1 gatekeeper monitoring interface)."""
        depth = self._executor.queue_depth if self._executor is not None else 0
        return {"queue_depth": depth, "max_depth": self._config.queue.max_depth,
                "recorded_calls": len(self.usage_ledger)}

    def _build_executor(self):
        from .clock import SystemClock
        from .executor import RateLimitedExecutor
        from .mock_client import MockAnthropicClient

        return RateLimitedExecutor(MockAnthropicClient(), SystemClock(), self._config)

    def execute(self, model, messages, *, agent: str = "orchestrator",
                protocol: str = PROTOCOL_BASELINE, question_id: str = "", **kwargs):
        """Single entry point for every outbound LLM call, under the rate_limits.json policy.

        Records one TokenLedgerEntry (agent/protocol/question tagged) per call before returning.
        """
        if self._executor is None:
            self._executor = self._build_executor()
        response = self._executor.execute(model, messages, **kwargs)
        self.record_usage(response, agent=agent, model=model,
                          protocol=protocol, question_id=question_id)
        return response

    def record_usage(self, response, *, agent: str, model: str, protocol: str,
                     question_id: str = "") -> TokenLedgerEntry:
        """Append one metrics TokenLedgerEntry for a completed LLM call (task 12.009)."""
        usage = getattr(response, "usage", None)
        entry = self.usage_ledger.append(TokenLedgerEntry(
            agent=agent, model=model, protocol=protocol,
            input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
            question_id=question_id))
        self._check_budget()
        return entry

    def _check_budget(self) -> None:
        """Log a structured warning the first time cumulative tokens cross the alert ratio.

        Never raises and never rejects — the call always completes (task 12.036).
        """
        budget = self._config.budget
        if budget.token_budget <= 0 or self.budget_alerts:
            return
        used = self.usage_ledger.total_tokens()
        if used >= budget.alert_ratio * budget.token_budget:
            self.budget_alerts.append({"used": used, "token_budget": budget.token_budget})
            logger.warning("token budget alert: %d/%d tokens used (>= %.0f%%)",
                           used, budget.token_budget, budget.alert_ratio * 100)

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
