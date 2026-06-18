# ArchLens — Master Product Requirements Document (PRD)

Version: 1.00 | Status: Approved (lecturer sign-off 2026-06-14) | Course: AI Agent Orchestration — HW4 (EX04)

---

## 1. Document Control

| Field | Value |
| --- | --- |
| Product name | ArchLens |
| Package name | `archlens` |
| Document version | 1.00 (versions start at 1.00 per Guidelines V3) |
| Status | Approved (lecturer sign-off 2026-06-14) |
| Author | \<STUDENT NAME — placeholder\> |
| Course | AI Agent Orchestration — Dr. Yoram Segal |
| Assignment | HW4 / EX04 — "Reverse Engineering of Graph Knowledge Systems with Graphify and Obsidian" (Lecture 07, section 11) |
| Source course material | L07 Lesson Summary; Part A (Active Knowledge Architecture); Part B (Graph-Based Knowledge Architectures & Context Management); Part C (Reading and Inferring from a Graphify Graph); Software Submission Guidelines V3 |
| Tooling baseline | Python 3.10+, LangGraph, Graphify, Obsidian, uv (exclusively) |

**Approval gate (mandatory workflow):** This PRD MUST be approved by the lecturer BEFORE `PLAN.md`, `TODO.md`, and the specialized per-mechanism PRDs (`PRD_<mechanism>.md`) are finalized, and BEFORE ANY development work begins. All documents must be approved before development starts. No code is written while this document carries the status "Draft".

---

## 2. Background & Problem Statement

### 2.1 The context-window bottleneck

Every LLM workflow is constrained by the context window: the amount of information we *want* to inject (an entire unfamiliar codebase, its docs, its tests) vastly exceeds what fits. Worse, naive workflows pre-fill the window with descriptions of every available asset before the first real question is asked, so the window is cluttered with irrelevant material (L07 §2, §7). The "lost-in-the-middle" phenomenon compounds this: the model weights the beginning and end of the context heavily while information in the middle is weakened, forgotten, or corrupted (L07 §9). Compaction (summarize, keep head and tail, drop the middle) is a partial workaround — costly in time and lossy by design.

### 2.2 Why RAG is not enough

RAG organizes knowledge by vector distance, which captures *semantic similarity* but not *associative connection*. "Movie", "Popcorn", and "Parking" tell a human one story — going to the cinema — yet in vector space "Movie" is only near "TV series" (L07 §2.1). Code has exactly this property: a controller, a validator, and a database reader are associated by a call path, not by textual similarity. Naive RAG therefore injects noise — chunk after chunk — while the relationship that matters (who calls whom) is invisible to it.

### 2.3 The graph-based answer

Graphify builds a knowledge graph from a repository almost token-free: AST analysis records that function A calls function B without any LLM involvement (L07 §4.1). Only deeper semantic inference costs tokens, and those edges are explicitly marked with confidence levels. Obsidian then serves as the "Wikipedia of the project" — a navigable vault of linked Markdown pages (L07 §4.2, Part A pp. 3–5). With a graph, retrieval becomes *targeted*: read the query, locate the relevant node, pull only the connected subgraph (L07 §7.1). The course cites 70–95% token savings; community reports cite up to 5.1x.

### 2.4 The problem ArchLens solves

A graduate engineer must be able to take a large, unfamiliar Python repository and (a) understand its architecture, (b) find and fix architectural defects (Single Points of Failure, god nodes, bottlenecks, duplicated logic), and (c) do so with a fraction of the tokens a naive full-context approach would burn. ArchLens is a multi-agent system (LangGraph supervisor pattern, 7 specialist agents) that automates this end-to-end: clone → graph → analyze → diagnose → refactor → re-graph → verify, with measurable token economics.

---

## 3. Goals & Non-Goals

### 3.1 Goals

| ID | Goal |
| --- | --- |
| G-1 | Fully automate the EX04 pipeline: clone target repo, run Graphify (detect → extract → build → cluster → export), generate an Obsidian vault, analyze, fix, verify. |
| G-2 | Produce reverse-engineering deliverables: block diagram, OOP class schema, PRD-vs-code alignment audit (unimplemented requirements, orphan modules). |
| G-3 | Detect architectural bugs with an auditable evidence ladder (OBSERVED → INFERRED → EXTRACTED → VALIDATED); every claim cites relation → confidence → source_file. |
| G-4 | Run an improvement loop (max 5 iterations) with hard stop conditions and unit tests after EVERY change. |
| G-5 | Prove ≥ 70% token savings vs. a naive full-context baseline, or deliver a documented written explanation (Part A reality check: initial graph-scan cost amortization). |
| G-6 | Meet every machine-checkable engineering standard of Guidelines V3 (coverage ≥ 85%, Ruff 0 violations, 150-line cap, uv-only, SDK/gatekeeper architecture). |
| G-7 | Ship the Part B knowledge assets: at least one SKILL.md, an LLM Wiki (raw/ → wiki/, index.md hub, log.md journal), and before/after measurement on 4 metrics. |

