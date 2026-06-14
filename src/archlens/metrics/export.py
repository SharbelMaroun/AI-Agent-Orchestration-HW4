"""token_metrics.json export — assembles the full Phase 12 metrics schema (task 12.041).

Combines the baseline and assisted ledgers into one document with savings, per-agent and per-model
breakdowns, cost totals, amortization, and the target_met flag.
"""

import json
from dataclasses import asdict
from pathlib import Path

from ..shared.config import SetupConfig, load_setup
from .accounting import by_agent, by_model, grand_total
from .amortization import Amortization
from .ledger import TokenLedger
from .savings import Savings


def build_metrics(baseline: TokenLedger, assisted: TokenLedger, savings: Savings,
                  amortization: Amortization, setup: SetupConfig | None = None) -> dict:
    """Assemble the token_metrics document from both ledgers and the computed figures."""
    cfg = setup or load_setup()
    combined = TokenLedger(list(baseline.entries) + list(assisted.entries))
    return {
        "savings": asdict(savings),
        "target_met": savings.target_met,
        "amortization": asdict(amortization),
        "per_agent": [asdict(row) for row in by_agent(combined, cfg)],
        "per_model": [asdict(row) for row in by_model(combined, cfg)],
        "cost_totals": asdict(grand_total(combined, cfg)),
    }


def write_metrics_json(metrics: dict, path: str | Path) -> Path:
    """Write the metrics document as pretty-printed JSON."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    return target
