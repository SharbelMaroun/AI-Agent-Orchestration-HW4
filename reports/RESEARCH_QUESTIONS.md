# Research-Questions Report (EX04)

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04) | Target: `andela/buggy-python`

The eight EX04 research questions, answered as a report. The same answers appear in the README and in
the Obsidian vault (`obsidian/findings.md`), satisfying the rule that the questions be expressed in
the README, reports, and Obsidian files. Numeric claims are backed by the committed artifacts cited
per answer.

| # | Research question | Answer (short) | Evidence |
|---|---|---|---|
| Q1 | Actual architecture; what was not obvious? | A thin `main.py` harness over one `snippets/` package fronted by a **re-export hub**; the bug is a **chain** (one hub defect gating three leaf defects), not five independent bugs. | `artifacts/buggy-python-graph.json`; `obsidian/architecture.md` |
| Q2 | Most central components? | `snippets/__init__.py` is #1 by centrality (**degree 9**); `main.py` and `io.py` follow. | `obsidian/hot.md` (states degree 9); `artifacts/buggy-python-graph.json` (the source graph it is computed from) |
| Q3 | Complex focal points / God Nodes? | The re-export hub `snippets/__init__.py` is the **God Node / SPOF** because all imports route through it; `io.py` is a secondary bottleneck. | `obsidian/suspects.md`; `src/archlens/graphops/spof.py` |
| Q4 | Extract block schema and OOP without docs? | Communities become the **block diagram**; module/function dependency edges become the structural view. The target is procedural (0 classes), so the UML class diagram is intentionally empty. | `obsidian/architecture.md`; `deliverables/CLASS_SCHEMA.md` |
| Q5 | How was the bug found; root cause; steps? | **Graph-first** localization (`BugLocalizer`) moved from failing symbol to hub, then from hub to leaves. Root cause: commented re-exports plus leaf defects in `loop.py`, `io.py`, and `foobar.py`. | `obsidian/localization.md`; `deliverables/BUG_REPORT.md` |
| Q6 | Advantage of graph + Obsidian vs linear reading? | The graph routed straight to the hub: **2 files/units read vs 5** and **1 cycle vs 2**. | `metrics/out/debug_token_study.json` |
| Q7 | How did the graph approach save tokens? | Debug localization used **685 input tokens vs 802 naive input tokens**, a **14.59%** reduction on the submitted target. | `metrics/out/debug_token_study.json`; `docs/metrics/GRAPH_VS_CODE.md` |
| Q8 | Improvements / extensions added? | Headline: the **graph-first `BugLocalizer` agent**. Also included orphan/gap detection, SPOF and bridge analysis, centrality ranking, before/after graph diff support, and sensitivity/variance studies. | `src/archlens/agents/bug_localizer.py`; `deliverables/ALIGNMENT_AUDIT.md` |

## Guiding Understanding

The investigation followed the lecture's macro-to-drill-down method: read the graph for the central
hub and communities first, localize the failure to the hub from structure, then read source only for
the implicated leaves. The graph turned one opaque `ImportError` into a ranked, cited
entry-to-hub-to-leaf chain.