### 3.2 Non-Goals

- Real-time / continuous re-graphing on every keystroke or commit. The architect inspects the finished product; Graphify is re-run only at defined loop checkpoints (L07 §10.2 "The architect does not work in real-time").
- Production deployment, hosting, packaging for PyPI, or multi-user operation. ArchLens runs locally for one operator.
- Reverse engineering of non-Python targets (JS, Java, media files, etc.).
- Building a general-purpose IDE plugin or replacing Obsidian's UI.
- Guaranteeing semantic correctness of the *target* repository beyond its own test suite.

---

## 4. Personas

| Persona | Description | Needs |
| --- | --- | --- |
| **P-1 Student operator** | The course student running ArchLens end-to-end on a target repo via `uv run`. Edits `config/setup.json`, supplies `.env` from `.env-example`, reads the generated vault in Obsidian. | One-command pipeline, clear logs, deterministic outputs, recoverable failures (FIFO queue — never crash on rate limits). |
| **P-2 Lecturer / grader** | Dr. Segal or a TA grading the submission. **May use AI agents to test the submission**, so every requirement here must be machine-checkable: file paths, thresholds, exit codes, report formats. | Reproducible runs, requirement IDs traceable to artifacts, docs that match the code, token-savings evidence tables. |
| **P-3 ArchLens agents** | The 7 LangGraph agents themselves (RepoAgent, GraphAgent, AnalystAgent, BugHunterAgent, RefactorAgent, QAAgent, MetricsAgent) are consumers of the vault and graph.json. The vault's `index.md` and `hot.md` are written *for them* first. | Compact, well-linked, front-matter-tagged Markdown; stable JSON schemas; confidence-annotated edges. |

---

## 5. User Stories

Each story includes acceptance criteria (AC). Stories are testable by P-2's AI graders.

| ID | Story | Acceptance criteria |
| --- | --- | --- |
| US-01 | As a student operator, I configure the target repo URL in `config/setup.json` and run one command so that the whole pipeline executes without manual steps. | AC: `uv run python src/main.py` (or `uv run archlens`) completes clone → graph → vault → analysis with exit code 0; no value is hardcoded in code. |
| US-02 | As a student operator, I want RepoAgent to clone and validate a BugsInPy candidate, so I can target real-world bugs. | AC: repo cloned to configured path; Python project detected; if environment setup fails, the documented fallback-repo path in `setup.json` is used and the switch is logged. |
| US-03 | As a student operator, I want GraphAgent to run the Graphify pipeline so I get graph.json, graph.html and REPORT.md. | AC: all three artifacts exist after stage `export`; pipeline stages detect → extract → build → cluster → export each log start/end. |
| US-04 | As a student operator, I want an Obsidian vault generated so I can navigate the target like Wikipedia. | AC: vault contains `hot.md`, `index.md`, `wiki/` pages, `log.md`; every wiki page has YAML frontmatter and at least one wikilink; vault opens in Obsidian without errors. |
| US-05 | As a grader, I want every detected architectural bug to cite its evidence so I can audit claims. | AC: each finding lists evidence-ladder level (OBSERVED/INFERRED/EXTRACTED/VALIDATED), the relation, a confidence value, and a source_file path. |
| US-06 | As a grader, I want edge triage so I can distinguish facts from guesses. | AC: every analyzed edge is classified EXTRACTED, INFERRED, or AMBIGUOUS; INFERRED/AMBIGUOUS edges carry confidence in [0.55, 0.95]; AMBIGUOUS edges are flagged for human review. |
| US-07 | As a student operator, I want RefactorAgent to fix one architectural bug per iteration so changes stay reviewable. | AC: each iteration produces exactly one applied fix, a re-run of Graphify, a metrics diff, and a green test run before the next iteration starts. |
| US-08 | As a student operator, I want the loop to stop on objective conditions so it cannot run away. | AC: loop halts when stop conditions are met (see FR-30) or after 5 iterations, whichever comes first; the halt reason is written to the metrics report. |
| US-09 | As a grader, I want token before/after accounting so I can verify the ≥ 70% savings claim. | AC: MetricsAgent emits a cost table per model with input/output tokens and $ cost for baseline vs. Graphify-assisted runs; if savings < 70%, a written explanation section is present. |
| US-10 | As a grader, I want the reverse-engineering deliverables so I can assess understanding, not just automation. | AC: block diagram (mermaid) and OOP class schema (mermaid classDiagram) of the *target* repo exist; PRD-vs-code audit lists unimplemented requirements and orphan modules. |
| US-11 | As a student operator, I want all external API calls to go through one gatekeeper with rate limiting so the run never crashes on 429s. | AC: limits 30 req/min, 500 req/hr, 5 concurrent enforced from `config/rate_limits.json`; overflow requests enter a FIFO queue (config-driven max depth) — queued, never rejected, never crashing; retry_after 30 s, max_retries 3. |
| US-12 | As an ArchLens agent (P-3), I want `index.md` to be the single entry hub so I read it first and then only 2–3 relevant pages. | AC: index.md links every wiki page; a logged navigation trace shows hub-first access; per-query page reads ≤ 3 in the assisted run. |
| US-13 | As a grader, I want knowledge assets per Part B so the project demonstrates active knowledge architecture. | AC: ≥ 1 SKILL.md with YAML frontmatter (name, description, allowed tools), "# When to use", "# Procedure", and guardrail classification; LLM Wiki with raw/ → wiki/ flow and log.md ingestion journal; before/after table on the 4 Part B metrics. |

