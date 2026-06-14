"""Smoke test for the synthetic-ledger fixture factory (task 12.003)."""


def test_synthetic_ledger_produces_ten_entries(synthetic_ledger):
    ledger = synthetic_ledger()
    assert len(ledger) == 10
    assert {entry.protocol for entry in ledger.entries} == {"baseline", "assisted"}


def test_synthetic_ledger_count_is_configurable(synthetic_ledger):
    assert len(synthetic_ledger(n=4)) == 4
    assert len(synthetic_ledger(n=25)) == 25
