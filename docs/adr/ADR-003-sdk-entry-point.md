# ADR-003 — Single SDK entry point

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

Guidelines V3: ALL business logic only via the SDK; GUI/CLI layers must hold zero
logic.

## Decision

`src/archlens/sdk/sdk.py` (`ArchLensSDK`) exposes the complete public surface
(PLAN §4 class diagram). The CLI (`src/main.py`) and the agent nodes contain zero
business logic; agents are prompt+contract shells delegating to SDK methods.

## Alternatives

- **Per-module public APIs** — rejected: multiplies the mockable surface and violates
  the single-entry mandate.
- **Logic in CLI subcommands** — rejected: untestable through the SDK seam and an
  explicit Guidelines V3 violation.

## Consequences

\+ One seam to mock in tests; an import-boundary test (`agents/` and `main.py` may not
import `graphops/`, `vault/`, `metrics/` directly) enforces the rule mechanically.
− The facade risks exceeding the 150-line cap; it therefore delegates to internal
modules and keeps only dispatch (**zero-logic CLI constraint**: `src/main.py` stays
argparse-only forever).
