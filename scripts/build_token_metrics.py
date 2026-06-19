"""Build metrics/out/token_metrics.json from the focused debug-localization study (reproducible).

The submission's CANONICAL token headline is the focused single-bug debug-localization study in
``metrics/out/debug_token_study.json`` (802 -> 685 input tokens, graph-guided vs naive). This script
re-emits that real study in the ``token_metrics.json`` schema (savings / per_agent / per_model /
cost_totals / amortization) so the headline is consistent across the CLI (``archlens tokens``), the
research notebook, and the docs — and is reproducible from committed data with no live API key. (The
broader ~97% knowledge-retrieval pilot lives separately in the committed ledgers + cost table.)

Run: uv run python scripts/build_token_metrics.py
"""

import json
from pathlib import Path

from archlens.metrics.amortization import compute_amortization
from archlens.shared.config import load_setup

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "metrics" / "out" / "debug_token_study.json"
OUT = ROOT / "metrics" / "out" / "token_metrics.json"


def build(study: dict, target_pct: float) -> dict:
    """Assemble the token_metrics schema from the debug study, internally consistent by construction."""
    baseline = study["naive"]["input_tokens"]
    assisted = study["graph_guided"]["input_tokens"]
    savings_pct = round((1 - assisted / baseline) * 100, 2)
    # The graph is already built before the queries, so there is no per-query build cost to amortize.
    amort = compute_amortization(0, baseline - assisted)
    total = baseline + assisted
    met = savings_pct >= target_pct
    return {
        "amortization": {
            "break_even_queries": amort.break_even_queries,
            "graph_build_tokens": amort.graph_build_tokens,
            "per_query_savings": amort.per_query_savings,
        },
        "cost_totals": {"input_tokens": total, "key": "TOTAL", "output_tokens": 0, "usd_cost": 0.0},
        "per_agent": [
            {"input_tokens": baseline, "key": "NaiveDebugReader", "output_tokens": 0, "usd_cost": 0.0},
            {"input_tokens": assisted, "key": "GraphGuidedBugLocalizer", "output_tokens": 0,
             "usd_cost": 0.0},
        ],
        "per_model": [
            {"input_tokens": total, "key": "offline-token-estimate", "output_tokens": 0,
             "usd_cost": 0.0},
        ],
        "savings": {"assisted_tokens": assisted, "baseline_tokens": baseline,
                    "savings_pct": savings_pct, "target_met": met},
        "target_met": met,
    }


def main() -> int:
    study = json.loads(STUDY.read_text(encoding="utf-8"))
    metrics = build(study, load_setup().metrics.savings_target_pct)
    OUT.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (savings {metrics['savings']['savings_pct']}% "
          f"target_met={metrics['target_met']} break_even={metrics['amortization']['break_even_queries']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
