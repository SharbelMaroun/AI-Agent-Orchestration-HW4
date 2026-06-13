# ADR-006 — Token-measurement baseline methodology

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

The course requires proving ≥ 70% token savings (cited range 70–95%; community
reports up to 5.1x) or explaining why not (Part A amortization reality check).

## Decision

Two measured runs over the SAME fixed 10-question analysis set:

- **Baseline run** — naive full-context: questions answered by stuffing raw target
  files into the prompt (capped at model context, chunked if needed); token counts
  taken from API usage fields via the gatekeeper ledger.
- **Assisted run** — Graphify-assisted navigation: `index.md` hub first, then 2–3
  `wiki/` pages / `hot.md` subgraph context only.

MetricsAgent emits per-model cost tables in this format:

| Model | Run | Input tokens | Output tokens | $ in | $ out | $ total |
|---|---|---|---|---|---|---|

plus the savings ratio. The one-off graph-scan cost is reported separately and
amortized (break-even queries) per Part A. If savings < 70%, a written explanation
section is mandatory in the metrics report.

## Alternatives

- **Compare against ad-hoc manual sessions** — rejected: not reproducible, no
  apples-to-apples question set.
- **Token estimates from text length** — rejected: API usage fields are authoritative.

## Consequences

\+ Apples-to-apples comparison; audit-ready ledger.
− The baseline run itself costs tokens; bounded by running it once on a fixed
question set.
