# With vs Without Graphify — Agent-Level Token Comparison

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)

A focused, reproducible demonstration of the lecture's core claim (L07 §6–9): the LLM should reason
from the **graph** (targeted retrieval), not by reading all the **code**. Same architecture question,
same model (`gpt-4o`), same target node — answered two ways.

Reproduce:

```bash
uv run python scripts/compare_graph_vs_code.py [graph.json] [repo_path]
# defaults: runs/run/target/graphify-out/graph.json  +  runs/run/target  (needs a live key in .env)
```

## Live result (real GPT-4o calls, httpie)

Target node: `utils_init_http` (`tests/utils/__init__.py`) — the highest in-degree hub.

| Approach | What the LLM saw | Input | Output | **Total** |
| --- | --- | ---: | ---: | ---: |
| **With Graphify** | the node's graph neighbourhood (degree, callers, dependencies) | 311 | 127 | **438** |
| **Without Graphify** (naive) | the node's full source module | 3096 | 135 | **3231** |

**Savings: 438 vs 3231 tokens → 86.4% fewer with Graphify**, for the same question and an equivalent
answer.

### With Graphify (graph context) — 438 tokens
> The main architectural problem with `utils_init_http` is that it has excessive in-degree,
> indicating it is highly coupled to numerous components… any change could have widespread
> implications… refactor to break it into smaller, more cohesive modules that adhere to the Single
> Responsibility Principle…

### Without Graphify (full source) — 3231 tokens
> The main architectural problem with this module is the lack of separation of concerns, resulting
> in a highly coupled and monolithic structure… decompose the module into smaller, more focused
> components… each class and function should focus on a single responsibility…

Both diagnoses agree (coupling / single-responsibility violation, split into cohesive modules); the
graph-based path reached it with **~7× fewer tokens**.

## How this relates to the formal economics

This is the *agent-level* echo of the project's full token-economics study, which compares a naive
full-context baseline against Graphify-assisted retrieval across 10 standard architecture questions:

| Protocol | Total input tokens | Per question |
| --- | ---: | ---: |
| Baseline (naive full-context) | 1,481,736 | ~148k |
| Graphify-assisted | 34,801 | ~3.4k |

**97.65% savings** (`metrics/out/token_metrics.json`). That study was measured in offline mock mode
with token estimates; the table above is **real, live GPT-4o** usage on a single question, which
independently confirms the same effect at ~86%.
