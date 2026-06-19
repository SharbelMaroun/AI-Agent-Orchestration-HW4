# EX04 Submission Checklist

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04) | Task 16.041

## Deliverables

- [x] PRD.md, PLAN.md, TODO.md, PROMPT_BOOK.md (`docs/`)
- [x] 5 specialized PRDs (gatekeeper, orchestration, improvement-loop, graph-pipeline, token-metrics)
- [x] 10 ADRs + ADR index (`docs/adr/`)
- [x] Target-repo module + validation (RepoAgent)
- [x] Graphify graph/report for `andela/buggy-python` (`artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md`)
- [x] Obsidian investigation vault: `index.md`, `hot.md`, `localization.md`, `repair.md`, `architecture.md`, `findings.md` (`obsidian/`)
- [x] Graph analysis engine (centrality, communities, hub/bottleneck, bridges, SPOF, triage)
- [x] Reverse-engineering deliverables: block diagram, OOP class schema, PRD-vs-code audit (`deliverables/`)
- [x] Real OOP class diagram (inheritance/composition) on class-bearing primary target `deliverables/CLASS_SCHEMA.md` (httpie, PDF-listed BugsInPy: 44 classes, 19 inheritance + 15 composition)
- [x] Live scale token study, real provider tokens, clears 70% (`metrics/out/token_study_httpie.json`, `docs/metrics/TOKEN_STUDY_HTTPIE.md` — httpie, 79.68% ± 7.91%, n=6)
- [x] httpie BugsInPy bug 4 (Host-header overwrite in `HTTPRequest.headers`) localized, repaired, and reproduced (`deliverables/BUG_REPORT_httpie.md`, `scripts/repro_httpie_bug.py`)
- [x] SDK single entry point + thin CLI
- [x] API gatekeeper: rate limiting + FIFO never-reject overflow queue
- [x] Multi-agent LangGraph orchestration (supervisor + 7 agents)
- [x] Improvement loop + 5 stop conditions + 5-iteration cap
- [x] Extensions / original ideas, dedicated deliverable (`deliverables/EXTENSIONS.md`)
- [x] Token measurement: graph-guided vs naive debug study (`metrics/out/debug_token_study.json`) plus persisted development ledger (`metrics/out/`)
- [x] SKILL.md files with guardrails + LLM wiki (raw -> wiki -> index -> log)
- [x] 4 knowledge-quality metrics documented for the `buggy-python` investigation (`deliverables/BUG_REPORT.md`, `obsidian/findings.md`, `metrics/out/debug_token_study.json`)
- [x] Research notebook + sensitivity analysis + charts (`notebooks/`, `docs/assets/`)
- [x] README.md, CONTRIBUTING.md, LICENSE
- [x] CI/CD workflow (`.github/workflows/ci.yml`) + PR template

## Quality Gates

- [x] Tests green (953 passed; a fresh checkout shows 952 passed, 1 skipped — one debug-harness test is clone-gated)
- [x] Branch coverage >= 85% (96.8%)
- [x] Ruff 0 violations
- [x] 150 effective-line cap on every file (incl. tests)
- [x] uv-only toolchain; no pip/virtualenv/venv/requirements.txt
- [x] Secrets policy: `.env` ignored, `.env-example` dummy, gitleaks job
- [x] TDD red-green evidence + mutation spot-checks (3/3 killed)
- [x] Guidelines V3 Table-5 sweep (`docs/COMPLIANCE_TABLE5.md`): all rows PASS / documented proxy

## Release

- [x] Submission branch is green; create/update final tag after this single-target cleanup commit

## Approvals

- [x] All lecturer approvals granted (2026-06-14), recorded in `docs/approvals/`.

## Remaining

Two steps need your GitHub account or the course submission portal:

- [ ] **16.011** - open a PR so GitHub Actions surfaces the CI checks tab.
- [ ] **16.043** - upload the final submission (repo at tag `v1.00`) per the course instructions.