---

## 6. Functional Requirements

### 6.1 Target-repo management

- **FR-01** — The system SHALL read the target repository URL, branch/commit, local clone path, and fallback repository from `config/setup.json`. No repo identifiers may appear in source code.
- **FR-02** — RepoAgent SHALL clone the configured GitHub repository (BugsInPy candidate with a uv-managed environment, or a simpler lecturer-approved repo) and validate it: directory exists, is a git repo, contains Python sources.
- **FR-03** — If environment preparation of the primary target fails (drivers, native libs, broken installs), RepoAgent SHALL switch to the configured fallback repository, log the decision in `log.md`, and continue — per L07 §11.2 "do not get stuck".
- **FR-04** — RepoAgent SHALL record the resolved commit hash so every downstream artifact (graph, vault, metrics) is traceable to an exact target state.
- **FR-40** — Every clone SHALL land in a sandboxed per-run directory under the configured `workdir_root`; path containment is enforced (no resolved path may escape the sandbox root) and cleanup is idempotent.
- **FR-41** — Clone retries SHALL follow `config/rate_limits.json` (max_retries, retry_after_seconds): transient failures (network, timeout) are retried, permanent failures (auth, disk full) are raised immediately as typed exceptions.
- **FR-42** — Every cloned target SHALL pass four validation checks before use — is-Python (share threshold + project config), size bounds (file count + MB), has-tests, recognized license — aggregated in a `ValidationResult` with a per-check reason string.
- **FR-43** — Git network operations SHALL exist only inside `gatekeeper/`; a guard test scans the rest of `src/archlens` for subprocess/git usage and fails on any match.

### 6.2 Graphify pipeline

- **FR-05** — GraphAgent SHALL execute the Graphify pipeline in order: `detect → extract → build → cluster → export`, surfacing per-stage status and failures.
- **FR-06** — The pipeline SHALL produce `graph.json` (nodes, edges, types, confidences), `graph.html` (visual graph), and `REPORT.md` (run report).
- **FR-07** — GraphAgent SHALL re-run the full pipeline on demand (used by the improvement loop after every applied fix) and version each output set per iteration (e.g., `iter_0/`, `iter_1/`, …).
- **FR-08** — Graphify invocation parameters (scan root, depth, exclusions) SHALL come from `config/setup.json`; the scan root choice is explicit because it directly impacts token consumption (L07 §5).

### 6.3 Obsidian vault generation

- **FR-09** — GraphAgent SHALL build an Obsidian vault containing, at minimum: `hot.md` (hottest nodes / entry points for fast triage), `index.md` (the hub page linking all content — read first), `wiki/` (one page per significant node/module with YAML frontmatter and wikilinks), and `log.md` (ingestion and decision journal).
- **FR-10** — Every `wiki/` page SHALL carry frontmatter with at least `type`, `status`, and `project` fields (Part A "Anatomy of a Note") to enable unified search.
- **FR-11** — `index.md` SHALL be authored as the agents' entry point: hub first, then 2–3 targeted pages per query (Part B navigation discipline). Orphan pages (no inbound link from index.md) are a defect.
- **FR-12** — `log.md` SHALL append an entry for every ingestion, vault regeneration, fallback decision, and improvement-loop iteration (timestamp, actor agent, summary).

### 6.4 Graph analysis engine

- **FR-13** — AnalystAgent SHALL compute degree centrality and betweenness centrality for all nodes in `graph.json`.
- **FR-14** — AnalystAgent SHALL perform community detection and report the community partition, including inter-community edge counts (the modularity signal used by the improvement loop).
- **FR-15** — AnalystAgent SHALL classify high-centrality nodes as **hub** vs. **bottleneck**: a hub has many connections; a bottleneck is a hub through which flow *must* pass (high betweenness, low redundancy). A weak hub is not dangerous; a critical bottleneck is an architectural problem (L07 §10).
- **FR-16** — AnalystAgent SHALL perform bridge analysis in both senses: (a) graph-theoretic bridge edges whose removal disconnects components, and (b) redundancy bridges — parallel paths that provide fallback but risk duplication/consistency issues (L07 §10.1).
- **FR-17** — AnalystAgent SHALL flag Single Point of Failure (SPOF) nodes: nodes on which a critical path depends with no alternative route (e.g., a lone auth/validation chokepoint).
- **FR-18** — AnalystAgent SHALL triage every edge as EXTRACTED (AST-certain), INFERRED (LLM-derived, confidence required), or AMBIGUOUS (contradictory/unclear, requires human review). EXTRACTED edges carry a fixed confidence of 0.95 (representation of certainty); the 0.55–0.95 confidence range is enforced for every edge.
- **FR-19** — BugHunterAgent SHALL detect, at minimum: SPOFs, god nodes (one module doing unrelated work across communities), hub-vs-bottleneck risks, fragile bridges, and duplicate logic — duplicates with similarity ≥ 0.91 enter merge triage. Every finding SHALL climb the evidence ladder OBSERVED → INFERRED → EXTRACTED → VALIDATED and cite relation → confidence → source_file.

