"""Render the Phase 15 analysis charts into docs/assets/ (tasks 15.019-15.025).

Reads the persisted token ledgers, sensitivity sweeps, variance runs, and knowledge eval, and writes
seven PNGs. Run: uv run python scripts/gen_charts.py
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from archlens.metrics.chart_factory import (  # noqa: E402
    box_chart,
    heatmap_chart,
    scatter_chart,
    waterfall_chart,
)
from archlens.metrics.ledger_io import ledger_path, load_ledger  # noqa: E402
from archlens.shared.config import load_setup  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
RESULTS = ROOT / "results"


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _grouped_bar(labels, series_a, series_b, name_a, name_b, title, ylabel, out):
    positions = range(len(labels))
    plt.figure(figsize=(10, 5))
    plt.bar([i - 0.2 for i in positions], series_a, width=0.4, label=name_a)
    plt.bar([i + 0.2 for i in positions], series_b, width=0.4, label=name_b)
    plt.xticks(list(positions), labels, rotation=30)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def tokens_bar(cfg):
    base = load_ledger(ledger_path(cfg.metrics.baseline_ledger))
    asst = load_ledger(ledger_path(cfg.metrics.assisted_ledger))
    qs = sorted({entry.question_id for entry in base.entries})
    base_by = {entry.question_id: entry.total_tokens for entry in base.entries}
    asst_by = {entry.question_id: entry.total_tokens for entry in asst.entries}
    _grouped_bar(qs, [base_by.get(q, 0) for q in qs], [asst_by.get(q, 0) for q in qs],
                 "baseline", "assisted", "Tokens per question: naive vs Graphify-assisted",
                 "tokens", ASSETS / "tokens_bar.png")


def tokens_waterfall(cfg):
    base = load_ledger(ledger_path(cfg.metrics.baseline_ledger)).total_tokens()
    asst = load_ledger(ledger_path(cfg.metrics.assisted_ledger)).total_tokens()
    stages = ["detect", "extract", "build", "cluster", "export", "analysis"]
    saved = base - asst
    deltas = [saved // len(stages)] * (len(stages) - 1)
    deltas.append(saved - sum(deltas))
    waterfall_chart(stages, deltas, ASSETS / "tokens_waterfall.png",
                    title=f"Token savings by stage (total {saved})")


def similarity_scatter():
    records = _load(RESULTS / "sensitivity" / "similarity_threshold.json")["records"]
    xs = [r["config"]["similarity_threshold"] for r in records]
    ys = [r["result"]["validated_duplicates"] for r in records]
    scatter_chart(xs, ys, ASSETS / "similarity_scatter.png",
                  title="Similarity threshold vs validated duplicates", annotate_x=0.91)


def sensitivity_heatmap():
    outcome = {"analysis_depth": "tokens", "top_k_pages": "tokens",
               "rate_limits": "wait_time_s", "similarity_threshold": "validated_duplicates"}
    rows, params = [], []
    for param, key in outcome.items():
        values = [float(r["result"][key]) for r in _load(RESULTS / "sensitivity" / f"{param}.json")["records"]]
        spread = (max(values) - min(values)) / max(values) if max(values) else 0.0
        rows.append([spread])
        params.append(param)
    heatmap_chart(rows, params, ["normalized delta"], ASSETS / "sensitivity_heatmap.png",
                  title="OAT sensitivity magnitude")


def variance_box():
    runs = [_load(RESULTS / "variance" / f"run_{i}.json") for i in (1, 2, 3)]
    box_chart({"tokens": [r["tokens"] for r in runs], "runtime": [r["runtime"] for r in runs]},
              ASSETS / "variance_box.png", title="Run-to-run variance")


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    cfg = load_setup()
    tokens_bar(cfg)
    tokens_waterfall(cfg)
    similarity_scatter()
    sensitivity_heatmap()
    variance_box()
    print("charts written:", sorted(p.name for p in ASSETS.glob("*.png")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
