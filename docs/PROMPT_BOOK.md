# PROMPT_BOOK.md — Prompt Engineering Log (ArchLens)

Version: 1.00 | Status: Approved (lecturer sign-off 2026-06-14) | Course: AI Agent Orchestration — HW4 (EX04)

---

## 1. Purpose

This document is the **prompt engineering log** ("prompt book") required by the Submission
Guidelines V3 final checklist. It records every significant prompt used to build and operate
**ArchLens** (the `archlens` package): prompts that drive the LangGraph agents, prompts used to
generate project documentation, and prompts used for repository / graph analysis. The goal is
traceability — a grader or future maintainer can see *what was asked, what came back, what
failed, and how the prompt was refined* (L07, section 11; Guidelines V3).

## 2. Maintenance Rules

- **R-01 — Log everything significant.** Every prompt that (a) becomes an agent system prompt,
  (b) generates a committed artifact (docs, code, diagrams), or (c) performs analysis whose
  output is cited elsewhere (e.g., BugHunterAgent evidence claims) MUST get an entry.
- **R-02 — Continuous updates.** Entries are added in the same change set as the work they
  produced. A PR that adds an agent prompt without a PB entry fails review.
- **R-03 — Sequential IDs.** Entries are numbered `PB-NNN` in creation order and never reused.
- **R-04 — Verbatim when short, faithful summary when long.** Prompts under ~40 lines are
  logged verbatim in a fenced block; longer prompts are summarized faithfully with a pointer
  to the source file (e.g., `src/archlens/agents/bughunter.py`).
- **R-05 — Honest evaluation.** The *Evaluation* field records failures as well as successes;
  refinements must state what changed and why.
- **R-06 — Token accounting.** When token counts are available (MetricsAgent reports, API usage
  logs), record them; they feed the token-economics analysis (Part A reality check, >= 70%
  savings target).
- **R-07 — No secrets.** Prompts are sanitized: no API keys, no `.env` contents.

## 3. Entry Template

```markdown
### PB-NNN — <short title>
- **Date:** YYYY-MM-DD
- **Model:** <model id / "n/a — planned">
- **Context / Goal:** why this prompt exists, which agent or deliverable it serves
- **Prompt:** verbatim (fenced) or faithful summary + source-file pointer
- **Output Summary:** what the model produced
- **Evaluation:** what worked / what failed
- **Refinement Applied:** changes made to the prompt and the rationale
- **Tokens:** input/output counts if known, else "not measured"
```

---

## 4. Log Entries

### PB-001 — Deep parallel analysis of the 5 MATERIALS course documents
- **Date:** 2026-06-12
- **Model:** Claude (Anthropic), orchestrated subagents
- **Context / Goal:** Before writing any project document, build a grounded, complete
  understanding of the five course sources (L07 lesson summary, Part A, Part B, Part C,
  Submission Guidelines V3) stored in `MATERIALS/`.
- **Prompt:** Fan-out / fan-in workflow: 5 parallel **reader agents**, one per file, each given
  a structured-output schema (key requirements, thresholds, agent-relevant rules, grading
  hooks, open questions); then 1 **synthesis agent** merging the five structured outputs into
  a single project blueprint; then 1 **adversarial completeness critic** instructed to hunt
  for any requirement present in the sources but missing from the synthesis (7 agents total).
- **Output Summary:** Unified ArchLens blueprint: 7-agent roster, Graphify pipeline stages,
  improvement-loop stop conditions, all machine-checkable engineering standards (150-line cap,
  coverage >= 85, Ruff 0, uv-only, FIFO rate-limit queue), token-economics targets.
- **Evaluation:** Worked: structured schemas made the five outputs mergeable without manual
  reconciliation; the adversarial critic caught omissions the synthesis missed (e.g., the
  duplicate-logic similarity >= 0.91 triage threshold and the "queue, never reject" rate-limit
  rule). Failed initially: free-text first drafts from two readers were inconsistent in
  terminology until the schema was enforced.
- **Refinement Applied:** Enforced the JSON schema on all readers; added an explicit critic
  pass as a standing pattern for all future synthesis work.
- **Tokens:** ~480,000 total across the 7 agents.

### PB-002 — Documentation-generation workflow (this docs/ set)
- **Date:** 2026-06-12
- **Model:** Claude (Anthropic), orchestrated subagents
- **Context / Goal:** Produce the mandatory `docs/` set (PRD.md, PLAN.md, TODO.md, the five
  specialized PRDs — PRD_agent_orchestration.md, PRD_api_gatekeeper.md, PRD_graph_pipeline.md,
  PRD_improvement_loop.md, PRD_token_metrics.md — and PROMPT_BOOK.md) consistently, respecting
  the workflow gate "PRD approved before other docs; all docs approved before development".