### 6.5 Reverse-engineering deliverables

- **FR-20** — The system SHALL emit a block diagram of the target's architecture (mermaid, derived from communities and inter-community edges) — not a copy of any pre-existing documentation (L07 §11.1: "the value is in the extraction of understanding").
- **FR-21** — The system SHALL emit an OOP class schema (mermaid classDiagram) of the target's main classes, methods, and relationships, derived from EXTRACTED edges.
- **FR-22** — The system SHALL produce a PRD-vs-code alignment audit of the target: requirements present in target docs but unimplemented in code (under-implementation), and orphan modules implemented without any corresponding requirement (over-implementation) — Part A "Plan vs. Code" synthesis.

### 6.6 Multi-agent orchestration

- **FR-23** — ArchLens SHALL be implemented as a LangGraph `StateGraph` using a supervisor pattern coordinating exactly these specialist agents: RepoAgent, GraphAgent, AnalystAgent, BugHunterAgent, RefactorAgent, QAAgent, MetricsAgent (L07 §11 "multiplicity of agents").
- **FR-24** — Shared state SHALL flow through a typed state object; agents SHALL NOT communicate via side channels (files excepted where they are declared artifacts).
- **FR-25** — All business logic SHALL be reachable only via the single SDK entry point `src/archlens/sdk/sdk.py`; agents call the SDK, never each other's internals.
- **FR-26** — ALL external API calls (LLM, GitHub, any network) SHALL pass through `src/archlens/gatekeeper/gatekeeper.py`, which enforces `config/rate_limits.json`.
- **FR-27** — The supervisor SHALL persist a run manifest (agents invoked, transitions, per-agent outcomes) sufficient for a grader to replay the decision sequence.

### 6.7 Improvement loop & stop conditions

- **FR-28** — RefactorAgent SHALL apply exactly one fix per iteration from the prioritized finding list, ordered by the canonical fix taxonomy: P1 SPOF on critical path > P2 bottleneck split (god node only when classified bottleneck, not healthy hub) > P3 split of >150-line modules > P4 merge of validated duplicates (similarity ≥ 0.91, after manual check) > P5 PRD-vs-code misalignment.
- **FR-29** — After EVERY change, QAAgent SHALL run the unit test suite; on a red test suite or ruff violations, RefactorAgent MAY attempt repair up to 3 times; if still red, the change is reverted and the failure recorded — no fix is ever kept on red.
- **FR-30** — After each fix, GraphAgent re-runs Graphify and AnalystAgent computes diff metrics (Part C p21). A fix is ACCEPTED only if ALL of the following per-fix acceptance criteria hold: (a) the targeted bottleneck node actually lost dependencies — not merely moved its load elsewhere (degree AND betweenness deltas); (b) modularity improved — fewer inter-community edges — or unchanged, for fixes that do not target coupling (P3/P5); (c) no new isolated components appeared; (d) all unit tests green; (e) Ruff reports 0 violations. The RUN terminates on convergence (stop-condition evaluation shows no further real improvement available), or when the fix queue is empty, or at the hard cap of 5 iterations (FR-31) — whichever comes first.
- **FR-31** — The loop SHALL hard-stop after 5 iterations regardless of remaining findings, recording unresolved items.
- **FR-32** — Every iteration SHALL append to `log.md` and to the metrics report: fix applied, metric deltas, stop-condition evaluation, decision.

### 6.8 Token measurement

- **FR-33** — MetricsAgent SHALL run (or replay) a **baseline** naive full-context analysis of the target and record its token consumption per model (input tokens, output tokens, $ cost).
- **FR-34** — MetricsAgent SHALL record the Graphify-assisted run's token consumption with the same accounting, and compute % savings. Target: ≥ 70% (course range 70–95%; community reports up to 5.1x).
- **FR-35** — If savings < 70%, MetricsAgent SHALL emit a written explanation section analyzing why — explicitly addressing initial graph-scan cost and its amortization horizon (Part A reality check: "initial scanning requires tokens and time before savings are realized").

### 6.9 Knowledge assets (Part B)

