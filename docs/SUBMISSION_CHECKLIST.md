# EX04 Submission Checklist

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Task 16.041

## Deliverables

- [x] PRD.md, PLAN.md, TODO.md, PROMPT_BOOK.md (`docs/`)
- [x] 5 specialized PRDs (gatekeeper, orchestration, improvement-loop, graph-pipeline, token-metrics)
- [x] 10 ADRs + ADR index (`docs/adr/`)
- [x] Target-repo module + validation (RepoAgent)
- [x] Graphify pipeline integration + `graph.json` / `graph.html` / `GRAPH_REPORT.md`
- [x] Obsidian vault: `hot.md`, `index.md`, `wiki/` (138 pages), `log.md` (`runs/httpie-vault/`)
- [x] Graph analysis engine (centrality, communities, hub/bottleneck, bridges, SPOF, triage)
- [x] Reverse-engineering deliverables: block diagram, OOP class schema, PRD-vs-code audit
- [x] SDK single entry point + thin CLI
- [x] API gatekeeper: rate limiting + FIFO never-reject overflow queue
- [x] Multi-agent LangGraph orchestration (supervisor + 7 agents)
- [x] Improvement loop + 5 stop conditions + 5-iteration cap
- [x] Token measurement: baseline vs assisted, **97.65% savings**, cost tables (`metrics/out/`)
- [x] SKILL.md files with guardrails + LLM wiki (raw→wiki→index→log)
- [x] 4 knowledge-quality metrics measured before/after
- [x] Research notebook + sensitivity analysis + charts (`notebooks/`, `docs/assets/`)
- [x] README.md, CONTRIBUTING.md, LICENSE
- [x] CI/CD workflow (`.github/workflows/ci.yml`) + PR template

## Quality gates

- [x] Tests green (800+ tests)
- [x] Branch coverage >= 85% (97.35%)
- [x] Ruff 0 violations
- [x] 150 effective-line cap on every file (incl. tests)
- [x] uv-only toolchain; no pip/virtualenv/venv/requirements.txt
- [x] Secrets policy: `.env` ignored, `.env-example` dummy, gitleaks job
- [x] TDD red-green evidence + mutation spot-checks (3/3 killed)
- [x] Guidelines V3 Table-5 sweep (`docs/COMPLIANCE_TABLE5.md`): all rows PASS

## Release

- [x] Annotated git tag `v1.00` created on the green-gate commit

## Pending external workflow gates (not machine-checkable)

These require lecturer/GitHub actions outside the repository and are tracked in `docs/TODO.md`:
lecturer approvals (PRD/docs/target-repo/research sign-off), GitHub branch protection, the live CI
PR-check run, final submission upload, and lecturer receipt confirmation.
