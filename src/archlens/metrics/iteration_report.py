"""Per-iteration report generator: before/after metrics table + decision log (task 11.044).

Writes reports/iteration_<NN>.md in the PRD_improvement_loop §9 format — a metrics table keyed
to the stop conditions and a decision log recording the verdict and evidence citation.
"""

from pathlib import Path

_HEADER = "| Metric | Before | After | Delta | Stop condition |"
_SEP = "|---|---|---|---|---|"


def _delta(row: dict):
    before, after = row["before"], row["after"]
    if isinstance(before, int | float) and isinstance(after, int | float):
        return after - before
    return row.get("delta", "")


def _table(rows) -> str:
    lines = [_HEADER, _SEP]
    for row in rows:
        lines.append(f"| {row['metric']} | {row['before']} | {row['after']} | "
                     f"{_delta(row)} | {row.get('sc', '')} |")
    return "\n".join(lines)


def _render(iteration: int, fix: dict, rows, decision: dict) -> str:
    return "\n".join([
        f"# Iteration {iteration:02d} — {fix.get('fix_id', '')}",
        "",
        f"- Priority: {fix.get('priority', '')}",
        f"- Branch: {fix.get('branch', '')}",
        f"- Evidence: {fix.get('evidence', '')}",
        "",
        "## Before/After Metrics",
        "",
        _table(rows),
        "",
        "## Decision Log",
        "",
        f"- Decision: {decision.get('decision', '')}",
        f"- Deciding condition: {decision.get('condition', '')}",
        f"- Evidence citation: {decision.get('citation', '')}",
    ]) + "\n"


def iteration_report(output_dir, iteration: int, fix: dict, rows, decision: dict) -> Path:
    """Write reports/iteration_<NN>.md and return its path."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"iteration_{iteration:02d}.md"
    path.write_text(_render(iteration, fix, rows, decision), encoding="utf-8")
    return path