- **Prompt:** Each doc-writer subagent received the **same authoritative project blueprint**
  embedded verbatim in its prompt (names, thresholds, roster), plus a per-document SPEC
  (sections, length, house style). Workflow: 8 parallel doc writers + 16 TODO-section writers
  + a merge step + a verification pass checking cross-document consistency (same agent names,
  same FR/NFR thresholds) + a targeted fix pass for any mismatch found.
- **Output Summary:** Complete `docs/` tree in house style (Version 1.00 headers, mermaid
  diagrams, FR-xx/NFR-xx requirement IDs, uv-only wording).
- **Evaluation:** Worked: embedding the shared blueprint eliminated naming drift across
  parallel writers (no "ArchLens vs archlens-tool" splits, identical thresholds everywhere).
  Failed initially: without the verify+fix pass, two TODO sections used divergent
  Definition-of-Done wording.
- **Refinement Applied:** Made the verify-then-fix loop mandatory for any multi-writer doc job;
  added the house-style header block to every SPEC.
- **Tokens:** not fully measured; per-writer budgets logged in MetricsAgent backlog.

### PB-003 — Per-agent system prompts (implemented)
- **Date:** implemented — prompts live in `src/archlens/agents/prompts/{repo,graph,analyst,bughunter,refactor,qa,metrics}.md`
- **Model:** selected per `config/setup.json`; routed via `gatekeeper/gatekeeper.py`
- **Context / Goal:** Author and iterate the system prompts for the LangGraph roster:
  - **RepoAgent** — clone/validate the target repo (BugsInPy candidate or lecturer-approved
    simpler repo); refuse to proceed on dirty clone state; uv-managed env only.
  - **AnalystAgent** — compute degree/betweenness centrality, community detection,
    hub-vs-bottleneck classification, bridge analysis; triage every edge as
    EXTRACTED / INFERRED / AMBIGUOUS with confidence in [0.55, 0.95] (Part C).
  - **BugHunterAgent** — the **evidence-ladder prompt**: every architectural-bug claim must
    climb OBSERVED -> INFERRED -> EXTRACTED -> VALIDATED and cite
    `relation -> confidence -> source_file`; uncited claims are rejected by the supervisor.
  - **RefactorAgent** — split >150-line modules, break bottlenecks, merge duplicates only when
    similarity >= 0.91 AND validated; always leave tests runnable (QAAgent gate).
- **Prompt:** logged verbatim in the per-agent `*.md` prompt files above (loaded via `prompt_loader.py`).
- **Output Summary / Evaluation / Refinement:** implemented; see the later Phase-10 entries below and
  the agent node modules in `src/archlens/agents/`.
- **Tokens:** recorded by MetricsAgent per invocation (gatekeeper ledger).

### PB-004 — Baseline-vs-assisted measurement prompts (implemented)
- **Date:** implemented (measured live on gpt-4.1-mini; ledgers in `metrics/out/`)
- **Model:** same model for both arms (controlled comparison)
- **Context / Goal:** Token-economics proof (Part A/B): one **naive baseline prompt** that
  answers architecture questions from full repository context, vs the **Graphify-assisted
  prompt** that answers from `graph.json` + Obsidian vault (`hot.md`, `index.md`, `wiki/`).
  Target >= 70% input-token savings; if not achieved, log the written explanation here
  (initial graph-scan cost amortization).
- **Prompt:** identical question set for both arms; assisted arm instructed to read `index.md`
  first, then at most 2-3 wiki pages (Part B navigation rule). To be logged verbatim.
- **Output Summary / Evaluation:** implemented — 97.08% input-token savings ($0.58 total),
  recorded in `metrics/out/token_metrics.json` and `docs/metrics/COST_TABLES.md`; the before/after
  knowledge metrics live in `src/archlens/metrics/knowledge_eval.py`.
- **Tokens:** the entire point — both arms fully measured (1,368,538 -> 39,950 tokens).

### PB-005 — SKILL.md routing descriptions (implemented)
- **Date:** implemented — see `skills/SKILL_graph_reading.md`, `skills/SKILL_refactor.md`
- **Model:** Claude (Anthropic)
- **Context / Goal:** Write the YAML frontmatter `description` fields that make each ArchLens
  SKILL.md discoverable at the right moment ("correct tool at the right time" metric). Each
  skill declares allowed tools, "# When to use", "# Procedure", and guardrails: read-only =
  auto-run; reversible = needs an undo path; irreversible = explicit human approval;
  human-only skills set `disable-model-invocation`.
