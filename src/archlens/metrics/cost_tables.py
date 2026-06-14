"""Table-4-style per-model cost table generator (task 12.034).

Renders a markdown cost table (model, input/output tokens, per-MTok prices, total USD) with a
grand-total row last, and writes it to docs/metrics/COST_TABLES.md.
"""

from pathlib import Path

from ..shared.config import SetupConfig, load_setup
from .accounting import by_model, grand_total
from .ledger import TokenLedger

COST_TABLES_MD = Path("docs/metrics/COST_TABLES.md")
_HEADER = "| model | input tokens | output tokens | $/MTok in | $/MTok out | total $ |"
_SEP = "|---|---|---|---|---|---|"
_DOC_HEADER = "# Cost Tables\n\nVersion: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)"


def render_cost_table(ledger: TokenLedger, setup: SetupConfig | None = None) -> str:
    """Render the per-model cost table as markdown, totals row last."""
    cfg = setup or load_setup()
    lines = [_HEADER, _SEP]
    for row in by_model(ledger, cfg):
        price = cfg.pricing[row.key]
        lines.append(f"| {row.key} | {row.input_tokens} | {row.output_tokens} | "
                     f"{price.input_per_mtok} | {price.output_per_mtok} | {row.usd_cost:.4f} |")
    total = grand_total(ledger, cfg)
    lines.append(f"| **TOTAL** | {total.input_tokens} | {total.output_tokens} | — | — | "
                 f"{total.usd_cost:.4f} |")
    return "\n".join(lines)


def write_cost_table(ledger: TokenLedger, path: str | Path = COST_TABLES_MD,
                     setup: SetupConfig | None = None) -> Path:
    """Write the rendered cost table (with the house doc header) to ``path``."""
    cfg = setup or load_setup()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"{_DOC_HEADER}\n\n{render_cost_table(ledger, cfg)}\n", encoding="utf-8")
    return target
