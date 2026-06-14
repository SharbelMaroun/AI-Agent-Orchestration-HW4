"""TDD tests for the Phase 12 TokenLedger and TokenLedgerEntry (task 12.004)."""

import pytest

from archlens.metrics.ledger import TokenLedger
from archlens.metrics.ledger_model import TokenLedgerEntry


def _entry(agent="RepoAgent", model="claude-opus-4-8", protocol="baseline",
           in_tokens=100, out_tokens=10, question_id="Q01"):
    return TokenLedgerEntry(agent=agent, model=model, protocol=protocol,
                            input_tokens=in_tokens, output_tokens=out_tokens,
                            question_id=question_id)


def test_entry_total_tokens_sums_input_and_output():
    assert _entry(in_tokens=100, out_tokens=25).total_tokens == 125


def test_entry_rejects_negative_tokens():
    with pytest.raises(ValueError):
        _entry(out_tokens=-1)


def test_entry_requires_agent_model_protocol():
    with pytest.raises(ValueError):
        _entry(agent="")


def test_append_grows_ledger_and_preserves_fields():
    ledger = TokenLedger()
    ledger.append(_entry())
    assert len(ledger) == 1
    assert ledger.entries[0].agent == "RepoAgent"


def test_totals_across_entries():
    ledger = TokenLedger([_entry(in_tokens=100, out_tokens=10),
                          _entry(in_tokens=50, out_tokens=5)])
    assert ledger.total_input() == 150
    assert ledger.total_output() == 15
    assert ledger.total_tokens() == 165


def test_filter_by_protocol_and_agent():
    ledger = TokenLedger([
        _entry(agent="RepoAgent", protocol="baseline"),
        _entry(agent="GraphAgent", protocol="assisted"),
        _entry(agent="GraphAgent", protocol="baseline"),
    ])
    assert len(ledger.filter(protocol="baseline")) == 2
    assert len(ledger.filter(agent="GraphAgent", protocol="baseline")) == 1


def test_filter_by_model_and_question_id():
    ledger = TokenLedger([_entry(model="m1", question_id="Q01"),
                          _entry(model="m2", question_id="Q02")])
    assert len(ledger.filter(model="m1")) == 1
    assert ledger.filter(question_id="Q02").entries[0].model == "m2"


def test_filter_unknown_field_raises():
    with pytest.raises(ValueError):
        TokenLedger().filter(nonsense="x")
