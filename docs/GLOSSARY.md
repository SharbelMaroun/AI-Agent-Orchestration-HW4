# Project Glossary

> Version: 1.00 | Status: Approved (lecturer sign-off 2026-06-14) | Course: AI Agent Orchestration — HW4 (EX04)

One-sentence definitions with course-source references (L07, Part A, Part B, Part C, Guidelines V3).

| Term | Definition | Source |
|---|---|---|
| Graphify | The free CLI tool that scans a codebase (AST + optional LLM inference) and emits a knowledge graph (`graph.json`, `graph.html`, report). | L07 §3 |
| Obsidian | The Markdown wiki tool that displays and navigates the Graphify graph as the project's "Wikipedia". | L07 §4.1 |
| Vault | The Obsidian root folder defining what is scanned/navigated; choosing it controls token spend. | L07 §5 |
| graph.json | Graphify's machine-readable graph output — nodes, edges, types, confidences, source files; the evidence lens. | L07 §3, Part C |
| graph.html | Graphify's visual graph output — the structure lens. | Part B, Part C |
| REPORT.md | Graphify's verbal run report — context, anomalies, recommendations; the story lens. | Part C |
| hot.md | Vault page with the hottest nodes/entry points/anomalies; course names it but never defines it — ADR-008 fixes the spec. | L07 §11, ADR-008 |
| index.md | The wiki hub page agents read FIRST, then 2–3 targeted pages per query. | Part B (Karpathy LLM Wiki) |
| log.md | The append-only ingestion/decision journal of the vault. | Part B |
| LLM Wiki | The `raw/` → compile → `wiki/` knowledge structure with `index.md` hub and `log.md` journal. | Part B |
| EXTRACTED | Edge type: hard structural link from AST (call/import) — full certainty, fixed confidence 0.95. | L07 §6, Part C |
| INFERRED | Edge type: LLM-derived semantic link carrying a confidence score in 0.55–0.95. | L07 §6, Part C |
| AMBIGUOUS | Edge type: contradictory/unclear link that requires human review; rendered as the red/dotted class. | L07 §6, Part C |
| Confidence range | Every edge carries confidence in [0.55, 0.95]; 0.55 ≈ needs validation, 0.95 ≈ strongest evidence. | Part C |
| Evidence ladder | Conclusion strength scale OBSERVED → INFERRED → EXTRACTED → VALIDATED with matching cautious language. | Part C |
| relation → confidence → source_file | The mandatory reading triple before drawing any conclusion from an edge. | Part C p6 rule |
| Centrality (degree/betweenness) | Node-importance measures: connection count vs how often a node sits on shortest paths (mandatory-flow signal). | L07 §8, Part C |
| Community | A node group with high internal vs external connectivity revealing logical architecture; a hypothesis, not a verdict. | L07 §8.1, Part C |
| COMMUNITY ≠ FOLDER | Communities can cross directory boundaries; never equate a cluster with a package. | Part C |
| Hub | High-connectivity node with alternative paths around it — not inherently dangerous. | L07 §10, Part C |
| Bottleneck | A hub through which flow MUST pass (high betweenness, no redundancy) — an architectural problem. | L07 §10, Part C |
| God node | One module doing unrelated work across communities; split only when classified bottleneck. | Part C |
| Bridge (two senses) | (a) Redundant alternate path — fallback vs duplication trade-off; (b) node/edge connecting two communities — knowledge focal point. | L07 §10.1, Part C |
| SPOF (Single Point of Failure) | A node a critical path depends on with no alternative route (canonical example: the auth chain). | L07 §10.2 |
| Context window bottleneck | The core constraint: what enters the model's attention is scarce; managing it is the real failure mode. | L07 §2, Part B |
| Lost in the Middle | U-curve attention: prompt beginning and end are strong, the middle is a risk zone (Liu et al. 2024). | L07 §9, Part B |
| Compaction | Summarize-and-restart discipline: keep decisions at the edges, drop the noisy middle, reload the relevant skill. | L07 §9, Part B |
| Context rot | Gradual answer-quality decay from accumulated noise before any hard token limit is hit. | Part B |
| RAG limitation | Vector similarity ≠ associative relevance (Movie–Popcorn–Parking); hence graphs over embeddings. | L07 §2.1, Part B |
| SKILL.md | Action-protocol file: YAML frontmatter (name, description, allowed tools), "# When to use", "# Procedure", guardrails. | Part B |
| Guardrail classes | read-only → auto; reversible → undo path required; irreversible → explicit human approval (`disable-model-invocation` for human-only). | Part B |
| Gatekeeper | The single egress module for ALL external API calls, enforcing `config/rate_limits.json`. | Guidelines V3 |
| FIFO overflow queue | Gatekeeper overflow behavior: queue (bounded by `queue.max_depth`), backpressure, drain — never reject, never crash. | Guidelines V3 |
| Token ledger | Per-call token/cost accounting written by the gatekeeper; the data source of the ≥ 70% savings proof. | Guidelines V3, ADR-006 |
| Baseline vs assisted run | Naive full-context answering vs index→2–3-pages graph navigation over the same 10 questions. | ADR-006, Part B |
| Amortization / break-even | The initial graph-scan token cost recovered over N queries (Part A reality check). | Part A p15 |
| Supervisor pattern | LangGraph routing node deciding which agent runs next from typed `AgentState`. | PRD_agent_orchestration |
| AgentState | The typed LangGraph state dict (7 normative fields) flowing between all agents. | PRD_agent_orchestration §3.2 |
| Improvement loop | Apply one fix → QA tests → re-run Graphify → diff metrics → stop-condition evaluation; max 5 iterations. | L07 §11 Core Task 5 |
| Stop conditions | The five Part C p21 per-fix acceptance verdicts (dependencies lost, modularity, no isolation, tests green, ruff 0). | Part C p21, ADR-005 |
| Fix taxonomy P1–P5 | Ordered fix classes: SPOF > bottleneck split > 150-line split > validated duplicates ≥ 0.91 > PRD misalignment. | ADR-010 |
| 150-line cap | Max 150 effective (non-blank, non-comment) lines per code file, tests included; split, never compress. | Guidelines V3 |
| TDD | Red-green-refactor: failing test first, minimal code to green, then refactor; coverage gate ≥ 85%. | Guidelines V3 |
| uv-only | The mandated toolchain: `uv sync` / `uv run` everywhere; pip, virtualenv, venv, and `python -m` are forbidden. | Guidelines V3 |