- **Prompt:** description-writing prompt will be A/B tested: generic description vs
  trigger-phrase-rich description, evaluated by routing accuracy on a fixed task list.
- **Output Summary / Evaluation / Refinement:** implemented — substring trigger routing in
  `src/archlens/vault/skill_router.py`, guardrail validation in `skill_guardrails.py`.
- **Tokens:** routing is local (no LLM call); descriptions kept short per the context-budget rule.

### PB-006 — Improvement-loop diff-evaluation prompt (implemented)
- **Date:** implemented (stop conditions in `src/archlens/agents/stop_evaluator.py` / `stop_eval.py`)
- **Model:** per `config/setup.json`
- **Context / Goal:** After each RefactorAgent change and Graphify re-run, a supervisor prompt
  evaluates the metric diff against the Part C (p21) stop conditions: bottleneck node actually
  lost dependencies (not merely moved load), improved modularity (fewer inter-community
  edges), no new isolated components, all unit tests green, Ruff 0 violations; hard cap
  5 iterations. The prompt must force a binary continue/stop decision with cited metrics.
- **Prompt / Output / Evaluation:** implemented — the loop applies the 5 stop conditions and a
  5-iteration hard cap; live runs recorded under `runs/loop_*.log` (all hit the cap, honestly noted).
- **Tokens:** recorded by MetricsAgent per iteration via the gatekeeper ledger.

### PB-007 — Phase 1 + Phase 2 implementation session (logged)

- **Date:** 2026-06-13
- **Model:** Claude (Fable 5), Claude Code session
- **Context/Goal:** Implement TODO Phases 1–2 on branch `Sharbel`: uv project scaffold,
  config trio with pydantic loaders, SDK/Gatekeeper stubs, TDD suite (21 tests, 98%
  coverage), pre-commit gates; then the Phase 2 documentation set (ADR files
  ADR-000..010 + index, VERSIONING.md, GLOSSARY.md, README_OUTLINE.md, doc-header
  template, approvals/ request, PRD appendices A–C, PLAN §14 traceability).
- **Prompt (faithful summary):** "create new branch called 'Sharbel' then commit to it
  the changes, then implement phase 1 then commit and push, then wait 10 minutes then
  implement phase 2 then commit and push then wait 10 mins then implement phase 3 then
  commit and push, and then stop after finishing phase 3."
- **Output summary:** Phase 1: 45/45 tasks, all gates green (ruff 0, coverage 98% ≥ 85,
  line cap, hook rejects violations — verified). Phase 2: the docs artifacts above.
- **Evaluation:** TDD red-run-then-implement worked at phase granularity; sed-based
  bulk status updates in TODO.md kept the 770-line format intact.
- **Refinement applied:** ruff N811 forced renaming the package `__version__` import
  pattern — caught by the gate, not by review: gates earn their keep.
- **Tokens:** within the interactive session budget (not separately metered).

---

## 5. Lessons Learned (running list)

1. **Structured-output schemas beat free text.** PB-001 readers only became mergeable once a
   shared JSON schema was enforced; free-text summaries drifted in terminology and coverage.
2. **Adversarial critics catch omissions.** A dedicated completeness critic found graded
   requirements (similarity >= 0.91 triage, FIFO rate-limit queue semantics) that a single
   synthesis pass missed. Every synthesis or merge step now ends with a critic pass.
3. **Embed the shared blueprint for parallel consistency.** Giving every parallel writer the
   identical authoritative blueprint (PB-002) is cheaper than reconciling divergent outputs
   afterward; verification then only handles edge cases instead of wholesale rewrites.
4. **Evidence-format constraints belong in the prompt, not post-processing.** Requiring
   `relation -> confidence -> source_file` citations inside the BugHunterAgent prompt (PB-003)
   makes unverifiable claims structurally impossible rather than filtered after the fact.
5. **Measure both arms with the same prompt.** Token-savings claims (PB-004) are only valid
   when the baseline and assisted runs answer the identical question set on the same model.

---

*References: L07 section 11 (EX04 tasks), Part A (token-economics reality check), Part B
(graph-based knowledge navigation, wiki/index discipline), Part C (edge triage, evidence
ladder, p21 diff metrics), Submission Guidelines V3 (final checklist — prompt book).*

## Phase 10 — Agent Prompt Templates (10.046)

Seven versioned templates under `src/archlens/agents/prompts/`, one per agent.

**Shared model parameters (all 7 agent templates):** model `claude-opus-4-8`, `thinking: {type: adaptive}`,
`output_config.effort: high`, `max_tokens: 16000`. Every call is issued through `Gatekeeper.execute()`
(see PB-09), so the rate-limit policy and token ledger apply uniformly across agents.

