# Findings - Research Questions (EX04)

The eight assignment research questions, answered for the target **`andela/buggy-python`** from the
graph investigation. This is the Obsidian-surface answer set; the same questions are answered in
`../README.md` and `../reports/RESEARCH_QUESTIONS.md`. Evidence links point into the vault.

## Q1 - What Is The Actual Architecture, And What Was Not Obvious?

A thin entry harness (`main.py`) over a **single package** (`snippets/`) fronted by a **re-export hub**
(`snippets/__init__.py`) that fans out to three independent leaf modules (`loop.py`, `io.py`,
`foobar.py`). What a file listing does not show: the package is a star around one hub, and the failure
is a chain, not five unrelated bugs. See [[architecture]] and [[index]].

## Q2 - Which Components Are The Most Central?

By graph centrality on the import graph: **`snippets/__init__.py` (degree 9)** is #1, followed by
`main.py` and `snippets/io.py`. The ranking is read from the graph; see [[hot]].

## Q3 - Where Are The Complex Focal Points / God Nodes?

The re-export hub `snippets/__init__.py` is the **God Node / Single Point of Failure**: every imported
symbol routes through it, so a single defect blocks the program. `io.py` is a secondary bottleneck
because it concentrates the loan-calculation logic and several defects. See [[suspects]].

## Q4 - How Can Block Schema And OOP Structure Be Extracted?

From the graph's `imports`, `re_exports`, and `contains` edges: communities become the block diagram,
and module/function dependency edges become the structural view. `buggy-python` is procedural
(0 classes), so an honest UML class diagram is empty. See [[architecture]].

## Q5 - How Was The Bug Identified?

The `BugLocalizer` agent resolved the failing symbol `lambda_array` to the hub from graph structure,
nominating `snippets/__init__.py` as the prime suspect. Steps: entry -> hub -> leaf. Root cause:
commented-out re-exports in the hub, then JS-isms in `loop.py`, dict/operator/typo defects in `io.py`,
and a mutable-default-argument bug in `foobar.py`. See [[localization]], [[suspects]], [[repair]].

## Q6 - What Was The Advantage Of Graph + Obsidian?

The graph routed the investigation straight to the hub instead of reading the package top-to-bottom.
Measured on the same question ("which file must be fixed first?"): **2 files/units read instead of
5** and **1 investigation cycle instead of 2**. See [[tests]] and Q7.

## Q7 - How Did The Graph-Oriented Agent Save Tokens?

Committed debug study (`../metrics/out/debug_token_study.json`): graph-guided localization used
**685 input tokens vs 802 naive input tokens (14.59% fewer)**, read **2 files/units instead of 5**,
and reached the first fix site in **1 cycle instead of 2**. Both approaches localize the correct first
fix site, but the graph path gets there with less reading.

The mechanism: read the vault `index` first, then ranked pages and a subgraph slice; do not dump all
source into context. This is the hub-first, short-context discipline from the lecture.

## Q8 - What Improvements / Extensions / Agent Mechanisms Did We Add?

The headline original extension is the **graph-first `BugLocalizer` agent**
(`../src/archlens/agents/bug_localizer.py`, `sdk.localize_bug`). Beyond that: orphan-component
detection, unimplemented-requirement audit support, SPOF and bridge analysis, centrality ranking,
before/after graph diff support, and sensitivity/variance studies. Full write-up in `../README.md`
and `../deliverables/ALIGNMENT_AUDIT.md`.

---

**Navigation:** back to [[index]] - diagrams in [[architecture]] - verification in [[tests]].
