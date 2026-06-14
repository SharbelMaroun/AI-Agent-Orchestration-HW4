"""TDD tests for the gatekeeper TokenLedger hooks (task 9.035)."""

from archlens.gatekeeper.ledger import LedgerEntry, TokenLedger


class _MetricsAgentStub:
    """Stands in for MetricsAgent: consumes ledger entries via a registered hook."""

    def __init__(self):
        self.seen = []

    def consume(self, entry: LedgerEntry) -> None:
        self.seen.append(entry)


def test_record_appends_one_entry_with_all_fields():
    ledger = TokenLedger()
    entry = ledger.record(model="claude-opus-4-8", input_tokens=10, output_tokens=4, usd_cost=0.01)
    assert len(ledger.entries) == 1
    assert (entry.model, entry.input_tokens, entry.output_tokens, entry.usd_cost) == (
        "claude-opus-4-8", 10, 4, 0.01)


def test_registered_hook_consumes_each_entry():
    ledger = TokenLedger()
    agent = _MetricsAgentStub()
    ledger.register_hook(agent.consume)
    ledger.record(model="m", input_tokens=1, output_tokens=1, usd_cost=0.5)
    ledger.record(model="m", input_tokens=2, output_tokens=2, usd_cost=0.5)
    assert len(agent.seen) == 2


def test_total_cost_sums_entries():
    ledger = TokenLedger()
    ledger.record(model="m", input_tokens=1, output_tokens=1, usd_cost=0.25)
    ledger.record(model="m", input_tokens=1, output_tokens=1, usd_cost=0.75)
    assert ledger.total_cost() == 1.0
