"""Cost calculator — converts token usage to USD via the setup.json pricing table (task 12.013).

Prices are read from config/setup.json under the ``pricing`` key; nothing is hardcoded.
An unknown model raises ConfigError rather than silently costing zero.
"""

from ..shared.config import ModelPricing, SetupConfig, load_setup
from ..shared.exceptions import ConfigError
from .ledger import TokenLedger
from .ledger_model import TokenLedgerEntry

_PER_MTOK = 1_000_000


def _model_pricing(model: str, setup: SetupConfig) -> ModelPricing:
    price = setup.pricing.get(model)
    if price is None:
        raise ConfigError(f"no pricing configured for model {model!r}",
                          source_context="config/setup.json")
    return price


def entry_cost(entry: TokenLedgerEntry, setup: SetupConfig | None = None) -> float:
    """USD cost of one ledger entry, from its model's per-MTok pricing."""
    cfg = setup if setup is not None else load_setup()
    price = _model_pricing(entry.model, cfg)
    return (entry.input_tokens * price.input_per_mtok
            + entry.output_tokens * price.output_per_mtok) / _PER_MTOK


def ledger_cost(ledger: TokenLedger, setup: SetupConfig | None = None) -> float:
    """Total USD cost across every entry in a ledger."""
    cfg = setup if setup is not None else load_setup()
    return sum(entry_cost(entry, cfg) for entry in ledger.entries)
