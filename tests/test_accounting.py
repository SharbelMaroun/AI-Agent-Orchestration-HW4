"""TDD tests for per-agent and per-model accounting aggregation (task 12.027)."""

import pytest

from archlens.metrics.accounting import by_agent, by_model, grand_total


def test_by_agent_breakdown_covers_all_agents(synthetic_ledger):
    ledger = synthetic_ledger(n=12)
    rows = by_agent(ledger)
    assert {r.key for r in rows} == {"RepoAgent", "GraphAgent", "AnalystAgent"}
    assert sum(r.total_tokens for r in rows) == ledger.total_tokens()


def test_by_model_breakdown_and_costs(synthetic_ledger):
    ledger = synthetic_ledger(n=10)
    rows = by_model(ledger)
    assert {r.key for r in rows} == {"claude-opus-4-8", "claude-haiku-4-5"}
    assert all(r.usd_cost > 0 for r in rows)


def test_grand_total_sums_everything(synthetic_ledger):
    ledger = synthetic_ledger(n=10)
    total = grand_total(ledger)
    assert total.input_tokens == ledger.total_input()
    assert total.output_tokens == ledger.total_output()
    assert total.usd_cost == pytest.approx(sum(r.usd_cost for r in by_agent(ledger)))
