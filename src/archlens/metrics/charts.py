"""Token-savings chart generation for the results notebook (task 12.043).

Renders two PNGs from the baseline and assisted ledgers: a per-question baseline-vs-assisted bar
chart and a cumulative-savings waterfall. Uses the headless Agg backend so it runs without a display.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)

from .ledger import TokenLedger  # noqa: E402

BAR_PNG = "baseline_vs_assisted_bar.png"
WATERFALL_PNG = "savings_waterfall.png"


def _by_question(ledger: TokenLedger) -> dict[str, int]:
    totals: dict[str, int] = {}
    for entry in ledger.entries:
        totals[entry.question_id] = totals.get(entry.question_id, 0) + entry.total_tokens
    return totals


def _save(out_dir, name: str) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def baseline_vs_assisted_bar(baseline: TokenLedger, assisted: TokenLedger, out_dir) -> Path:
    """Grouped bar chart of baseline vs assisted tokens for each question."""
    base, asst = _by_question(baseline), _by_question(assisted)
    questions = sorted(set(base) | set(asst))
    positions = range(len(questions))
    plt.figure(figsize=(11, 5))
    plt.bar([i - 0.2 for i in positions], [base.get(q, 0) for q in questions],
            width=0.4, label="baseline")
    plt.bar([i + 0.2 for i in positions], [asst.get(q, 0) for q in questions],
            width=0.4, label="assisted")
    plt.xticks(list(positions), questions, rotation=45)
    plt.ylabel("tokens")
    plt.title("Baseline vs assisted tokens per question")
    plt.legend()
    return _save(out_dir, BAR_PNG)


def savings_waterfall(baseline: TokenLedger, assisted: TokenLedger, out_dir) -> Path:
    """Cumulative token savings (baseline minus assisted) accumulated across the questions."""
    base, asst = _by_question(baseline), _by_question(assisted)
    questions = sorted(set(base) | set(asst))
    cumulative: list[int] = []
    running = 0
    for question in questions:
        running += base.get(question, 0) - asst.get(question, 0)
        cumulative.append(running)
    positions = range(len(questions))
    plt.figure(figsize=(11, 5))
    plt.plot(positions, cumulative, marker="o", color="green")
    plt.fill_between(positions, cumulative, alpha=0.2, color="green")
    plt.xticks(list(positions), questions, rotation=45)
    plt.ylabel("cumulative tokens saved")
    plt.title("Cumulative token savings (assisted vs baseline)")
    return _save(out_dir, WATERFALL_PNG)


def generate_charts(baseline: TokenLedger, assisted: TokenLedger, out_dir) -> tuple[Path, Path]:
    """Render both charts; return (bar_png_path, waterfall_png_path)."""
    return (baseline_vs_assisted_bar(baseline, assisted, out_dir),
            savings_waterfall(baseline, assisted, out_dir))
