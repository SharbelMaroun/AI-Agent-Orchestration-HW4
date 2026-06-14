"""Variance statistics across repeated runs: mean, std, coefficient of variation (task 15.008)."""

import csv
import statistics
from pathlib import Path


def variance_stats(runs: list[dict], metrics: list[str]) -> dict[str, dict]:
    """Per-metric mean, population std, and CV (std/mean, guarded) across the run records."""
    stats: dict[str, dict] = {}
    for metric in metrics:
        values = [float(run[metric]) for run in runs]
        mean = statistics.fmean(values)
        std = statistics.pstdev(values)
        stats[metric] = {"mean": mean, "std": std, "cv": (std / mean) if mean else 0.0}
    return stats


def write_summary_csv(stats: dict, path) -> Path:
    """Write a mean/std/cv CSV summary, one row per metric."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "mean", "std", "cv"])
        for metric, row in stats.items():
            writer.writerow([metric, row["mean"], row["std"], row["cv"]])
    return target
