# ADR-001 — LangGraph over CrewAI

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

EX04 (L07 §11) mandates agents "based on LangGraph or CrewAI". ArchLens needs
deterministic supervisor routing, durable checkpoints for kill/resume, and a
human-approval interrupt before irreversible refactors.

## Decision

LangGraph `StateGraph` with a supervisor pattern; routing is a pure function over the
typed `AgentState`; persistence via the SQLite checkpointer (ADR-009).

## Alternatives

- **CrewAI** — rejected: its role/task abstraction is convenient but routing is less
  deterministic, and first-class `interrupt_before` approval gates plus checkpoint
  resume are exactly the LangGraph primitives the improvement loop needs.
- **Hand-rolled orchestrator** — rejected: re-implements checkpointing and interrupts
  with no course credit for the plumbing.

## Consequences

\+ Checkpointer gives crash-resume and `interrupt_before` approval gates for free;
routing is unit-testable without an LLM.
− More boilerplate than CrewAI's role abstraction; mitigated by a shared `BaseAgent`.
