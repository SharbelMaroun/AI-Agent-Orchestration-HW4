"""SDK token-measurement methods (Phase 12) — a mixin to honour the 150-line file cap.

All measurement runs go through the gatekeeper egress; offline runs use the estimating mock
client so recorded token counts reflect real context size.
"""

from pathlib import Path

from ..metrics.baseline_runner import BaselineRunner
from ..metrics.questions import Question, load_questions


class MetricsMixin:
    """Phase 12 measurement entry points on the SDK facade."""

    def load_questions(self) -> list[Question]:
        """Load the ten standard architecture questions (Q01-Q10)."""
        return load_questions()

    def _metrics_gatekeeper(self):
        """A gatekeeper whose offline executor estimates tokens from real context size."""
        from ..gatekeeper.clock import SystemClock
        from ..gatekeeper.executor import RateLimitedExecutor
        from ..gatekeeper.gatekeeper import Gatekeeper
        from ..gatekeeper.mock_client import MockAnthropicClient

        executor = RateLimitedExecutor(MockAnthropicClient(estimate=True), SystemClock())
        return Gatekeeper(executor=executor)

    def run_baseline(self, repo_path, model: str | None = None,
                     questions: list[Question] | None = None, gatekeeper=None):
        """Run the naive full-context baseline protocol; return the usage TokenLedger."""
        chosen_model = model or self._config().metrics.default_model
        qs = questions if questions is not None else self.load_questions()
        gk = gatekeeper if gatekeeper is not None else self._metrics_gatekeeper()
        return BaselineRunner(gk, chosen_model).run(Path(repo_path), qs)
