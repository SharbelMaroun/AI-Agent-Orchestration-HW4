# ADR-005 — Improvement-loop stop conditions (Part C p21)

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

The improvement loop needs objective termination, not LLM self-assessment. **Part C
p21** supplies the diff metrics for judging whether a refactor genuinely improved the
architecture.

## Decision

`LoopState` computes five verdicts by diffing consecutive `graph.json` snapshots plus
QA output:

1. the targeted bottleneck node actually **lost dependencies** — not merely moved load
   (degree AND betweenness deltas);
2. **improved modularity** — fewer inter-community edges — or unchanged, for fixes
   that do not target coupling (P3/P5);
3. **no new isolated components**;
4. **all unit tests green**;
5. **ruff 0 violations**.

The five conditions are PER-FIX acceptance criteria: ALL five must hold for a fix to
be accepted. The RUN terminates on convergence, an empty fix queue, or the hard cap
of **5 iterations** (`MAX_LOOP_ITERATIONS = 5` in `src/archlens/shared/constants.py`).

## Alternatives

- **LLM judges its own refactor** — rejected: not reproducible, gameable.
- **Fixed iteration count only** — rejected: wastes iterations after convergence and
  cannot distinguish real improvement from load shuffling.

## Consequences

\+ Deterministic and reproducible from persisted snapshots; prevents "load shuffling"
being counted as improvement.
− Requires keeping every iteration's `graph.json` (disk cost accepted).
