"""Per-module coverage-target gate reading reports/coverage.json (task 13.051).

Targets: gatekeeper >= 90, sdk >= 95, agents >= 85, graphops >= 85 (percent of statements).
Exits non-zero when any package is below its target. Generate the input first with:
    uv run pytest --cov=archlens --cov-report=json:reports/coverage.json
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVERAGE_JSON = ROOT / "reports" / "coverage.json"
TARGETS = {"gatekeeper": 90.0, "sdk": 95.0, "agents": 85.0, "graphops": 85.0}


def _package_coverage(data: dict) -> dict[str, float]:
    totals: dict[str, list[int]] = {pkg: [0, 0] for pkg in TARGETS}
    for filename, info in data["files"].items():
        parts = Path(filename).parts
        for pkg in TARGETS:
            if pkg in parts:
                summary = info["summary"]
                totals[pkg][0] += summary["covered_lines"]
                totals[pkg][1] += summary["num_statements"]
    return {pkg: (100.0 * cov / stmts if stmts else 100.0)
            for pkg, (cov, stmts) in totals.items()}


def main() -> int:
    if not COVERAGE_JSON.is_file():
        raise SystemExit(f"missing {COVERAGE_JSON}; run pytest with --cov-report=json first")
    data = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    actual = _package_coverage(data)
    failures = []
    for pkg, target in TARGETS.items():
        got = actual[pkg]
        flag = "OK" if got >= target else "LOW"
        print(f"{pkg:<12} {got:6.2f}% (target {target:.0f}%) {flag}")
        if got < target:
            failures.append(pkg)
    if failures:
        print(f"FAIL: below target: {failures}")
        return 1
    print("all per-module coverage targets met")
    return 0


if __name__ == "__main__":
    sys.exit(main())
