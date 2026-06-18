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

\+ One seam to mock in tests. The **`main.py`** import boundary is enforced mechanically by
`tests/test_main_cli.py::test_src_main_imports_only_the_sdk_layer` (it may not import
`agents/`, `graphops/`, `vault/`, `metrics/`), and `tests/test_no_api_client_in_agents.py`
mechanically enforces that **agents import no API/HTTP client** (the safety-critical boundary).
Caveat (corrected 2026-06-18): there is **no** test forbidding `agents/` from importing
`graphops/`/`vault/`/`metrics/`, and four agents do import a few **stateless** helpers/error
types directly (`bug_localizer`→`graphops.loader`; `graph_agent`/`loop_wiring`→`graphops.errors`,
`metrics.graph_diff`/`load_shift`/`iteration_report`; `stop_evaluator`→`metrics.graph_diff`/`load_shift`).
These carry no LLM/git/state side-effects, but the agent→SDK-only boundary is therefore a
convention for stateful operations, not a fully mechanically-enforced rule for pure helpers.
− The facade risks exceeding the 150-line cap; it therefore delegates to internal
modules and keeps only dispatch (**zero-logic CLI constraint**: `src/main.py` stays
argparse-only forever).
