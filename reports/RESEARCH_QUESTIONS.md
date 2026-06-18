# Research-Questions Report (EX04 §4)

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Target: `andela/buggy-python`

The eight §4 research questions, answered as a report. The same answers appear in the README (§4 block)
and in the Obsidian vault (`obsidian/findings.md`), satisfying the §4 rule that the questions be
expressed "in the README, in the reports, and in the Obsidian files." Numeric claims are backed by the
committed artifacts cited per answer.

| # | Research question | Answer (short) | Evidence |
|---|---|---|---|
| Q1 | Actual architecture; what was not obvious? | A thin `main.py` harness over one `snippets/` package fronted by a **re-export hub**; the bug is a **chain** (one hub defect gating three leaf defects), not five independent bugs. | `artifacts/buggy-python-graph.json`; `obsidian/architecture.md` |
| Q2 | Most central components? | `snippets/__init__.py` is #1 by centrality (**degree 9**); `main.py` and `io.py` follow (degree 6). | `obsidian/hot.md`; `artifacts/buggy-python-GRAPH_REPORT.md` |
| Q3 | Complex focal points / God Nodes? | The re-export hub `snippets/__init__.py` is the **God Node / SPOF** (all imports route through it); `io.py` is a secondary bottleneck. | `obsidian/suspects.md`; `src/archlens/graphops/spof.py` |
| Q4 | Extract block schema & OOP without docs? | Communities → **block diagram**; module/function dependency edges → **OOP-level view**. Target is procedural (0 classes), so a UML class diagram is empty and the dependency view is the honest substitute. | `obsidian/architecture.md`; `src/archlens/graphops/{mermaid_blocks,class_extractor}.py` |
| Q5 | How was the bug found; root cause; steps? | **Graph-first** localization (`BugLocalizer`) from the failing symbol to the hub, **no source read**; steps **entry → hub → leaf**. Root cause: commented re-exports + JS-isms (`loop.py`) + dict/operator/typo defects (`io.py`) + mutable default (`foobar.py`). | `obsidian/localization.md`; `deliverables/BUG_REPORT.md` |
| Q6 | Advantage of graph + Obsidian vs linear reading? | Routed straight to the hub: **2 files read vs 5 (−60%)** and **1 cycle vs 2**; hub-first navigation avoids reading every file. | `metrics/out/debug_token_study.json` |
| Q7 | How did the graph approach save tokens? | Debug task **685 vs 802 tokens (−14.6%)**; scale study **97.08% fewer** (1,368,538 → 39,950, target met); live graph-vs-code **84.0% fewer** at equal judge quality (5.0/5.0). | `metrics/out/{token_metrics,graph_vs_code,debug_token_study}.json` |
| Q8 | Improvements / extensions added? | Headline: the **graph-first `BugLocalizer` agent**. Also orphan/gap (PRD-vs-code) detection, SPOF + bridges, centrality ranking, before/after graph diff, OAT sensitivity + variance studies. | `src/archlens/agents/bug_localizer.py`; README §5.6 |

## Guiding understanding
The investigation followed the lecture's macro→drill-down method: read the graph for the central hub
and communities first, localize the failure to the hub from structure alone, then read source only for
the implicated leaves. The graph turned a single opaque `ImportError` into a ranked, cited entry → hub →
leaf chain — the value the assignment asks us to demonstrate over linear code reading.
