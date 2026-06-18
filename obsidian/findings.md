# Findings — Research Questions (EX04 §4)

The eight assignment research questions (§4), answered for the target **`andela/buggy-python`** from
the graph investigation. This is the Obsidian-surface answer set; the same questions are answered in
`../README.md` (§4 block) and `../reports/RESEARCH_QUESTIONS.md`. Evidence links point into the vault.

## Q1 — What is the actual architecture, and what was not obvious at first glance?
A thin entry harness (`main.py`) over a **single package** (`snippets/`) fronted by a **re-export hub**
(`snippets/__init__.py`) that fans out to three independent leaf modules (`loop.py`, `io.py`,
`foobar.py`). What a file listing does **not** show: the package is a star around one hub, and the
failure is a **chain** (one hub defect gating three leaf defects), not five unrelated bugs. See
[[architecture]] and [[index]].

## Q2 — Which components are the most central?
By graph centrality on the import graph: **`snippets/__init__.py` (degree 9)** is #1, followed by
`main.py` and `snippets/io.py` (degree 6). The ranking is read straight from the graph, not by reading
files — see [[hot]].

## Q3 — Where are the complex focal points / "God Nodes"?
The re-export hub `snippets/__init__.py` is the **God Node / Single Point of Failure**: every imported
symbol routes through it, so a single defect there blocks the whole program. `io.py` is a secondary
**bottleneck** (it concentrates the loan-calculation logic and its multiple defects). See [[suspects]].

## Q4 — How can block schema & OOP structure be extracted when docs are missing?
From the Graphify graph's `imports` / `re_exports` / `contains` edges, with **no upstream
documentation**: communities become the **block diagram**, and the module + function dependency
structure becomes the **OOP-level view**. `buggy-python` is procedural (0 classes), so an honest UML
class diagram is empty — the engineering structure view is the right substitute. Both diagrams are in
[[architecture]].

## Q5 — How was the bug identified, what was the root cause, and what were the steps?
**Graph-first** localization: the `BugLocalizer` agent resolved the failing symbol `lambda_array` to the
hub from graph structure alone (no source read), nominating `snippets/__init__.py` as the prime suspect.
Steps: **entry → hub → leaf**. Root cause: commented-out re-exports in the hub (the `ImportError`), then
JS-isms in `loop.py`, dict/operator/typo defects in `io.py`, and a mutable-default-argument bug in
`foobar.py`. See [[localization]], [[suspects]], [[repair]].

## Q6 — What was the advantage of the graph + Obsidian over linear file reading?
The graph routed the investigation **straight to the hub** instead of reading the package top-to-bottom.
Measured on the same question ("which file must be fixed first?"): **2 files read instead of 5 (−60%)**
and **1 investigation cycle instead of 2** — hub-first navigation (this vault's `index → hot → suspects`
path) avoids opening every file. See [[tests]] for how the fix is verified, and Q7 for the token figures.

## Q7 — How did the graph-oriented agent save tokens / reduce redundant reads?
Three committed studies (`../metrics/out/`):
- **Debug task** (`debug_token_study.json`): graph-guided **685 tokens vs 802 naive (−14.6%)**, 2 vs 5
  files, 1 vs 2 cycles — both localize the correct root cause.
- **Scale study** (`token_metrics.json`, httpie 2 033-node graph): **97.08% fewer tokens**
  (1 368 538 → 39 950), target (≥70%) met, real billed `gpt-4.1-mini`.
- **Live graph-vs-code** (`graph_vs_code.json`): **84.0% fewer tokens** (8 125 → 1 302) at **equal
  LLM-judge quality (5.0/5.0)**.

The mechanism: read the vault `index` first, then ≤3 ranked pages and a subgraph slice — never dump raw
source. This is the "hub-first, short-context" discipline (Lost-in-the-Middle mitigation).

## Q8 — What improvements / extensions / agent mechanisms did we add?
The headline original extension is the **graph-first `BugLocalizer` agent**
(`../src/archlens/agents/bug_localizer.py`, `sdk.localize_bug`) — it turns the graph itself into the
localizer, nominating the fix site from structure alone (see [[localization]]). Beyond that:
orphan-component detection, unimplemented-requirement (PRD-vs-code) gap detection, SPOF + bridge
analysis, centrality ranking, a real before/after graph diff, and OAT sensitivity + variance studies.
Full write-up in `../README.md` §5.6.

---
**Navigation:** back to [[index]] · diagrams in [[architecture]] · verification in [[tests]].
