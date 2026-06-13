# ADR-008 — `hot.md` content definition

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

The course mandates `hot.md` in the vault (L07 §11 Core Task 2) but never defines its
content. The authoritative spec is `docs/PRD_graph_pipeline.md` §7.1; this ADR records
the decision and rationale for the grader.

## Decision

`hot.md` contains exactly three sections, regenerated on every Graphify run:

1. **Top-10 hot nodes** — ranked by betweenness centrality, degree as tiebreaker,
   each with a wikilink into `wiki/`;
2. **Entry points** — `__main__` blocks, CLI scripts, exported APIs;
3. **Anomalies needing review** — AMBIGUOUS edges and unresolved contradictions.

Measurable qualification criteria: a node is "hot" iff it ranks in the top 10 by
betweenness (tiebreak: higher degree, then lexicographic id). The whole file respects
a **≤ 120-line budget** and is ordered so an LLM reading only `index.md` + `hot.md`
sees the load-bearing elements first.

## Alternatives

- **Config-driven N instead of Top-10** — rejected: a fixed, graded artifact beats a
  tunable one; 10 fits the 120-line budget with headroom.
- **Degree-ranked instead of betweenness-ranked** — rejected: betweenness captures
  mandatory-path risk (bottlenecks), the thing reviewers must see first.

## Consequences

\+ Directly serves the token-economy goal (smallest high-signal context) and the
"correct-file identification" before/after metric.
− The definition is ours, not the course's; this ADR documents the rationale.
