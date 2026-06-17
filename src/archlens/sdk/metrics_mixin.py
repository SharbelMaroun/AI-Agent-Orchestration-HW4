"""SDK token-measurement methods (Phase 12) — a mixin to honour the 150-line file cap.

All measurement runs go through the gatekeeper egress; offline runs use the estimating mock
client so recorded token counts reflect real context size.
"""

from pathlib import Path

from ..metrics.amortization import compute_amortization
from ..metrics.assisted_runner import AssistedRunner
from ..metrics.baseline_runner import BaselineRunner
from ..metrics.export import build_metrics, write_metrics_json
from ..metrics.ledger_io import ledger_path
from ..metrics.questions import Question, load_questions
from ..metrics.savings import compute_savings


class MetricsMixin:
    """Phase 12 measurement entry points on the SDK facade."""

    def load_questions(self) -> list[Question]:
        """Load the ten standard architecture questions (Q01-Q10)."""
        return load_questions()

    def _metrics_gatekeeper(self, live: bool = False):
        """A gatekeeper for measurement: the real API when live, else an estimating offline mock."""
        from ..gatekeeper.gatekeeper import Gatekeeper

        if live:
            return Gatekeeper(mode="live")
        from ..gatekeeper.clock import SystemClock
        from ..gatekeeper.executor import RateLimitedExecutor
        from ..gatekeeper.mock_client import MockAnthropicClient

        executor = RateLimitedExecutor(MockAnthropicClient(estimate=True), SystemClock())
        return Gatekeeper(executor=executor)

    def run_baseline(self, repo_path, model: str | None = None,
                     questions: list[Question] | None = None, gatekeeper=None, live: bool = False):
        """Run the naive full-context baseline protocol; return the usage TokenLedger."""
        chosen_model = model or self._config().metrics.default_model
        qs = questions if questions is not None else self.load_questions()
        gk = gatekeeper if gatekeeper is not None else self._metrics_gatekeeper(live)
        return BaselineRunner(gk, chosen_model).run(Path(repo_path), qs)

    def run_assisted(self, vault_root=None, graph_json=None, model: str | None = None,
                     questions: list[Question] | None = None, gatekeeper=None,
                     max_wiki_pages: int | None = None, live: bool = False):
        """Run the Graphify-assisted protocol over the vault; return the usage TokenLedger."""
        cfg = self._config()
        chosen_model = model or cfg.metrics.default_model
        root = vault_root if vault_root is not None else cfg.vault.vault_root
        cap = max_wiki_pages if max_wiki_pages is not None else cfg.metrics.max_wiki_pages
        qs = questions if questions is not None else self.load_questions()
        gk = gatekeeper if gatekeeper is not None else self._metrics_gatekeeper(live)
        return AssistedRunner(gk, chosen_model, root, graph_json, cap).run(qs)

    def compare_graph_vs_code(self, graph_json, repo_path, top_k: int = 3) -> dict:
        """Evaluate the top bottlenecks with vs without Graphify — real flow tokens + LLM-judged quality."""
        from ..metrics.graph_vs_code import compare
        return compare(self, self.load_analysis_graph(graph_json), repo_path, top_k)

    def export_token_metrics(self, baseline_ledger, assisted_ledger, graph_build_tokens: int,
                             path=None) -> dict:
        """Build and persist metrics/out/token_metrics.json; return the metrics document."""
        cfg = self._config()
        baseline_tokens, assisted_tokens = (baseline_ledger.total_tokens(),
                                            assisted_ledger.total_tokens())
        savings = compute_savings(baseline_tokens, assisted_tokens, cfg.metrics.savings_target_pct)
        answered = len(assisted_ledger.entries)
        per_query = (baseline_tokens - assisted_tokens) // answered if answered else 0
        amortization = compute_amortization(graph_build_tokens, per_query)
        metrics = build_metrics(baseline_ledger, assisted_ledger, savings, amortization, cfg)
        target = Path(path) if path is not None else ledger_path(cfg.metrics.metrics_json)
        write_metrics_json(metrics, target)
        return metrics
