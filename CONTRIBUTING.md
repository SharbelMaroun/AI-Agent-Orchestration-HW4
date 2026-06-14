# Contributing to ArchLens

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)

## Feature-branch naming

- Branch off the main branch for every change: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`,
  `test/<topic>`, or `chore/<topic>` (e.g. `feat/token-ledger`, `fix/retry-backoff`).
- One logical change per branch; keep branches short-lived and rebased on the main branch.
- Never commit directly to the main branch — open a pull request.

## Pull-request review rules

- Every PR targets the main branch and must pass all CI gates before review.
- At least one approving review is required before merge; the author does not self-approve.
- PRs use the checklist in `.github/PULL_REQUEST_TEMPLATE.md`; every box must be ticked.
- Squash-or-rebase merges only — keep the main-branch history linear.

## Commit-message style

- Imperative subject line scoped by phase/area, e.g. `Phase 12 (batch M1): token ledger model`.
- A short body explaining the *why*; reference task IDs where helpful.
- Co-authorship trailers are preserved; do not bypass hooks or signing.

## uv-only command policy

- uv is the single toolchain. Every command runs through `uv run ...`
  (`uv run pytest`, `uv run ruff check .`, `uv run python src/main.py`).
- `pyproject.toml` plus the committed `uv.lock` are the only dependency source.
- pip, virtualenv, venv, and `python -m` invocations are forbidden everywhere — code, docs, and CI;
  `requirements.txt` files are not allowed. The scanner `scripts/check_forbidden_tools.py` enforces
  this on every push.
