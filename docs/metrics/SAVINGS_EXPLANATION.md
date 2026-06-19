# Savings Explanation

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04)

The submitted target, `andela/buggy-python`, is intentionally small. For the debug-localization task,
the graph-guided path used **685 input tokens** versus **802 input tokens** for naive source reading,
which is **14.59% fewer input tokens**.

This does not reach the lecture's 70% headline savings target because the whole target repository is
tiny: the naive path only needs five source files. The stronger measured benefit is navigation:

| Metric | Naive | Graph-guided |
|---|---:|---:|
| Input tokens | 802 | 685 |
| Files / units read | 5 | 2 |
| Investigation cycles | 2 | 1 |

The graph still demonstrates the required mechanism: it routes the agent from `main.py` to the
`snippets/__init__.py` re-export hub before opening every leaf module.

## Scale study clears the 70% target

To show the savings are not an artifact of a 5-file toy, a **rigorous scale study** repeats the
measurement on a medium class-bearing repo, `psf/requests` (19 modules), with a **real tokenizer**
(`tiktoken o200k_base`) over **six** reverse-engineering questions: the naive full-source context
(**49,592 tokens**) vs graph-scoped retrieval saves **85.8% ± 5.48%** input tokens (range
77.9–94.4%) — **above the lecture's 70% target**. Details: `docs/metrics/TOKEN_STUDY_REQUESTS.md`
(`metrics/out/token_study_requests.json`). The two studies are complementary: buggy-python is the
conservative floor, requests is the scale result; neither is blended into the other.
