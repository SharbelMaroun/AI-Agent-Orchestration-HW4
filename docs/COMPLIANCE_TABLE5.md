# Guidelines V3 - Table-5 Quick-Reference Compliance Sweep

Version: 1.01 | Course: AI Agent Orchestration - HW4 (EX04) | Task 16.033

Each Guidelines V3 quick-reference requirement, with verdict and evidence.

| # | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | uv-only toolchain (no pip/virtualenv/venv/`python -m`/requirements.txt) | PASS | `scripts/check_forbidden_tools.py`; `tests/test_check_forbidden_tools.py` |
| 2 | `pyproject.toml` + committed `uv.lock` as single dependency source | PASS | `git ls-files uv.lock`; `uv lock --check` |
| 3 | Test coverage >= 85% (statement + branch) | PASS | `uv run pytest --cov=archlens --cov-branch` -> 941 passed, 1 skipped, 96.80% |
| 4 | Ruff: 0 violations (E,F,W,I,N,UP,B,C4,SIM; ignore E501) | PASS | `uv run ruff check .`; `tests/test_ruff_gate.py` |
| 5 | 150 effective-line cap per file (incl. tests) | PASS | `scripts/check_line_cap.py`; `tests/test_check_line_cap.py` |
| 6 | TDD red-green workflow | PASS | per-phase red/green commit history; mutation spot checks |
| 7 | Config trio (setup/rate_limits/logging) typed + validated | PASS | `tests/test_setup_config.py`, `test_rate_limits_config.py`, `test_logging_setup.py` |
| 8 | Secrets policy (`.env` ignored, `.env-example` dummy, gitleaks) | PASS | `tests/test_env_policy.py`; `.github/workflows/ci.yml` gitleaks job |
| 9 | Single SDK entry point; thin zero-logic CLI | PASS | `tests/test_main_zero_logic.py`; `ArchLensSDK` facade |
| 10 | Gatekeeper-only external calls + FIFO never-reject | PASS | `tests/test_api_call_routing.py`, `test_no_llm_bypass.py`, `test_no_direct_git.py` |
| 11 | Graphify pipeline + Obsidian vault (hot/index/wiki/log) | PASS | `artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md`, `obsidian/` |
| 12 | Reverse-engineering deliverables (block diagram, class schema, audit) | PASS | `deliverables/ARCHITECTURE.md`, `CLASS_SCHEMA.md`, `ALIGNMENT_AUDIT.md`, `BUG_REPORT.md` |
| 13 | Token before/after with >= 70% savings (or amortization/explanation when target is small) | PASS (measured + explained) | `metrics/out/debug_token_study.json`, `metrics/out/token_metrics.json`, `docs/metrics/SAVINGS_EXPLANATION.md` |
| 14 | 4 knowledge-quality metrics measured before/after | PASS | `deliverables/BUG_REPORT.md`, `obsidian/findings.md`, and `metrics/out/debug_token_study.json` document files read, cycles, root-cause quality, and token use |
| 15 | SKILL.md with guardrails + LLM wiki | PASS | `skills/SKILL_graph_reading.md`, `SKILL_refactor.md` |
| 16 | CI/CD pipeline (uv sync --frozen, gates) | PASS | `.github/workflows/ci.yml` |
| 17 | README + PROMPT_BOOK + PRD/PLAN docs | PASS | `README.md`, `docs/PROMPT_BOOK.md`, `docs/PRD.md`, `docs/PLAN.md` |

All Table-5 rows are covered with one submitted target repository: `andela/buggy-python`.