- **FR-36** — The project SHALL ship at least one `SKILL.md` with YAML frontmatter (`name`, `description`, allowed tools), a "# When to use" section, and a "# Procedure" section.
- **FR-37** — Each skill SHALL declare its guardrail class: read-only → auto-invocable; reversible → requires a documented undo path; irreversible → requires explicit human approval. Human-only skills SHALL set `disable-model-invocation`.
- **FR-38** — The project SHALL maintain an LLM Wiki: `raw/` sources transformed into `wiki/` pages, with `index.md` as the hub read first (then 2–3 pages per query) and `log.md` as the ingestion journal.
- **FR-39** — The project SHALL measure before/after (without wiki vs. with wiki) on the 4 Part B metrics: source traceability, noise reduction, correct-file identification, correct-tool-at-the-right-time, and publish the comparison table.
- **FR-44** — Every `SKILL.md` SHALL pass a schema validator (`sdk.validate_skill`) that rejects frontmatter missing or with empty `name`, `description`, or allowed-tools fields, before the skill is usable.
- **FR-45** — A guardrail classifier SHALL map each skill's declared tools and step markers to exactly one of `auto` (read-only), `reversible` (documented undo path required), `irreversible` (explicit human approval required), or `human_only` (`disable-model-invocation`, never auto-invocable).
- **FR-46** — A skill router SHALL match prompts to skills by trigger phrase/problem pattern, return no match for ambiguous prompts, and never auto-return a `disable-model-invocation` skill.
- **FR-47** — The raw→wiki pipeline SHALL stamp every ingested `raw/` file with a provenance header (source path + timestamp), produce `wiki/` pages that backlink their `raw/` source, build an `index.md` hub linking 2–3 wiki pages per topic, and append one `log.md` journal entry per pipeline stage; every wiki page SHALL be reachable from `index.md` within 2 hops with zero orphans.
- **FR-48** — The 4-metric knowledge rubric SHALL score each metric on an integer 0–10 scale with a mandatory rationale, drive a before/after measurement harness over a fixed 10-task evaluation set, and feed an iterate cycle (score → correct weakest metric → re-measure) that stops when all metrics meet target or after 3 cycles.

---

## 7. Non-Functional Requirements

- **NFR-01 — Test coverage:** ≥ 85% (`fail_under = 85`), measured as statement + branch + path coverage; exclusions limited to `src/main.py`, `tests/`, and GUI code. TDD (red-green-refactor) is the working method.
- **NFR-02 — Lint:** Ruff with 0 violations. Configuration: line-length 100, target py310, select `E,F,W,I,N,UP,B,C4,SIM`, ignore `E501`.
- **NFR-03 — File size:** maximum 150 lines of code per file (blank and comment lines excluded), including test files. Files are split, never compressed, to comply.
- **NFR-04 — Toolchain:** uv ONLY. `pip`, `virtualenv`, `venv`, and `python -m` invocations are FORBIDDEN everywhere — code, docs, CI. `pyproject.toml` is the single source of truth (no `requirements.txt`); `uv.lock` is committed; everything runs via `uv run`.
- **NFR-05 — SDK single entry:** all business logic lives under `src/archlens/` and is exposed only via `sdk/sdk.py`. `src/main.py` is a thin CLI with zero business logic.
- **NFR-06 — Gatekeeper-only API access:** no module other than `gatekeeper/gatekeeper.py` opens network connections or calls external APIs. Rate limits (30 req/min, 500 req/hr, 5 concurrent, retry_after 30 s, max_retries 3) and FIFO overflow queue depth come from `config/rate_limits.json`; overflow is queued, never rejected, never a crash.
- **NFR-07 — Secrets policy:** secrets only in `.env` (git-ignored); `.env-example` with dummy values is committed (mandatory). No key, token, or password ever appears in code, config, logs, or docs.
- **NFR-08 — No hardcoded values:** all tunables via `cfg.get(...)` / `os.environ.get(...)`. Permitted exceptions: `shared/constants.py`, Enums, mathematical/physical constants.
- **NFR-09 — Local-only execution:** the full pipeline runs on the student's machine; the only outbound traffic is gatekeeper-mediated (LLM API, git clone). No server component, no telemetry.
- **NFR-10 — Concurrency model (I/O-bound by design) + thread safety:** ArchLens's parallelism need is **I/O-bound** — the dominant cost is external API / git / subprocess egress through the gatekeeper, so the correct tool is **threading** (a `BoundedSemaphore` caps concurrent in-flight calls; sliding-window counters, the FIFO overflow queue, the token ledger, and the metrics counter are each lock-guarded). The CPU-bound graph computations (centrality, community detection, duplicate scan) run **single-threaded by deliberate choice**: the analyzed graphs are small (httpie ≈ 2k–4k nodes, sub-second NetworkX passes), so a `ProcessPoolExecutor` would add pickling/spawn overhead and Windows fragility for no measurable gain. Multiprocessing is the documented extension point should a target graph ever grow large enough to need it. Shared LangGraph state mutations are confined to node boundaries.
- **NFR-11 — DRY thresholds:** same function in 2+ files → extract to shared module; same try/except pattern in 3+ files → wrapper; same method in 3+ classes → base class or mixin.
- **NFR-12 — Versioning:** component versions live in `shared/version.py` and start at 1.00.
- **NFR-13 — Repository layout:** exactly per Guidelines V3 — `src/archlens/{sdk/, gatekeeper/, agents/, graphops/, vault/, metrics/, shared/}`, `src/main.py`, `config/{setup.json, rate_limits.json, logging_config.json}`, `tests/` with `conftest.py`, `docs/`.

