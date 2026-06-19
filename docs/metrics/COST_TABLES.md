# Cost Tables

Version: 1.01 | Course: AI Agent Orchestration — HW4 (EX04)

Billed cost of the **broad 10-question knowledge-retrieval pilot** (the ~97% study), measured live on
gpt-4.1-mini from `metrics/out/{baseline,assisted}_ledger.jsonl`. This is the cost of running both arms
of that pilot; it is distinct from the conservative focused debug-localization headline (14.59%,
`metrics/out/debug_token_study.json`), whose artifact records input tokens only.

| model | input tokens | output tokens | $/MTok in | $/MTok out | total $ |
|---|---|---|---|---|---|
| gpt-4.1-mini | 1393010 | 15478 | 0.4 | 1.6 | 0.5820 |
| **TOTAL** | 1393010 | 15478 | — | — | 0.5820 |
