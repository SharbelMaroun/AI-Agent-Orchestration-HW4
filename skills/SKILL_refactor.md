---
name: refactor
description: Apply graph-evidenced refactors (split god module, break bottleneck, merge duplicates, fix SPOF). Human-only — never auto-invocable.
allowed-tools: [Read, Edit, Bash]
triggers: [split god module, break bottleneck, merge duplicates, fix spof, rewire imports]
disable-model-invocation: true
---

# When to use

Use this skill only on explicit human request to change code, with each trigger tied to a
BugHunterAgent bug class:

- "split god module" → **GodModule** (a hub with excessive fan-in/fan-out)
- "break bottleneck" → **Bottleneck** (a cut vertex on the critical path)
- "merge duplicates" (similarity >= 0.91) → **DuplicateLogic**
- "fix SPOF" → **SinglePointOfFailure** (validates / writes_session / checks_policy chain)
- "rewire imports" → **BrokenSeam** (imports left dangling after a split)

# Procedure

This skill is human-only (`disable-model-invocation`); the supervisor never auto-invokes it. Each
mutating step declares its guardrail tag.

- [reversible] Create the fix branch and apply the edit. undo: `git checkout main && git branch -D fix/iter-<n>`
- [reversible] Split the god module into seams and rewire imports. undo: `git revert --no-edit HEAD`
- [reversible] Stage the duplicate-merge candidate for review. undo: `git restore --staged --worktree .`
- [irreversible] Finalize a duplicate merge (deletes the redundant module). APPROVAL REQUIRED before execution.
- [irreversible] Delete a dead file after SPOF removal. APPROVAL REQUIRED before execution.

After every reversible step, QAAgent re-runs tests + ruff; a red gate triggers the documented undo.
Irreversible steps halt for explicit human approval and are never executed automatically.
