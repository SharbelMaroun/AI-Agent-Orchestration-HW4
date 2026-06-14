# ArchLens

Multi-agent, graph-based reverse engineering of Python codebases — HW4/EX04 for the
AI Agent Orchestration course. ArchLens clones a target repository, builds a knowledge
graph with Graphify, navigates it in an Obsidian vault, detects architectural defects
with LangGraph agents, fixes them in a measured improvement loop, and proves token savings.

Full documentation lives in `docs/` (PRD, PLAN, specialized PRDs, TODO, prompt book).

## Quickstart (uv only)

```bash
uv tool install graphifyy==0.8.39   # prerequisite: the external Graphify code-graph CLI (pinned)
uv sync                          # install the locked environment
uv run pytest                    # run the test suite (coverage gate: 85%)
uv run ruff check .              # lint gate: zero violations
uv run python src/main.py --version
```

All tooling goes through uv; this project never uses other package managers. Graphify
(`graphifyy` on PyPI, command `graphify`, by Safi Shamsi) is an external CLI tool — like
`git`, it is invoked through the gatekeeper and is **not** vendored into the repo. Its
clones and outputs land under the git-ignored `runs/`.

### Optional developer setup: the `/graphify` skill in Claude Code

ArchLens drives Graphify through the gatekeeper, so this is **not required** to run the
project. It only adds a `/graphify` slash command to your own Claude Code for ad-hoc
graph queries:

```bash
graphify install --platform claude   # installs the skill into ~/.claude/skills/graphify/
# then restart Claude Code (skills load at startup) and type:  /graphify .
graphify uninstall                   # to remove it later
```

This writes to your per-machine `~/.claude/` (a `SKILL.md`, its `references/`, and a
`graphify` section in `~/.claude/CLAUDE.md`) — it changes your local IDE, not this repo.

## Report

What was actually done on branch `Sharbel` (commits `ef5e993` → `7ad35d0`,
2026-06-12..14), including the real failures hit along the way. Everything below is
reproducible from the repo.

### Timeline of work

| Commit | Scope | Outcome |
|---|---|---|
| `ef5e993` | Course materials + full `docs/` suite | 9 documents incl. a 770-task TODO (statuses + DoD per task) |
| `dc8348d` | **Phase 1 — Project setup & tooling** (45/45 tasks) | uv project `archlens` v1.00, package skeleton, config trio + pydantic loaders, SDK/Gatekeeper stubs, 21 TDD tests, pre-commit gates |
| `a0b0b9f` | **Phase 2 — Documentation & approval gates** (40/45; 5 await the lecturer) | ADR-000..010 standalone files + index, GLOSSARY (44 terms), VERSIONING, README outline, PRD appendices, PLAN traceability matrix, all 7 diagrams compiled |
| `1158695` | **Phase 3 — Target repository module** (44/45; approval task blocked) | Sandbox manager, gatekeeper-only git ops with typed errors + config-driven retry, 4 validation checks, RepoAgent node with fallback, measured repo-selection evidence |
| `41881db` | **Phase 4 — Graphify pipeline integration** (49/50; 4.002 awaits lecturer) | graph.json models + validating parser, stage orchestrator, run layout/manifest, GraphDiff engine, SDK facade — built first against a *mocked* CLI (see correction below) |
| `6b1b8d1` | **Phase 5 — Obsidian vault & navigation** (48/50; 5.002 + 5.046 blocked) | layout, frontmatter, wikilinks, hot.md/index.md/wiki pages, append-only log, raw ingest, orphan/broken-link validation, deterministic builder, `archlens vault` CLI + GraphAgent |
| `77658a0` | **Graphify correction — real CLI + adapter, run for real** | rebuilt the wrapper to real `graphify update`/`extract`, added a node-link adapter, ran on httpie (2033 nodes / 4306 edges / 138 communities), built + validated a real vault |
| `f359c08` | Pin prerequisite `graphifyy==0.8.39` | reproducible external-tool version |
| `743a383` | **Phase 6 — Graph analysis engine** (55/55) | centrality, community detection (COMMUNITY≠FOLDER), bridges, critical paths/SPOF, edge triage + confidence policy, review queue, duplicates, macro/meso/micro views + query/path/explain/diff |
| `8b9ad6b` | **Phase 7 — Reverse-engineering deliverables** (44/45) | architecture block diagram, OOP class schema (AST→classDiagram), PRD↔code alignment audit, traceability + evidence-ladder linter, deliverable generators + CLI |
| `d93a776` | **Phase 8 — SDK layer & core architecture** (49/50) | constants/exceptions, frozen DTOs + serde, gatekeeper protocol, SDK orchestration facade (analyze/run_loop/measure_tokens), plugin registry, thin CLI subcommands, DRY + thread-safety audits |
| `41efe45` | **Phase 10 — Multi-agent orchestration (LangGraph)** (55/55) | AgentState + per-key reducers, supervisor + conditional routing, 7 agent nodes, compiled StateGraph, SqliteSaver checkpointing + resume, guardrail tiers + human-approval interrupt, per-node retries, run trace, 7 prompt templates |
| `4f6be68` | **Phase 11 — Improvement loop & stop conditions** (49/50) | fix priority policy + evidence gate + queue, iteration brancher + revert rollback, refactor fixes (split/bottleneck/duplicate/SPOF), test gate→rollback, graph-diff metrics + load-shift SC-1, StopConditionEvaluator (5 SCs + 5-iter cap), LoopController subgraph + `--loop` CLI + E2E convergence |
| `7ad35d0` | **Phase 9 — API gatekeeper & rate limiting** (49/50) | sliding-window limiters (30/min, 500/hr), concurrency semaphore, retry policy, FIFO overflow queue + blocking backpressure, drain loop, structured call log + key redaction, token-ledger hooks, Anthropic client + offline mock mode, `execute()` facade (saturation / never-reject / thread-safety) |

