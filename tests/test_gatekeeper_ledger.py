"""TDD tests for the gatekeeper TokenLedger hooks (task 9.035) and usage recording (task 12.008)."""

from types import SimpleNamespace

from archlens.gatekeeper.gatekeeper import Gatekeeper
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


class _StubExecutor:
    """Executor double returning a response carrying canned token usage (task 12.008)."""

    def __init__(self, in_tokens: int = 12, out_tokens: int = 3):
        self._usage = SimpleNamespace(input_tokens=in_tokens, output_tokens=out_tokens)
        self.calls = 0

    def execute(self, model, messages, **kwargs):
        self.calls += 1
        return SimpleNamespace(usage=self._usage)


def test_execute_appends_one_usage_entry_with_all_fields():
    gk = Gatekeeper(executor=_StubExecutor())
    gk.execute("claude-opus-4-8", [{"role": "user", "content": "hi"}],
               agent="AnalystAgent", protocol="baseline", question_id="Q01")
    entries = gk.usage_ledger.entries
    assert len(entries) == 1
    recorded = entries[0]
    assert (recorded.agent, recorded.model, recorded.input_tokens,
            recorded.output_tokens, recorded.protocol) == (
        "AnalystAgent", "claude-opus-4-8", 12, 3, "baseline")


def test_execute_records_one_entry_per_call():
    stub = _StubExecutor()
    gk = Gatekeeper(executor=stub)
    for _ in range(3):
        gk.execute("m", [{"role": "user", "content": "x"}], agent="A")
    assert len(gk.usage_ledger.entries) == 3
    assert stub.calls == 3
