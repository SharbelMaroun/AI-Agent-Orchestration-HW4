"""Debug-demo SDK flow: graph-first bug localization plus repair evidence."""

from pathlib import Path

from ..agents.bug_localizer import localize_import_failure


class DebugDemoMixin:
    """Focused EX04 demonstration: graph -> agent localization -> repair evidence."""

    def debug_demo(self, graph="artifacts/buggy-python-graph.json",
                   failing_symbol: str = "lambda_array") -> str:
        """Return a runnable, assignment-aligned debugging workflow report."""
        graph_path = Path(graph)
        report = Path("deliverables/BUG_REPORT.md")
        loc_page = Path("obsidian/localization.md")
        repair_page = Path("obsidian/repair.md")
        loc = localize_import_failure(graph_path, failing_symbol)
        lines = [
            "EX04 Debug Demo",
            "Target repo: https://github.com/andela/buggy-python",
            f"Graphify graph: {_display(graph_path)}",
            "Obsidian vault: obsidian/index.md, obsidian/hot.md",
            "Agent workflow: BugLocalizer over graph neighbourhood",
            f"Failure: ImportError cannot import {loc.failing_symbol}",
            f"Suspect: {loc.suspect_file}",
            f"Suspect node: {loc.suspect}",
            "Graph evidence:",
        ]
        lines.extend(f"  - {item}" for item in loc.evidence)
        lines.extend([
            f"Root cause: {loc.root_cause}",
            "Fix summary: restore package re-exports; repair loop/io/foobar leaf defects",
            f"Bug report: {_display(report)}",
            f"Obsidian localization: {_display(loc_page)}",
            f"Obsidian repair: {_display(repair_page)}",
            "Token study: metrics/out/debug_token_study.json",
            f"Verification: {_verify_buggy_python()}",
        ])
        return "\n".join(lines)


def _verify_buggy_python() -> str:
    repo = Path("runs/buggy-python")
    if not (repo / "main.py").is_file():
        return "skipped; clone absent, see deliverables/BUG_REPORT.md"
    return "clone present; run tests/debug/test_buggy_python_entry.py for harness verification"


def _display(path: Path) -> str:
    return path.as_posix()