Task ledger after Phases 1–11 (the skipped Phase 9 now also complete): **528 DONE · 6 IN_PROGRESS · 14 BLOCKED · 222 TODO** of 770. (BLOCKED = lecturer-approval gates plus 5.046, which needs the Obsidian GUI. The remaining TODO are Phases 12–16.)

### Quality-gate evidence (final state)

```text
$ uv run pytest --cov=archlens --cov-branch
649 passed in 6.12s
Required test coverage of 85.0% reached. Total coverage: 97.11%

$ uv run ruff check .
All checks passed!

$ uv run python scripts/check_line_cap.py
line cap OK: all files within 150 effective lines

$ uv run python src/main.py --version
1.00
```

### Architecture diagrams (compiled from PLAN.md)

All seven mermaid diagrams are machine-verified (mermaid-cli exit 0) and rendered to SVG:

| | |
|---|---|
| ![C4 L1 — System context](docs/diagrams/plan_01.svg) | ![C4 L2 — Containers](docs/diagrams/plan_02.svg) |
| ![C4 L3 — Agent layer](docs/diagrams/plan_03.svg) | ![UML class diagram](docs/diagrams/plan_04.svg) |
| ![Improvement-loop sequence](docs/diagrams/plan_05.svg) | ![Supervisor state machine](docs/diagrams/plan_06.svg) |

![Deployment diagram](docs/diagrams/plan_07.svg)

### Analysis of a real graph (httpie — 2033 nodes / 4306 edges / 138 communities)

Generated from the real `runs/eval/httpie/graphify-out/graph.json` by
`uv run python scripts/visualize_graph.py` (structural `graphify update` pass, no LLM):

| | |
|---|---|
| ![Top 15 hubs by degree](docs/diagrams/analysis_hubs.png) | ![Top 20 communities by size](docs/diagrams/analysis_communities.png) |
| ![Node file-type mix](docs/diagrams/analysis_filetypes.png) | ![Top-hub neighbourhood subgraph](docs/diagrams/analysis_subgraph.png) |

