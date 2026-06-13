# ADR-009 — SQLite checkpointer + interrupt-based human approval

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

Irreversible refactors require explicit human approval (Part B guardrails: read-only
auto / reversible with undo path / irreversible needs approval), and runs must
survive restarts.

## Decision

LangGraph **SQLite checkpointer** (`SqliteSaver`, `checkpoints.db`,
`thread_id` = run id) with **`interrupt_before=["RefactorAgent"]`** as the approval
interrupt point — every RefactorAgent source modification pauses for explicit human
approval; approvals append to `AgentState.approvals` and persist across sessions;
denied → the finding is skipped; there is **no timeout auto-grant**.

## Alternatives

- **In-memory checkpointer** — rejected: no kill/resume demo (an acceptance
  criterion), no audit trail after a crash.
- **Auto-approve reversible-looking refactors** — rejected: the project classifies
  every source modification as irreversible-tier (PRD_agent_orchestration §5).

## Consequences

\+ Kill/resume is demonstrable; the approval audit trail satisfies the guardrail
requirement.
− Single-writer SQLite is fine locally but would need replacing for multi-user
deployment (out of scope).