---

## 8. Success Metrics

| Metric | Target | Evidence artifact |
| --- | --- | --- |
| Token savings (assisted vs. naive baseline) | ≥ 70% (course cites 70–95%; community 5.1x); else a documented written explanation (FR-35) | MetricsAgent cost tables (per model: input/output tokens, $ cost) |
| Part B metric 1 — source traceability | Improved after wiki adoption (every answer cites its source page/file) | Before/after measurement table (FR-39) |
| Part B metric 2 — noise reduction | Fewer irrelevant files/pages loaded per query | Before/after measurement table |
| Part B metric 3 — correct-file identification | Higher hit rate locating the file responsible for a behavior | Before/after measurement table |
| Part B metric 4 — correct-tool-at-the-right-time | Skill/tool invoked matches the need (Part A "Skill-to-Need" routing) | Before/after measurement table |
| Improvement-loop deltas (Part C p21) | Bottleneck dependency count strictly decreased; inter-community edges decreased; isolated components not increased | Per-iteration graph diff report |
| Quality gates | Tests green after every change; coverage ≥ 85%; Ruff 0 | CI / `uv run` outputs |
| Loop discipline | ≤ 5 iterations; halt reason recorded | Metrics report + log.md |

---

## 9. Scope

### 9.1 In scope

- One target Python repository per run (BugsInPy candidate or approved fallback), configured in `config/setup.json`.
- Full Graphify pipeline, Obsidian vault generation, 7-agent LangGraph orchestration, improvement loop, token economics, all documentation and knowledge assets listed herein.
- Re-running Graphify at loop checkpoints (after each applied fix).

### 9.2 Out of scope

- **Real-time re-graphing** (file-watcher / per-keystroke graph updates) — the architect inspects completed states, not live edits.
- **Production deployment** — no hosting, containers-for-prod, auth, or multi-tenancy.
- **Non-Python targets** — JS/TS, Java, media-heavy repos are excluded.
- Modifying Graphify or Obsidian themselves; building custom graph visualization.
- Fixing *functional* (non-architectural) bugs in the target beyond what its own test suite enforces during refactors.

---

## 10. Dependencies & Assumptions

| ID | Dependency / Assumption | Notes |
| --- | --- | --- |
| D-1 | Graphify CLI is installed and runnable locally, supporting the detect/extract/build/cluster/export pipeline and emitting graph.json / graph.html / REPORT.md. | Verified during setup; pinned version recorded in log.md. |
| D-2 | Obsidian (desktop) is available to open the generated vault. | Vault must also be fully usable as plain Markdown without Obsidian. |
| D-3 | Claude API access (Anthropic) via key in `.env`; all calls through the gatekeeper. | Assumption: rate limits in `rate_limits.json` are below account limits. |
| D-4 | uv is installed; Python 3.10+ available via uv-managed environments. | No pip/venv anywhere. |
| D-5 | LangGraph is the orchestration framework (not CrewAI). | Per blueprint decision. |
| D-6 | Target repo is reachable on GitHub and clonable anonymously or with configured credentials. | Fallback repo configured for resilience (FR-03). |
| A-1 | The lecturer approves this PRD before any downstream doc/code work. | Workflow gate, §1. |
| A-2 | A pair working in a focused manner can complete the assignment in ~5 hours of work (L07 §12); ArchLens automation keeps the human share within that budget. | Time-box assumption. |

---

## 11. Risks & Mitigations

| ID | Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| R-1 | **Token-cost amortization fails:** initial Graphify scan + vault build costs exceed savings on a small target, missing the 70% target. | Medium | High | Measure honestly; FR-35 mandates a written explanation with amortization analysis (Part A reality check); choose a target large enough for savings to dominate. |
| R-2 | **Graphify output instability:** schema drift or non-deterministic graph.json between runs breaks diff metrics. | Medium | High | Pin Graphify version; validate graph.json against an internal schema on load; compare graphs structurally (node/edge sets), not byte-wise. |
| R-3 | **BugsInPy environment complexity:** legacy dependencies fail to install under uv. | High | Medium | FR-03 fallback-repo plan, pre-approved by lecturer; switch early, log the decision; "repository choice does not affect the grade" (L07 §11.2). |
| R-4 | **LLM hallucination** in inferred edges or bug claims. | High | High | Evidence ladder (OBSERVED → INFERRED → EXTRACTED → VALIDATED); confidence bounds 0.55–0.95; AMBIGUOUS edges require human review; no fix applied on unvalidated claims. |
| R-5 | **Refactor regressions** in the target repo. | Medium | High | Unit tests after EVERY change (FR-29); red suite → automatic revert; one fix per iteration keeps diffs small. |
| R-6 | **Rate-limit storms / API outages** mid-run. | Medium | Medium | Gatekeeper FIFO queue (never reject, never crash), retry_after 30 s, max_retries 3; resumable pipeline stages. |
| R-7 | **Lost-in-the-middle degradation** when agents are fed long vault excerpts. | Medium | Medium | Hub-first navigation (index.md, then 2–3 pages); short focused contexts; compaction only as last resort. |
| R-8 | **150-line cap vs. complexity:** agents or graph ops outgrow file limits, tempting compression. | High | Low | Split modules along responsibilities (never compress); DRY thresholds (NFR-11) push shared code into `shared/`. |
| R-9 | **Improvement loop "improves" metrics without improving architecture** (load merely moved, not removed). | Medium | High | Stop condition (a): bottleneck must *lose* dependencies, not relocate them; modularity and isolation checks run together (FR-30). |
| R-10 | **Doc/code drift:** PRD claims diverge from implementation by submission time. | Medium | Medium | Requirement IDs (FR/NFR) referenced from tests and TODO.md DoD entries; PRD-vs-code audit run on ArchLens itself before submission. |

