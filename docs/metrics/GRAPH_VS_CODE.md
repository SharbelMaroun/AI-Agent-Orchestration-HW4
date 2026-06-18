# With vs Without Graphify - Tokens and Quality

Version: 1.02 | Course: AI Agent Orchestration - HW4 (EX04)

This evaluation compares the `andela/buggy-python` bug investigation in two modes:

- Naive: read the entry point plus all source files in `snippets/`.
- Graph-guided: read the Obsidian index/suspect notes derived from
  `artifacts/buggy-python-graph.json`.

Committed artifact: `metrics/out/debug_token_study.json`.

## Result

| Metric | Naive | Graph-guided |
|---|---:|---:|
| Input tokens | 802 | 685 |
| Files / units read | 5 | 2 |
| Investigation cycles | 2 | 1 |
| Correct first fix site | `snippets/__init__.py` | `snippets/__init__.py` |

On this small target, both approaches eventually find the correct root cause. The graph-guided path
is still more efficient: it reads 60% fewer files/units, uses 14.6% fewer input tokens, and reaches
the package re-export hub in one investigation cycle.