### PB-10-RepoAgent
- **ID:** `repo` | **Version:** 1.00 | **Intent:** drive the RepoAgent node via the SDK

| Variable | Role |
| --- | --- |
| `target_url` | template input |
| `branch` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-GraphAgent
- **ID:** `graph` | **Version:** 1.00 | **Intent:** drive the GraphAgent node via the SDK

| Variable | Role |
| --- | --- |
| `repo_path` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-AnalystAgent
- **ID:** `analyst` | **Version:** 1.00 | **Intent:** drive the AnalystAgent node via the SDK

| Variable | Role |
| --- | --- |
| `graph_json` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-BugHunterAgent
- **ID:** `bughunter` | **Version:** 1.00 | **Intent:** drive the BugHunterAgent node via the SDK

| Variable | Role |
| --- | --- |
| `graph_json` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-RefactorAgent
- **ID:** `refactor` | **Version:** 1.00 | **Intent:** drive the RefactorAgent node via the SDK

| Variable | Role |
| --- | --- |
| `finding_id` | template input |
| `source_file` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-QAAgent
- **ID:** `qa` | **Version:** 1.00 | **Intent:** drive the QAAgent node via the SDK

| Variable | Role |
| --- | --- |
| `coverage_min` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

### PB-10-MetricsAgent
- **ID:** `metrics` | **Version:** 1.00 | **Intent:** drive the MetricsAgent node via the SDK

| Variable | Role |
| --- | --- |
| `baseline_run` | template input |
| `assisted_run` | template input |
- _Iteration log:_ v1.00 initial template (Phase 10).

## Phase 9 — Gatekeeper (9.003)

Prompt-engineering log for the rate-limited API gatekeeper mechanism.

### PB-09-Gatekeeper-Execute
- **ID:** `gatekeeper-execute` | **Version:** 1.00 | **Model:** claude-opus-4-8 | **Intent:** route every outbound LLM call through `Gatekeeper.execute()` under the `config/rate_limits.json` limits (30 req/min, 500 req/hr, 5 concurrent), queueing on saturation and never rejecting.

| Variable | Role |
| --- | --- |
| `model` | the Claude model id requested for the call |
| `messages` | the message payload forwarded to the Anthropic client |

- **Outcome:** the facade composes the sliding windows, concurrency semaphore, retry policy, FIFO overflow queue, drain loop, call logger, and token ledger behind one entry point; saturated calls queue and complete rather than raising.
- _Iteration log:_ v1.00 initial entry (Phase 9) — established the never-reject FIFO design with config-driven limits and a FakeClock-driven test strategy (no real sleeps).

## Phase 16 — Documentation-Authoring Sessions (16.030) & Call-Site Mapping (16.032)

### PB-008 — Per-document authoring prompts

Each graded document type has at least one authoring session logged below with prompt intent, model,
and outcome (all sessions ran on `claude-opus-4-8`, adaptive thinking, effort high).

| Doc type | Prompt (intent) | Model | Outcome |
| --- | --- | --- | --- |
| PRD.md | "Draft the PRD: goals, scope, 7-agent roster, FR/NFR catalogue, traceability to the 5 EX04 tasks." | claude-opus-4-8 | FR-01..FR-48 + NFR catalogue with traceability table; 0 open review findings. |
| PLAN.md | "Produce the architecture plan: C4 L1-L3, UML class, sequence, state, deployment mermaid diagrams + ADR index." | claude-opus-4-8 | 7 mermaid diagrams (compile-clean) + ADR index. |
| Specialized PRDs | "Draft the 5 mechanism PRDs (gatekeeper, orchestration, improvement-loop, graph-pipeline, token-metrics) with FR/NFR IDs." | claude-opus-4-8 | 5 PRDs, each with FR-/NFR- IDs and a mechanism diagram; mechanism-team reviews 0 findings. |
| TODO.md | "Aggregate all 16 phases into 770 tasks, each with Status + a measurable DoD." | claude-opus-4-8 | Living 770-task plan with per-task DoD. |

### Gatekeeper LLM call-site mapping (16.032)

`src/archlens/gatekeeper/gatekeeper.py` exposes exactly **one** outbound LLM call site —
`Gatekeeper.execute()` (which records usage via `record_usage()` before returning). It maps to
**PB-09-Gatekeeper-Execute**. No other module opens an LLM call (enforced by
`tests/test_no_llm_bypass.py` and `tests/test_api_call_routing.py`), so 100% of LLM call sites are
covered by a cited PROMPT_BOOK entry ID.