---

## 12. Acceptance Criteria & Definition of Done

ArchLens HW4 is DONE when ALL of the following hold (each item machine-checkable by an AI grader):

1. **Pipeline:** `uv run` of the CLI completes clone → Graphify (all 5 stages) → vault → analysis → improvement loop → metrics on the configured target with exit code 0.
2. **Artifacts exist:** `graph.json`, `graph.html`, `REPORT.md`; vault with `hot.md`, `index.md`, `wiki/`, `log.md`; block diagram; OOP class schema; PRD-vs-code audit of the target.
3. **Findings audited:** every architectural-bug claim carries evidence-ladder level, relation, confidence (0.55–0.95 where applicable), and source_file.
4. **Loop discipline:** ≤ 5 iterations; per-iteration diff metrics recorded; every kept fix has a green test run; stop reason logged.
5. **Quality gates:** coverage ≥ 85% (fail_under enforced), Ruff 0 violations, no file over 150 effective lines, no hardcoded values outside permitted locations.
6. **Architecture gates:** single SDK entry point; gatekeeper-only external calls; thin CLI; layout per NFR-13; `.env` ignored + `.env-example` present; `uv.lock` committed; no pip/venv/requirements.txt anywhere.
7. **Token economics:** baseline vs. assisted cost tables per model published; ≥ 70% savings OR written amortization explanation.
8. **Knowledge assets:** ≥ 1 compliant SKILL.md with guardrails; LLM Wiki with hub-first structure and log.md journal; 4-metric before/after table.
9. **Docs complete and gated:** PRD.md (this, approved), PLAN.md (C4 + UML + deployment + ADRs), TODO.md (statuses + DoD), the 5 specialized PRDs — exactly `PRD_agent_orchestration.md`, `PRD_api_gatekeeper.md`, `PRD_graph_pipeline.md`, `PRD_improvement_loop.md`, `PRD_token_metrics.md` — and PROMPT_BOOK.md — all approved before development started, per the workflow gate.

---

## 13. Glossary

| Term | Definition |
| --- | --- |
| **Graphify** | CLI tool that scans a repository (AST for code, optional LLM for semantics) and emits a knowledge graph (`graph.json`, `graph.html`, `REPORT.md`) via the pipeline detect → extract → build → cluster → export. Its structural analysis is nearly token-free. |
| **Vault** | An Obsidian workspace — the root folder of linked Markdown files defining "who is playing". ArchLens generates one per target with `hot.md`, `index.md`, `wiki/`, `log.md`. |
| **EXTRACTED** | Edge type: hard fact obtained by AST analysis (function calls function). Full certainty; no LLM involved. EXTRACTED edges are represented with a fixed confidence of 0.95; the 0.55–0.95 range is enforced for every edge. |
| **INFERRED** | Edge type: relationship derived by an LLM from comments/text/semantics. Partial certainty; always carries a confidence score (in ArchLens: 0.55–0.95). |
| **AMBIGUOUS** | Edge type: contradictory or unclear relationship ("something does not look right"). Flagged for mandatory human review before any action. |
| **Hub** | A high-centrality node — many edges in and out. A weak hub is harmless. |
| **Bottleneck** | A hub through which flow *must* pass (high betweenness, no alternative path). A critical bottleneck is an architectural problem; ArchLens distinguishes hub vs. bottleneck explicitly. |
| **Bridge (graph-theoretic)** | An edge whose removal disconnects parts of the graph — a fragility indicator. |
| **Bridge (redundancy)** | A parallel path letting information reach a destination two ways — robustness and fallback, at the price of duplication and consistency risk (L07 §10.1: both senses are analyzed). |
| **SPOF (Single Point of Failure)** | A node on which a critical path depends with no alternative route (e.g., a lone validation step in an auth flow). Failure or overload there halts the system. |
| **God node** | A module/class doing many unrelated things whose edges "escape" into multiple communities — evidence of poor separation of concerns. |
| **Community** | A group of nodes with many internal edges and few external ones; reveals logical architecture (e.g., frontend vs. backend). |
| **Compaction** | Context-management operation: summarize a long context, keep the beginning and end, discard the middle (where the model performs worst). Time-consuming but effective. |
| **Lost-in-the-middle** | LLM phenomenon: information at the start and end of the context is weighted strongly; information in the middle is weakened, forgotten, or corrupted. Motivates short, targeted contexts. |
| **Evidence ladder** | BugHunterAgent claim-strength scale: OBSERVED → INFERRED → EXTRACTED → VALIDATED; only VALIDATED findings are eligible for automated fixes. |
| **Edge triage** | AnalystAgent classification of every edge as EXTRACTED / INFERRED / AMBIGUOUS with confidence, separating facts from guesses before any decision. |
| **Gatekeeper** | The single module (`gatekeeper/gatekeeper.py`) through which ALL external API calls pass, enforcing rate limits and the FIFO overflow queue. |
| **SDK** | The single business-logic entry point (`sdk/sdk.py`); the CLI and agents consume it; nothing bypasses it. |

