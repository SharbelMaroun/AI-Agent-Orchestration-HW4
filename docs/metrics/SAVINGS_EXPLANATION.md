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
