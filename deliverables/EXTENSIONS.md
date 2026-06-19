# Extensions & Original Ideas (EX04 §5.6)

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04)

The assignment baseline is "locate and fix one bug, graph-first." Beyond that minimum, this submission
adds the following. Each item is implemented and test-covered (not just described), with file and test
citations. The first three are original contributions of the group; the last three implement the
PDF's own suggested example extensions (§5.6) on top of the real target graph.

## Original contributions (beyond the suggested baseline)

### E1 — Graph-first BugLocalizer that names the fix site without reading source
`src/archlens/agents/bug_localizer.py` resolves a failing symbol to its definition node, finds the
importers and the package re-export hub they route through, and nominates the max-degree hub as the
prime suspect — using **only** the dependency graph. The LLM explanation prompt is explicitly
constrained to "use ONLY this dependency-graph evidence (no source code)" (`prompts/localizer.md`,
`PB-localizer-01`). On `andela/buggy-python` it nominates `snippets/__init__.py` (degree 9) as the
first fix site before any leaf module is opened.
*Tests:* `tests/agents/test_bug_localizer.py` (nominates the hub, not the leaf, from graph data alone).

### E2 — Improvement loop with five real stop conditions and a hard cap
`src/archlens/agents/loop_controller.py` wires `select_fix → apply_fix → regraph_diff → evaluate` as a
LangGraph StateGraph; `src/archlens/agents/stop_evaluator.py` composes five Part-C signals
(dependency-loss, modularity-improved, new-isolates, tests-green, token-budget) plus a hard
`MAX_LOOP_ITERATIONS=5` cap into a STOP/CONTINUE verdict, and re-runs Graphify after every change to
measure the graph delta.
*Tests:* `tests/test_loop_convergence.py` (converges in 2 iterations via the production evaluator with
real git branching), `tests/test_stop_eval.py`, `tests/test_stop_conditions.py`, `tests/test_graph_node_diff.py`.

### E3 — Human-in-the-loop guardrail on irreversible source modifications
Every RefactorAgent source change is classified irreversible-tier and routed through an `ApprovalAgent`
that raises a dynamic LangGraph `interrupt()`; the agent never writes without a recorded `granted`
approval (interactive runs await a human, the headless loop uses a recorded auto-approval policy).
*Files:* `src/archlens/agents/{guardrails,approval,refactor_agent,supervisor}.py`.
*Tests:* `tests/test_refactor_guardrail.py` (pauses before any write; every applied refactor has a
recorded grant — §12.4).

## PDF-suggested example extensions, implemented on the target graph

### E4 — Centrality ranking of the bug-investigation hotspots
`obsidian/hot.md` ranks the candidate nodes by graph centrality (degree), produced from
`node_centrality` on the real `artifacts/buggy-python-graph.json` (hub `snippets/__init__.py` = degree
9, ranked #1) — the graph, not file reading, sets the investigation order.
*Tests:* `tests/graphops/test_centrality.py`.

### E5 — Orphan detection + automatic alignment-audit documentation
`src/archlens/graphops/orphan_detector.py` flags modules with no requirement linkage; it feeds
`src/archlens/vault/audit_doc.py`, which auto-writes `deliverables/ALIGNMENT_AUDIT.md` with
evidence-tagged sections (PRD-vs-implementation coverage gaps).
*Tests:* `tests/graphops/test_orphan_detector.py`, `tests/vault/test_audit_doc.py`.

### E6 — SPOF / bottleneck / bridge detection feeding refactor suggestions
`src/archlens/graphops/{spof,bridges,classify}.py` surface single-points-of-failure, hub-vs-bottleneck
verdicts, and structural bridges; the BugHunterAgent escalates the worst bottleneck to a VALIDATED,
cited finding that hands RefactorAgent a concrete, graph-derived target.
*Tests:* `tests/graphops/test_spof.py`, `tests/graphops/test_bridges.py`, `tests/graphops/test_classify.py`.

## Cross-references
- Research-question framing of these extensions: `reports/RESEARCH_QUESTIONS.md` Q8, `README.md` Q8,
  `obsidian/findings.md`.
- Token measurement tooling for the before/after study: `metrics/out/debug_token_study.json`,
  `scripts/compare_debug_tokens.py`, `scripts/build_token_metrics.py`.
