"""TDD tests for the token_metrics.json export schema (task 12.040)."""

import json

from archlens.metrics.amortization import compute_amortization
from archlens.metrics.export import build_metrics, write_metrics_json
from archlens.metrics.savings import compute_savings


def test_metrics_has_all_top_level_keys(synthetic_ledger):
    base, assisted = synthetic_ledger(n=10), synthetic_ledger(n=10)
    savings = compute_savings(base.total_tokens(), assisted.total_tokens())
    metrics = build_metrics(base, assisted, savings, compute_amortization(1000, 50))
    for key in ("savings", "per_agent", "per_model", "cost_totals", "amortization", "target_met"):
        assert key in metrics
    assert isinstance(metrics["per_agent"], list)
    assert isinstance(metrics["per_model"], list)


def test_metrics_json_round_trips(tmp_path, synthetic_ledger):
    base = synthetic_ledger(n=6)
    savings = compute_savings(1000, 200)
    metrics = build_metrics(base, base, savings, compute_amortization(1000, 100))
    out = write_metrics_json(metrics, tmp_path / "token_metrics.json")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded["target_met"] == savings.target_met
    assert loaded["cost_totals"]["key"] == "TOTAL"