The hub chart surfaces httpie's real architecture: `http()` dominates at degree ~343 — a
genuine god-node / single-point-of-failure candidate — followed by `Environment`,
`MockEnvironment`, and `ExitStatus`. This is exactly the signal the AnalystAgent and
BugHunterAgent consume to drive the improvement loop. (An interactive `graph.html` exists
alongside the JSON; rendering it to a static screenshot needs a browser/GUI — see "Not yet
captured" below — so these matplotlib charts are the headless-reproducible substitute.)

### Errors actually encountered (and what they taught)

**1. Session usage limits killed an entire 27-agent docs-generation run.** Every agent
failed identically; the workflow was resumed after the reset and completed (33 agents,
770 tasks merged). The six post-verification fix agents then hit the *next* window and
were re-applied manually afterwards.

```text
[write:PRD] failed: You've hit your session limit · resets 6:40pm (Asia/Jerusalem)
[todo:01-Project] failed: You've hit your session limit · resets 6:40pm (Asia/Jerusalem)
... (27/27 agents, run 1) ...
[fix:PRD.md] failed: You've hit your session limit · resets 12:20am (Asia/Jerusalem)
```

**2. The lint gate caught a real naming violation (Phase 1).** First `ruff check` run:

```text
N811 Constant `VERSION` imported as non-constant `__version__`
 --> src\archlens\__init__.py:3:37
Found 1 error.
```

Fixed by importing `get_version()` and assigning `__version__` — the gate, not review,
caught it.

**3. The pre-commit hook provably rejects bad commits (task 1.042).** A deliberate
`import os` (unused, F401) was staged and committed; the hook blocked it — verified by
`git log` showing no such commit exists.

**4. mermaid-cli found two real diagram bugs the eye missed (task 2.021).**

```text
Error: Parse error on line 5: Expecting 'SEMI', 'NEWLINE', ... got 'GRAPH'
Error: Parse error on line 19: Expecting '()', 'SOLID_OPEN_ARROW', ... got 'NEWLINE'
```

Causes: a flowchart node named `graph` (reserved keyword) and `&lt;`/`&gt;` HTML
entities in a sequence-diagram message — the entity's `;` terminates a mermaid
statement mid-line. Both fixed in PLAN.md; all 7 diagrams now compile.

**5. The planned primary target repo failed its environment check (Phase 3).**
PRD Appendix B originally proposed tqdm. Measured:

```text
$ uv sync   # inside the tqdm clone
hint: The `requires-python` value (>=3.7) includes Python versions that are
not supported by your dependencies (e.g., pytest-asyncio>=0.25.0,<=1.2.0
only supports >=3.9).
```

httpie/thefuck are `setup.py`-only, so plain `uv sync` fails there too. The working
uv-only strategy is an ephemeral env — and it flipped the recommendation to httpie:

```text
$ uv run --with-editable <httpie clone> --with pytest python -c "import httpie"
Installed 21 packages in 743ms
httpie import OK 3.2.4

$ uv run --with-editable ".[dev]" --with pytest pytest tests -q --collect-only
1028 tests collected in 1.13s

$ uv run --with-editable ".[dev]" --with pytest pytest tests/test_compress.py -q
16 passed, 1 warning in 2.88s
```

**6. A measurement pitfall: uv workspace discovery produced fake evidence.** The first
`uv sync` runs inside `runs/eval/<repo>` silently resolved *ArchLens's own* project
(the clones sat inside our workspace and two had no `[project]` table). Detected
because no `.venv` appeared inside the clones; all evaluations were re-run isolated in
the system temp directory. Full honest log trail: `docs/REPO_SELECTION.md` §3.

### What is verifiable right now

- `uv run pytest` — 649 tests across the repo module, the Graphify pipeline (models,
  validating parser, node-link adapter, diff engine, orchestrator), the graph-analysis
  engine, the Obsidian vault generator (hot.md golden file, broken-link/orphan validation,
  deterministic rebuild), the LangGraph multi-agent orchestration (supervisor + 7 agents +
  SqliteSaver checkpointing + human-approval interrupts), the improvement loop (fix
  selection, graph-diff stop conditions, end-to-end convergence in ≤5 iterations), and the
  rate-limited gatekeeper (sliding windows, FIFO never-reject queue, 50×20-thread safety) —
  plus guard tests proving no module outside `gatekeeper/` touches subprocess/git or imports
  an API client.
- A **real Graphify run** on the httpie clone (`graphify update`, no LLM): 2033 nodes,
  4306 edges, 138 communities → ArchLens built a 138-page Obsidian vault that passes
  validation (0 broken links, 0 orphans). See the correction note below.
- `uv run python -c "..."` config-switch demo — primary `httpie/cli`, fallback
  `psf/requests`, no code change needed (see `docs/REPO_SELECTION.md` §5).
- Lecturer-approval gates (PRD, all-docs, target repo) are deliberately BLOCKED —
  the Guidelines V3 workflow forbids development past those gates without sign-off;
  requests are prepared in `docs/approvals/`.

### Not yet captured

Real `graph.json` / `graph.html` / `GRAPH_REPORT.md` now exist (httpie, under the
git-ignored `runs/`), a real Obsidian vault was generated and validated, and the real graph
is now charted in the **Analysis** section above (hubs, communities, file-type mix, subgraph).
Still open: interactive `graph.html` / Obsidian-vault **screenshots** (this environment has no
headless browser, so vis.js can't be rendered here — the matplotlib charts are the substitute);
the **semantic** `graphify extract` pass (needs an LLM API key); and the **token-economics**
before/after tables (Phase 12).

### Correction (2026-06-13): Graphify integration rebuilt against the real CLI, then run for real

We got something wrong in Phase 4 and fixed it. Recorded honestly, with before/after.

**What we did wrong.** The Phase 4 Graphify wrapper was built against an *assumed*
five-stage interface, `graphify --stage <s> --repo <p> --depth <d>`, and was only ever
exercised against hand-authored `graph.json` fixtures with a **mocked** subprocess. So:

- Graphify was **never actually run**; the httpie repo was **never analyzed**; no real
  `graph.json` existed.
- The real tool — **`graphifyy`** on PyPI (command `graphify`, by Safi Shamsi, *not*
  Dr. Yoram Segal, who only teaches with it) — has **no** `--stage`/`--repo`/`--depth`
  flags. Its real `graph.json` is networkx node-link JSON: edges under `links` with
  `source`/`target`, an **open** AST relation vocabulary (`calls`, `contains`,
  `imports_from`, `inherits`, `re_exports`, ...), the evidence tier in `confidence` plus
  a numeric `confidence_score`, and community membership as a per-node `community` id.
  Our PRD-spec models (`from`/`to`, closed relation enum, float `confidence`) did not
  match it.

**What we did to fix it.**

1. Installed the real tool the uv-compliant way, pinned: `uv tool install graphifyy==0.8.39`.
2. Rewrote `graphops/cli_wrapper.py` + `gatekeeper/graphify_ops.py` to call the real
   commands — `graphify update <repo>` for the structural, no-LLM pass (the "almost
   free" AST analysis) and `graphify extract` for the semantic pass — through the
   gatekeeper, exactly like `git`.
3. Added `graphops/adapter.py` (`load_graphify_graph`) that normalizes real node-link
   output (and our canonical fixtures) into the `Graph` aggregate, and relaxed the
   models to reality (`relation` is now an open string; nodes carry `label` /
   `source_location`; the adapter pins EXTRACTED confidence and maps `file_type`).
4. **Ran it for real** on the httpie clone and rebuilt the vault end-to-end.

**Real-run evidence (no LLM / no API key — structural `graphify update`):**

```text
$ graphify update runs/eval/httpie
  AST extraction: 188/188 files (100%) [8 workers]
[graphify watch] Rebuilt: 2033 nodes, 4306 edges, 138 communities
  graph.json, graph.html and GRAPH_REPORT.md updated

# ArchLens then consumed that real graph.json:
REAL httpie graph: 2033 nodes, 4306 edges, 138 communities
vault root: runs/httpie-vault   wiki community pages: 138   hot.md lines: 46
raw/ files: ['GRAPH_REPORT.md', 'graph.json']
VALIDATION ok: True | orphans: 0 | broken_links: 0 | lint: 0
```

The wrapper, adapter, and models are now exercised by unit tests *and* proven against a
real 2033-node Graphify graph. `graph.html` / vault screenshots remain to be captured;
the semantic (`extract`) pass needs an LLM API key and is deferred to the token-economics
work in Phase 12.
