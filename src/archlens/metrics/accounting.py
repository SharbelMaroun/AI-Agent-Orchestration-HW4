"""Per-agent and per-model token/cost accounting (task 12.028).

Aggregates a TokenLedger into per-agent and per-model breakdown rows plus a grand total,
costing every entry through the setup.json pricing table.
"""

from dataclasses import dataclass

from ..shared.config import SetupConfig, load_setup
from .cost import entry_cost
from .ledger import TokenLedger

GRAND_TOTAL_KEY = "TOTAL"


@dataclass(frozen=True)
class AccountRow:
    """Aggregated token and dollar totals for one key (an agent, a model, or the grand total)."""

    key: str
    input_tokens: int
    output_tokens: int
    usd_cost: float

    @property
    def total_tokens(self) -> int:
        """Input plus output tokens for this row."""
        return self.input_tokens + self.output_tokens


def _group(ledger: TokenLedger, attr: str, setup: SetupConfig) -> list[AccountRow]:
    acc: dict[str, list] = {}
    for entry in ledger.entries:
        bucket = acc.setdefault(getattr(entry, attr), [0, 0, 0.0])
        bucket[0] += entry.input_tokens
        bucket[1] += entry.output_tokens
        bucket[2] += entry_cost(entry, setup)
    return [AccountRow(key, *vals) for key, vals in sorted(acc.items())]


def by_agent(ledger: TokenLedger, setup: SetupConfig | None = None) -> list[AccountRow]:
    """Per-agent breakdown rows, sorted by agent name."""
    return _group(ledger, "agent", setup or load_setup())


def by_model(ledger: TokenLedger, setup: SetupConfig | None = None) -> list[AccountRow]:
    """Per-model breakdown rows, sorted by model id."""
    return _group(ledger, "model", setup or load_setup())


def grand_total(ledger: TokenLedger, setup: SetupConfig | None = None) -> AccountRow:
    """Single row summing every entry's tokens and cost."""
    cfg = setup or load_setup()
    return AccountRow(GRAND_TOTAL_KEY, ledger.total_input(), ledger.total_output(),
                      sum(entry_cost(entry, cfg) for entry in ledger.entries))
