# ADR-004 — Gatekeeper FIFO queue, never reject

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

Guidelines V3 mandates one gatekeeper for ALL external API calls with rate limits and
an overflow queue that queues — never rejects, never crashes.

## Decision

`gatekeeper/gatekeeper.py` is the sole egress. Limits come from
`config/rate_limits.json` (`rate_limits.services.default`):
**requests_per_minute 30, requests_per_hour 500, concurrent_max 5,
retry_after_seconds 30, max_retries 3**. Over-limit calls enter a FIFO queue bounded
by the **`queue.max_depth`** config key (with `queue.backpressure_warn_ratio` for the
warn threshold); when full, the queue blocks producers (backpressure) rather than
dropping; retries are gatekeeper-internal; every call — including failures — is
written to the token ledger.

## Alternatives

- **Reject-on-overflow (HTTP 429 style)** — rejected: Guidelines V3 explicitly says
  queue, never reject or crash.
- **Per-agent clients** — rejected: bypasses central accounting; the ≥ 70% savings
  proof needs one authoritative ledger.

## Consequences

\+ No lost work; honest token accounting (failed calls still cost — Part A).
− Latency under burst is accepted for a batch pipeline. Queue depth is config, never
hardcoded.
