"""ISO/IEC 25010 quality-characteristic mapping for measured ArchLens metrics (task 15.012)."""

ISO_MAPPING = (
    ("Functional Suitability", "all-tests-green flag", "tests_green"),
    ("Performance Efficiency", "token savings %", "token_savings_pct"),
    ("Compatibility", "uv-only toolchain", "uv_only"),
    ("Usability", "Nielsen heuristics — severity>=3 findings resolved", "usability_resolved"),
    ("Reliability", "branch coverage %", "coverage_pct"),
    ("Security", "single-point-of-failure count", "spof_count"),
    ("Maintainability", "modularity (community count)", "modularity"),
    ("Portability", "Ruff violation count", "ruff_violations"),
)


def iso25010_table(metrics: dict) -> str:
    """Render a Markdown table mapping ISO/IEC 25010 characteristics to measured ArchLens metrics."""
    rows = ["| ISO/IEC 25010 Characteristic | ArchLens Metric | Measured |", "|---|---|---|"]
    for characteristic, metric_name, key in ISO_MAPPING:
        rows.append(f"| {characteristic} | {metric_name} | {metrics.get(key, '—')} |")
    return "\n".join(rows) + "\n"
