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
`thread_id` = run id) for crash-resume, plus an approval gate realized as a
**dynamic `interrupt()` raised inside the ApprovalAgent node** (the supervisor routes
there whenever a finding's latest approval status is `pending`) — every RefactorAgent
source modification defers until a decision is recorded; approvals append to
`AgentState.approvals` and persist across sessions; denied → the finding is skipped.
There is **no timeout-based auto-grant**: interactive runs await a human, while the
headless improvement loop uses an explicit recorded auto-approval policy (approver
`auto-approval-policy`).

## Alternatives

- **In-memory checkpointer** — rejected: no kill/resume demo (an acceptance
  criterion), no audit trail after a crash.
- **Auto-approve reversible-looking refactors** — rejected: the project classifies
  every source modification as irreversible-tier (PRD_agent_orchestration §5). The
  headless loop's auto-approval is an explicit recorded grant (approver
  `auto-approval-policy`), not a silent reversible-tier auto-approve.

## Consequences

\+ Kill/resume is demonstrable; the approval audit trail satisfies the guardrail
requirement.
− Single-writer SQLite is fine locally but would need replacing for multi-user
deployment (out of scope).
