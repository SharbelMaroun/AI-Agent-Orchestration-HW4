"""TDD tests for the Phase 12 cost calculator (task 12.012)."""

import pytest

from archlens.metrics.cost import entry_cost, ledger_cost
from archlens.metrics.ledger import TokenLedger
from archlens.metrics.ledger_model import TokenLedgerEntry
from archlens.shared.exceptions import ConfigError


def _entry(model="claude-opus-4-8", in_tokens=1_000_000, out_tokens=1_000_000):
    return TokenLedgerEntry(agent="A", model=model, protocol="baseline",
                            input_tokens=in_tokens, output_tokens=out_tokens)


def test_single_entry_cost_matches_pricing():
    # opus 4.8: $5/MTok in + $25/MTok out; 1M in + 1M out = 5 + 25 = 30
    assert entry_cost(_entry()) == pytest.approx(30.0)


def test_partial_mtok_cost():
    # 100k input at $5/MTok, no output = 0.5
    assert entry_cost(_entry(in_tokens=100_000, out_tokens=0)) == pytest.approx(0.5)


def test_haiku_cheaper_than_opus():
    assert entry_cost(_entry(model="claude-haiku-4-5")) < entry_cost(_entry())


def test_ledger_total_cost_sums_entries():
    ledger = TokenLedger([_entry(in_tokens=1_000_000, out_tokens=0),
                          _entry(in_tokens=1_000_000, out_tokens=0)])
    assert ledger_cost(ledger) == pytest.approx(10.0)


def test_unknown_model_raises_config_error():
    with pytest.raises(ConfigError):
        entry_cost(_entry(model="no-such-model"))
