"""TDD tests for the MetricsAgent orchestration node (tasks 10.025-10.026)."""

from archlens.agents.metrics_agent import make_metrics_node


class _SDK:
    def token_usage(self):
        return {"baseline": 100, "assisted": 30, "rows": [{"model": "x", "in": 10}]}


def test_metrics_appends_token_ledger_entries():
    ledger = make_metrics_node(_SDK())({})["token_ledger"]
    assert ledger["baseline_tokens"] == 100
    assert ledger["assisted_tokens"] == 30
    assert ledger["savings_pct"] == 70.0
    assert ledger["rows"]
