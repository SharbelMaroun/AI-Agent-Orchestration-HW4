# With vs Without Graphify — Tokens AND Quality

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)

A reproducible evaluation of the lecture's core claim (L07 §6–9): the LLM should reason from the
**graph** (targeted retrieval), not from the **code**. For each top bottleneck the agents detect, the
SAME architecture question is answered twice — once from the node's **graph neighbourhood** (with
Graphify), once from its **full source module** (without it) — then an LLM judge rates both 1–5 for
correctness/specificity. Tokens are read back from the gatekeeper ledger, so they are the **flow's
real usage**, not estimates.

Code: `src/archlens/metrics/graph_vs_code.py` (via `sdk.compare_graph_vs_code`). Reproduce:

```bash
uv run python scripts/compare_graph_vs_code.py [graph.json] [repo_path] [top_k]
# defaults: runs/run/target/graphify-out/graph.json  runs/run/target  3   (needs a live key in .env)
```

## Live result — real GPT-4o, top 3 bottlenecks of httpie

| Node | Quality WITH | Quality WITHOUT |
| --- | :---: | :---: |
| `utils_init_http` | 5 | 4 |
| `httpie_context_environment` | 5 | 4 |
| `utils_init_mockenvironment` | 4 | 5 |

| Metric | **With Graphify** (graph) | **Without Graphify** (full source) |
| --- | ---: | ---: |
| **Total tokens** (real) | **1,322** | **8,102** |
| **Avg quality** (judge 1–5) | **4.67** | **4.33** |

**Result: 83.7% fewer tokens with Graphify, at equal-or-better quality (4.67 vs 4.33).** Reading the
whole module costs ~6× more tokens and did **not** improve the diagnosis — the graph neighbourhood
(degree, callers, dependencies) already carries what the model needs to name the coupling / god-object
/ single-point-of-failure and propose the split. (The judge itself spent 892 tokens.)

## Relation to the formal economics

This is the *agent-level, live* echo of the project's full token-economics study (naive full-context
baseline vs Graphify-assisted retrieval over 10 standard questions): **1,368,538 → 39,950 tokens =
97.08% savings** (`metrics/out/token_metrics.json`, measured live on gpt-4.1-mini, $0.58). The
live numbers above independently confirm the same effect (~84%) **and** add a quality dimension the
formal study did not measure.