---

## Appendix A — EX04 Core-Task Traceability

Mapping of all 5 L07 §11 EX04 core tasks to functional requirements (zero unmapped tasks):

| # | EX04 core task (L07 §11) | Covering FRs |
|---|---|---|
| 1 | Code cloning (GitHub repo, lecturer-approved; BugsInPy or simpler fallback) | FR-01, FR-02, FR-03, FR-04, FR-40, FR-41, FR-42, FR-43 |
| 2 | Run Graphify — graph, index, navigation pages (`hot.md`), display in Obsidian | FR-05, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12 |
| 3 | Reverse engineering — block diagram + OOP class schema | FR-20, FR-21, FR-22 |
| 4 | AI agents (LangGraph) for analysis, identification, and fixing of architectural bugs | FR-13–FR-19, FR-23–FR-27 |
| 5 | Improvement loop — apply fix, re-run Graphify, stop conditions, unit tests after every change | FR-28, FR-29, FR-30, FR-31, FR-32 |
| + | Token-savings proof required by L07 §9/§12 ("prove savings or explain") | FR-33, FR-34, FR-35 |
| + | Part B final-project knowledge assets (SKILL.md, LLM Wiki, 4 metrics) | FR-36, FR-37, FR-38, FR-39 |

## Appendix B — Target-Repository Shortlist (approved 2026-06-14)

Selection criteria: pure Python (AST-friendly), real test suite (the improvement loop
needs a green baseline), uv-compatible installation, small enough for the 5-hour
budget, present in BugsInPy where possible (L07 §11.2). Repo choice does not affect
the grade — L07 §11.2.

| # | Repository | BugsInPy? | uv compatibility (measured — see docs/REPO_SELECTION.md) | Test suite |
|---|---|---|---|---|
| 1 (primary) | https://github.com/httpie/cli | Yes | uv-OK via `uv run --with-editable` (1028 tests collected) | pytest, 44 test files |
| 2 | https://github.com/tqdm/tqdm | Yes | `uv sync` FAIL (dep conflict); `--with-editable` OK | pytest, 20 test files |
| 3 | https://github.com/nvbn/thefuck | Yes | setup.py-only; `uv sync` FAIL | pytest, 204 test files |
| F (fallback) | https://github.com/psf/requests | No | modern packaging, uv-friendly | pytest, extensive |

Fallback policy: FR-03 — if primary environment preparation fails, switch to F and
log the decision (L07 §11.2 "do not get stuck"; a virtual environment is mandatory
for BugsInPy work and is provided by the uv-managed environment, satisfying both the
L07 requirement and the Guidelines V3 venv prohibition).

## Appendix C — Change Log & Self-Review

### Change log (per docs/VERSIONING.md)

| Version | Date | Author | Change summary | Trigger |
|---|---|---|---|---|
| 1.00 | 2026-06-12 | S. Maroun + Claude | Initial draft (13 sections, FR-01..39, NFR-01..13) | — |
| 1.00 | 2026-06-13 | S. Maroun + Claude | Consistency fixes (FR-28/29/30 canonical policies); Appendices A–C added | Internal review (pre-approval, no bump) |

### Self-review checklist (TODO 2.011) — 0 open findings

- [x] Every requirement carries a unique FR-xx / NFR-xx ID (FR-01..39, NFR-01..13; no duplicates)
- [x] Every requirement is testable (thresholds/conditions stated numerically where applicable)
- [x] All 5 EX04 core tasks trace to FRs (Appendix A, zero unmapped)
- [x] No tooling other than uv is referenced for use anywhere in this document
- [x] Stop conditions, hard cap, coverage 85, ruff 0, 150-line cap, uv-only each appear as a dedicated requirement (FR-30/31, NFR-01..04)
- [x] Mandatory header present; status remains Draft pending lecturer approval

---

*End of document. This PRD awaits lecturer approval before any downstream document is finalized or any development begins.*
