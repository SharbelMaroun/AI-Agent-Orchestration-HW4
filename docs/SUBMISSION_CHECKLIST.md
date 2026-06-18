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
- [x] Token measurement: baseline vs assisted, **97.08% savings** (real billed gpt-4.1-mini), cost tables (`metrics/out/`)
- [x] SKILL.md files with guardrails + LLM wiki (raw→wiki→index→log)
- [ ] 4 knowledge-quality metrics measured before/after — *illustrative harness only (hardcoded scores); fabricated result removed rather than shown as real (see RETRO)*
- [x] Research notebook + sensitivity analysis + charts (`notebooks/`, `docs/assets/`)
- [x] README.md, CONTRIBUTING.md, LICENSE
- [x] CI/CD workflow (`.github/workflows/ci.yml`) + PR template

## Quality gates

- [x] Tests green (930 tests)
- [x] Branch coverage >= 85% (96.81%)
- [x] Ruff 0 violations
- [x] 150 effective-line cap on every file (incl. tests)
- [x] uv-only toolchain; no pip/virtualenv/venv/requirements.txt
- [x] Secrets policy: `.env` ignored, `.env-example` dummy, gitleaks job
- [x] TDD red-green evidence + mutation spot-checks (3/3 killed)
- [x] Guidelines V3 Table-5 sweep (`docs/COMPLIANCE_TABLE5.md`): all rows PASS

## Release

- [x] Annotated git tag `v1.00` created on the green-gate commit

## Approvals

- [x] **All lecturer approvals granted (2026-06-14)** — recorded in `docs/approvals/` (PRD, all docs,
  target repo, deliverables, research notebook) and reflected by every deliverable doc's Status header
  now reading **Approved**.

## Remaining (your GitHub / course-portal actions only)

Two steps need your GitHub account or the course submission portal — they cannot be done from the
repo itself:

- [ ] **16.011** — open a PR so GitHub Actions runs the CI checks (CI already runs on every push to
  the branch; a PR just surfaces the checks tab).
- [ ] **16.043** — upload the final submission (repo at tag `v1.00`) per the course instructions.
