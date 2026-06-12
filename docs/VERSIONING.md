# Documentation Versioning Convention

> Version: 1.00 | Status: Draft — awaiting lecturer approval | Course: AI Agent Orchestration — HW4 (EX04)

## Rules

1. **Start version.** Every deliverable document starts at **1.00** (two decimals,
   Guidelines V3: all versions start at 1.00). The same applies to code
   (`shared/version.py`) and JSON configs (`"version"` key).
2. **Bump triggers.**
   - **+0.01 (patch)** — editorial fixes, clarified wording, internal consistency
     corrections that do not change any requirement, threshold, or decision.
   - **+0.10 (minor)** — incorporation of lecturer feedback, or a changed/added
     requirement, ADR, diagram, or threshold.
   - **+1.00 (major)** — a scope change that invalidates a previously approved gate
     (requires re-approval of the affected document).
3. **Pre-approval drafts** stay at 1.00; edits are recorded in the change log only.
   The first bump happens with the first lecturer feedback round.
4. **Status field** transitions: `Draft — awaiting lecturer approval` → `Approved`
   (only with a record in `docs/approvals/`); any post-approval edit reverts the
   status to Draft and bumps per rule 2.

## Change-log table format

Every deliverable doc ends with (or links to) a change log in this exact format:

| Version | Date | Author | Change summary | Trigger |
|---|---|---|---|---|
| 1.00 | 2026-06-12 | <author> | Initial draft | — |
