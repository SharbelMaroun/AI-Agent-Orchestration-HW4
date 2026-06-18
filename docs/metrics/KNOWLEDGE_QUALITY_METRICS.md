# Knowledge-Quality Metrics

Version: 1.02 | Course: AI Agent Orchestration - HW4 (EX04)

This file records the current knowledge-quality evidence for the single submitted target:
`andela/buggy-python`.

## Scope

- Source graph: `artifacts/buggy-python-graph.json`
- Human-readable graph report: `artifacts/buggy-python-GRAPH_REPORT.md`
- Investigation vault: `obsidian/`
- Machine-readable token result: `metrics/out/debug_token_study.json`
- Repair evidence: `deliverables/BUG_REPORT.md`

## Metrics

| Metric | Baseline | Graph-guided | Result |
|---|---:|---:|---|
| Input tokens | 802 | 685 | 14.6% fewer input tokens |
| Files / units read | 5 | 2 | 60% fewer files/units |
| Investigation cycles | 2 | 1 | One cycle to first fix site |
| Correct root-cause localization | `snippets/__init__.py` | `snippets/__init__.py` | Both correct; graph path is faster |

## Interpretation

The target is intentionally small, so the token delta is modest. The stronger benefit is navigation:
the graph points directly from the failing `main.py` import to the `snippets/__init__.py` re-export
hub, then to the implicated leaf modules. That is the graph/Obsidian advantage required by EX04.
