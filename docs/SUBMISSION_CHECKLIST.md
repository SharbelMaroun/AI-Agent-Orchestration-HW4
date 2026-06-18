# EX04 Submission Checklist

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04) | Task 16.041

## Deliverables

- [x] PRD.md, PLAN.md, TODO.md, PROMPT_BOOK.md (`docs/`)
- [x] 5 specialized PRDs (gatekeeper, orchestration, improvement-loop, graph-pipeline, token-metrics)
- [x] 10 ADRs + ADR index (`docs/adr/`)
- [x] Target-repo module + validation (RepoAgent)
- [x] Graphify pipeline integration + `graph.json` / `graph.html` / `GRAPH_REPORT.md` (`deliverables/graphify-out/`)
- [x] Obsidian vault: `hot.md`, `index.md`, `wiki/`, `raw/`, `log.md` (`deliverables/bugsinpy-vault/`)
- [x] Graph analysis engine (centrality, communities, hub/bottleneck, bridges, SPOF, triage)
- [x] Reverse-engineering deliverables: block diagram, OOP class schema, PRD-vs-code audit (`deliverables/`)
- [x] SDK single entry point + thin CLI
- [x] API gatekeeper: rate limiting + FIFO never-reject overflow queue
- [x] Multi-agent LangGraph orchestration (supervisor + 7 agents)
- [x] Improvement loop + 5 stop conditions + 5-iteration cap
- [x] Token measurement: baseline vs assisted ledger, **97.08% savings** from the persisted billed development run; BugsInPy graph-vs-code proxy regenerated as inconclusive (`metrics/out/`)
- [x] SKILL.md files with guardrails + LLM wiki (raw -> wiki -> index -> log)
- [x] 4 knowledge-quality metrics regenerated for BugsInPy as an honest inconclusive proxy (`metrics/out/knowledge_quality_metrics.json`, `docs/metrics/KNOWLEDGE_QUALITY_METRICS.md`)
- [x] Research notebook + sensitivity analysis + charts (`notebooks/`, `docs/assets/`)
- [x] README.md, CONTRIBUTING.md, LICENSE
- [x] CI/CD workflow (`.github/workflows/ci.yml`) + PR template

## Quality Gates

- [x] Tests green (930 tests)
- [x] Branch coverage >= 85% (96.81%)
- [x] Ruff 0 violations
- [x] 150 effective-line cap on every file (incl. tests)
- [x] uv-only toolchain; no pip/virtualenv/venv/requirements.txt
- [x] Secrets policy: `.env` ignored, `.env-example` dummy, gitleaks job
- [x] TDD red-green evidence + mutation spot-checks (3/3 killed)
- [x] Guidelines V3 Table-5 sweep (`docs/COMPLIANCE_TABLE5.md`): all rows PASS / documented proxy

## Release

- [x] Annotated git tag `v1.00` created on the green-gate commit

## Approvals

- [x] All lecturer approvals granted (2026-06-14), recorded in `docs/approvals/`.

## Remaining

Two steps need your GitHub account or the course submission portal:

- [ ] **16.011** - open a PR so GitHub Actions surfaces the CI checks tab.
- [ ] **16.043** - upload the final submission (repo at tag `v1.00`) per the course instructions.
