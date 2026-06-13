# ADR-007 — Evidence-ladder enforcement

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

Findings must be trustworthy enough to justify code-changing refactors (Part C
reading discipline: relation → confidence → source_file; "the graph is a map, not a
verdict").

## Decision

Every `Finding` carries an `EvidenceLevel` on the ladder
**OBSERVED → INFERRED → EXTRACTED → VALIDATED** and the citation triple
relation → confidence → source_file. The SDK rejects (schema validation) any finding
lacking the triple; the Supervisor routes to RefactorAgent **only at VALIDATED**.
Numeric thresholds:

- edge confidence range: **0.55–0.95**, enforced for every edge;
- EXTRACTED edges carry fixed confidence **0.95**;
- duplicate-logic findings require similarity **≥ 0.91** (and never auto-merge
  without manual check).

## Alternatives

- **Trust INFERRED/EXTRACTED findings for fixes** — rejected: a similarity edge alone
  must never trigger merge/delete (Part C); VALIDATED-only is the safe bar.
- **Free-text findings** — rejected: not machine-checkable, not gradeable.

## Consequences

\+ No uncited claim can trigger a code change; graders can trace every fix to a graph
edge and a source file.
− Some real bugs stall below VALIDATED; they are reported as findings without fixes.
