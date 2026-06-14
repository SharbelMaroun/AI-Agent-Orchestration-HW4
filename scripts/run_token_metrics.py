"""End-to-end Phase 12 token-metrics pipeline (task 12.044).

Loads the persisted baseline and assisted ledgers, exports metrics/out/token_metrics.json, renders
the per-model cost table and the savings charts, and writes the savings explanation when the target
was missed. Run with: uv run python scripts/run_token_metrics.py
"""

from pathlib import Path

from archlens.metrics.amortization import compute_amortization
from archlens.metrics.charts import generate_charts
from archlens.metrics.cost_tables import write_cost_table
from archlens.metrics.explanation import write_explanation_if_needed
from archlens.metrics.ledger import TokenLedger
from archlens.metrics.ledger_io import ledger_path, load_ledger
from archlens.metrics.savings import compute_savings
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup


def main() -> int:
    cfg = load_setup()
    sdk = ArchLensSDK()
    baseline = load_ledger(ledger_path(cfg.metrics.baseline_ledger))
    assisted = load_ledger(ledger_path(cfg.metrics.assisted_ledger))
    graph_build_tokens = baseline.entries[0].input_tokens  # one full-scan build cost
    metrics = sdk.export_token_metrics(baseline, assisted, graph_build_tokens)

    out_dir = Path(cfg.metrics.output_dir)
    write_cost_table(TokenLedger(list(baseline.entries) + list(assisted.entries)))
    generate_charts(baseline, assisted, out_dir)
    savings = compute_savings(baseline.total_tokens(), assisted.total_tokens(),
                              cfg.metrics.savings_target_pct)
    per_query = (baseline.total_tokens() - assisted.total_tokens()) // len(assisted.entries)
    explanation = write_explanation_if_needed(
        savings, compute_amortization(graph_build_tokens, per_query))

    print(f"savings_pct: {metrics['savings']['savings_pct']:.2f}%")
    print(f"target_met: {metrics['target_met']}")
    print(f"break_even_queries: {metrics['amortization']['break_even_queries']}")
    print(f"explanation written: {explanation}")
    print(f"token_metrics.json: {ledger_path(cfg.metrics.metrics_json)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
