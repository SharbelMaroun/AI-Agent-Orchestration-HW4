"""Token ledger with registerable hooks consumable by MetricsAgent (task 9.036).

Every completed call appends one LedgerEntry (model, input/output tokens, usd_cost); registered
hooks fire on each entry so MetricsAgent can stream usage without polling.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LedgerEntry:
    """One recorded LLM call's token usage and cost."""

    model: str
    input_tokens: int
    output_tokens: int
    usd_cost: float


class TokenLedger:
    """Append-only token ledger; registered hooks fire on each recorded entry."""

    def __init__(self):
        self._entries: list[LedgerEntry] = []
        self._hooks: list = []

    def register_hook(self, hook) -> None:
        """Register a callback(entry) invoked on every appended entry (e.g. MetricsAgent)."""
        self._hooks.append(hook)

    def record(self, model: str, input_tokens: int, output_tokens: int,
               usd_cost: float) -> LedgerEntry:
        """Append one entry and notify every registered hook."""
        entry = LedgerEntry(model, input_tokens, output_tokens, usd_cost)
        self._entries.append(entry)
        for hook in self._hooks:
            hook(entry)
        return entry

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        """An immutable view of the recorded entries."""
        return tuple(self._entries)

    def total_cost(self) -> float:
        """Sum of usd_cost across all entries."""
        return sum(entry.usd_cost for entry in self._entries)
