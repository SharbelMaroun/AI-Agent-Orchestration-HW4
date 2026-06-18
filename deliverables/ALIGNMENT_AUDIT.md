# Alignment Audit - EX04 Requirements

Version: 1.00 | Course: AI Agent Orchestration - HW4 / EX04

## Target

Submitted repository: `https://github.com/andela/buggy-python`

This is one of the PDF-listed base repositories and is used as the single target for the submitted
reverse-engineering and debugging story.

## Requirement Coverage

| Requirement | Status | Evidence |
|---|---|---|
| Choose a PDF-listed repository | PASS | `config/setup.json`, `docs/REPO_SELECTION.md` |
| Build a graph representation | PASS | `artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md` |
| Use Obsidian-style navigation | PASS | `obsidian/index.md`, `obsidian/hot.md`, `obsidian/suspects.md` |
| Reverse engineer architecture | PASS | `deliverables/ARCHITECTURE.md`, `obsidian/architecture.md` |
| Provide OOP/class view | PASS | `deliverables/CLASS_SCHEMA.md`; target has no classes |
| Identify a bug | PASS | `deliverables/BUG_REPORT.md`, `obsidian/localization.md` |
| Explain root cause | PASS | `deliverables/BUG_REPORT.md` sections 2-3 |
| Repair code behavior | PASS | `deliverables/BUG_REPORT.md` fix table and diff |
| Verify failing-to-passing path | PASS | `deliverables/BUG_REPORT.md` section 4, `tests/debug/test_buggy_python_entry.py` |
| Use graph-guided agentic AI | PASS | `src/archlens/agents/bug_localizer.py`, `src/archlens/sdk/debug_mixin.py` |
| Compare token efficiency | PASS | `metrics/out/debug_token_study.json`, `docs/metrics/GRAPH_VS_CODE.md` |
| Answer research questions | PASS | `obsidian/findings.md` |
| Provide README run instructions | PASS | `README.md` |

## Graph-Guided Debugging Claim

The failing import is:

```text
ImportError: cannot import name 'lambda_array' from 'snippets'
```

The graph route is:

```text
main.py -> snippets/__init__.py -> snippets/loop.py
```

Because `snippets/__init__.py` is the re-export hub, the graph identifies it as the first file to
inspect and fix. This is confirmed by `uv run python src/main.py debug-demo`.

## Token-Efficiency Claim

| Metric | Naive | Graph-guided |
|---|---:|---:|
| Input tokens | 802 | 685 |
| Files / units read | 5 | 2 |
| Investigation cycles | 2 | 1 |

The graph-guided path saves 14.59% input tokens on this small target and reduces files/units read by
60%.

## Known Limits

The target is intentionally small, so the token saving is not dramatic. The stronger demonstrated
benefit is navigation quality: the graph routes the investigation directly to the package hub instead
of requiring a linear scan of every file.
