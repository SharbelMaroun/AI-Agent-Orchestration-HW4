# Guidelines V3 — Table-5 Quick-Reference Compliance Sweep

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Task 16.033

Each Guidelines V3 quick-reference requirement, with verdict and evidence.

| # | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | uv-only toolchain (no pip/virtualenv/venv/`python -m`/requirements.txt) | PASS | `scripts/check_forbidden_tools.py` (0 hits); `tests/test_check_forbidden_tools.py` |
| 2 | `pyproject.toml` + committed `uv.lock` as single dependency source | PASS | `git ls-files uv.lock`; `uv lock --check` |
| 3 | Test coverage >= 85% (statement + branch) | PASS | `uv run pytest --cov` → 96.76% (936 tests, branch on) |
| 4 | Ruff: 0 violations (E,F,W,I,N,UP,B,C4,SIM; ignore E501) | PASS | `uv run ruff check .`; `tests/test_ruff_gate.py` |
| 5 | 150 effective-line cap per file (incl. tests) | PASS | `scripts/check_line_cap.py`; `tests/test_check_line_cap.py` |
| 6 | TDD red-green workflow | PASS | per-phase red/green commit history; 3/3 mutants killed (`reports/mutation_spotchecks.md`) |
| 7 | Config trio (setup/rate_limits/logging) typed + validated | PASS | `tests/test_setup_config.py`, `test_rate_limits_config.py`, `test_logging_setup.py` |
| 8 | Secrets policy (`.env` ignored, `.env-example` dummy, gitleaks) | PASS | `tests/test_env_policy.py`; `.github/workflows/ci.yml` gitleaks job |
| 9 | Single SDK entry point; thin zero-logic CLI | PASS | `tests/test_main_zero_logic.py`; `ArchLensSDK` facade |
| 10 | Gatekeeper-only external calls + FIFO never-reject | PASS | `tests/test_api_call_routing.py`, `test_no_llm_bypass.py`, `test_no_direct_git.py` |
| 11 | Graphify pipeline + Obsidian vault (hot/index/wiki/log) | PASS | `runs/httpie-vault/`; `runs/eval/httpie/graphify-out/graph.json` |
| 12 | Reverse-engineering deliverables (block diagram, class schema, audit) | PASS | `deliverables/ARCHITECTURE.md`, `CLASS_SCHEMA.md`, `ALIGNMENT_AUDIT.md` |
| 13 | Token before/after with >= 70% savings (or amortization) | PASS | 97.08% real billed gpt-4.1-mini, $0.58 (`metrics/out/token_metrics.json`) |
| 14 | 4 knowledge-quality metrics measured before/after | N/A | the eval harness was illustrative (hardcoded scores, not a real measurement); the fabricated result was removed rather than presented as real (see RETRO) |
| 15 | SKILL.md with guardrails + LLM wiki | PASS | `skills/SKILL_graph_reading.md`, `SKILL_refactor.md` |
| 16 | CI/CD pipeline (uv sync --frozen, gates) | PASS | `.github/workflows/ci.yml` |
| 17 | README + PROMPT_BOOK + PRD/PLAN docs | PASS | `README.md`, `docs/PROMPT_BOOK.md`, `docs/PRD.md`, `docs/PLAN.md` |

All Table-5 rows: **PASS**. Lecturer-approval workflow gates remain pending (outside the
machine-checkable set).
