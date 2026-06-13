# ADR-010 — Fix-priority taxonomy P1–P5 (one refactor per iteration)

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

Diff metrics must attribute graph changes to a specific fix, and the fix queue needs a
deterministic order a grader can audit.

## Decision

RefactorAgent applies exactly **one** VALIDATED finding per loop iteration; QA and
Graphify re-run before the next fix. Finding selection follows the canonical ordered
taxonomy:

| Priority | Fix class |
|---|---|
| **P1** | SPOF on a critical path |
| **P2** | Bottleneck split (god node only when classified bottleneck, not healthy hub) |
| **P3** | Split of modules > 150 effective lines |
| **P4** | Merge of validated duplicates (similarity ≥ 0.91, after manual check) |
| **P5** | PRD-vs-code misalignment |

## Alternatives

- **Batch multiple fixes per iteration** — rejected: destroys causal attribution in
  the stop-condition diff and complicates revert.
- **LLM-chosen order** — rejected: not deterministic; risk-driven order (SPOF first)
  is the course's own emphasis.

## Consequences

\+ Clean causal attribution in `stop_eval`; simple revert (one branch per fix).
− More iterations consumed within the cap of 5; acceptable since each accepted fix is
provably real.
