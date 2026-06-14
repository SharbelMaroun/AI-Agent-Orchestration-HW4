"""TokenLedger — append-only, filterable aggregate of TokenLedgerEntry rows (task 12.005)."""

from collections.abc import Iterable

from .ledger_model import TokenLedgerEntry

_FILTER_FIELDS = ("agent", "model", "protocol", "question_id")


class TokenLedger:
    """Append-only ledger with per-field filtering and token totals."""

    def __init__(self, entries: Iterable[TokenLedgerEntry] | None = None) -> None:
        self._entries: list[TokenLedgerEntry] = list(entries or ())

    def append(self, entry: TokenLedgerEntry) -> TokenLedgerEntry:
        """Append one entry and return it."""
        self._entries.append(entry)
        return entry

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> tuple[TokenLedgerEntry, ...]:
        """Immutable view of the recorded entries."""
        return tuple(self._entries)

    def total_input(self) -> int:
        """Sum of input tokens across all entries."""
        return sum(e.input_tokens for e in self._entries)

    def total_output(self) -> int:
        """Sum of output tokens across all entries."""
        return sum(e.output_tokens for e in self._entries)

    def total_tokens(self) -> int:
        """Sum of input plus output tokens across all entries."""
        return self.total_input() + self.total_output()

    def filter(self, **criteria: str) -> "TokenLedger":
        """Return a new ledger keeping entries that match every given field.

        Valid fields: agent, model, protocol, question_id. Unknown fields raise ValueError.
        """
        unknown = set(criteria) - set(_FILTER_FIELDS)
        if unknown:
            raise ValueError(f"unknown filter field(s): {sorted(unknown)}")
        kept = [e for e in self._entries
                if all(getattr(e, key) == value for key, value in criteria.items())]
        return TokenLedger(kept)
