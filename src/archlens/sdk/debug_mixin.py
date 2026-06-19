"""Debug-demo SDK flow: graph-first bug localization plus repair evidence."""

import json
from pathlib import Path

from ..agents.bug_localizer import localize_import_failure

_TOKEN_STUDY = Path("metrics/out/debug_token_study.json")


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
            "Fix patch: deliverables/buggy-python-fix.patch",
            f"Bug report: {_display(report)}",
            f"Obsidian localization: {_display(loc_page)}",
            f"Obsidian repair: {_display(repair_page)}",
            "Token study: metrics/out/debug_token_study.json",
            f"Verification: {_verify_buggy_python()}",
        ])
        return "\n".join(lines)

    def submission_demo(self) -> str:
        """Return the one-command EX04 evidence summary for graders."""
        lines = [
            "EX04 Submission Demo",
            "Target repo: https://github.com/andela/buggy-python",
            "Authoritative graph: artifacts/buggy-python-graph.json",
            "Graph report: artifacts/buggy-python-GRAPH_REPORT.md",
            "Obsidian vault: obsidian/index.md and obsidian/hot.md",
            "",
            "Agent workflow:",
            "  RepoAgent -> GraphAgent -> BugLocalizer/BugHunterAgent -> RefactorAgent -> QAAgent -> MetricsAgent",
            "  Framework: LangGraph StateGraph, documented in docs/PRD_agent_orchestration.md",
            "",
            "Bug localization:",
            self.debug_demo(),
            "",
            "Repair evidence:",
            "  Patch: deliverables/buggy-python-fix.patch",
            "  Report: deliverables/BUG_REPORT.md",
            "  Before/after architecture snapshot: deliverables/BUG_REPORT.md section 5",
            "",
            "Token comparison:",
            *_token_comparison(),
            "  Explanation: docs/metrics/SAVINGS_EXPLANATION.md",
            "",
            "Verification commands:",
            "  uv run python src/main.py analyze",
            "  uv run pytest --cov=src --cov-branch",
        ]
        return "\n".join(lines)


def _token_comparison() -> list[str]:
    """Format the naive-vs-graph token lines from the committed study (no hardcoded literals)."""
    if not _TOKEN_STUDY.is_file():
        return [f"  (token study artifact absent: {_TOKEN_STUDY.as_posix()})"]
    study = json.loads(_TOKEN_STUDY.read_text(encoding="utf-8"))
    naive, guided = study["naive"], study["graph_guided"]
    return [
        f"  Naive: {naive['input_tokens']} input tokens, {naive['files_read']} files/units, "
        f"{naive['iterations']} cycles",
        f"  Graph-guided: {guided['input_tokens']} input tokens, {guided['files_read']} files/units, "
        f"{guided['iterations']} cycle(s)",
        f"  Savings: {study['token_savings_pct']}% input tokens, "
        f"{study['files_reduction_pct']}% fewer files (target_met=false; small repo)",
    ]


def _verify_buggy_python() -> str:
    repo = Path("runs/buggy-python")
    if not (repo / "main.py").is_file():
        return "skipped; clone absent, see deliverables/BUG_REPORT.md"
    return "clone present; run tests/debug/test_buggy_python_entry.py for harness verification"


def _display(path: Path) -> str:
    return path.as_posix()
