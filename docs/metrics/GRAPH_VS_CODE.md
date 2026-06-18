# With vs Without Graphify - Tokens AND Quality

Version: 1.01 | Course: AI Agent Orchestration - HW4 (EX04)

This evaluation compares answering the same architecture question from a node's Graphify
neighbourhood versus from the broader source context.

Code: `src/archlens/metrics/graph_vs_code.py` (via `sdk.compare_graph_vs_code`). Reproduce:

```bash
uv run python scripts/compare_graph_vs_code.py runs/run/target/graphify-out/graph.json runs/run/target 3
```

## Current BugsInPy Result

Committed artifact: `metrics/out/graph_vs_code.json`.

The project was retargeted to the PDF-listed BugsInPy repository and this comparison was
regenerated. The local run used the offline/canned response path, so the result is recorded as
inconclusive rather than as a live quality win.

| Node | Quality WITH | Quality WITHOUT |
| --- | :---: | :---: |
| `pysnooper_verify_my_function` | 0 | 0 |
| `ansible_verify_my_function` | 0 | 0 |
| `cookiecutter_verify_my_function` | 0 | 0 |

| Metric | With Graphify | Without Graphify |
| --- | ---: | ---: |
| Total tokens | 45 | 45 |
| Avg quality | 0.0 | 0.0 |

Result: 0.0% token savings in this offline proxy. A live-key rerun over a 10-question rubric is the
remaining work if the grader requires a full Part B quality study on the retargeted BugsInPy corpus.

## Historical Note

The earlier httpie development run measured 84.0% fewer tokens in this graph-vs-code comparison and
97.08% savings in the separate token-economics ledger. Those numbers remain development history, but
they are not claimed as BugsInPy-specific evidence.
