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

To show the savings are not an artifact of a 5-file toy, the **headline scale study** repeats the
measurement **live** on the class-bearing PDF-listed BugsInPy repo **httpie**, with **real provider
token counts** (the gatekeeper's recorded `input_tokens`, not a `chars//4` estimate) over **six**
reverse-engineering questions: graph-scoped retrieval (the AST class map + the one focused module)
saves a mean **79.68% ± 7.91%** input tokens (range 67.7–87.8%), cutting files read **13 → 2** and
cycles **13 → 1**, with **6/6** correct guided localization — **above the lecture's 70% target**.
Details: `docs/metrics/TOKEN_STUDY_HTTPIE.md` (`metrics/out/token_study_httpie.json`). The two studies
are complementary: buggy-python is the conservative floor, httpie is the live scale result; neither is
blended into the other.
