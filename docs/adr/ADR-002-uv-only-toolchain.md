# ADR-002 — uv-only toolchain

> Version: 1.00 | Status: Accepted | Course: AI Agent Orchestration — HW4 (EX04)

## Status

Accepted (2026-06-12).

## Context

**Guidelines V3** (the decision driver) forbids `pip`, `virtualenv`, `venv`, and
`python -m` invocations everywhere — code, docs, scripts, CI — and mandates uv with
`pyproject.toml` as the single source of truth.

## Decision

uv exclusively: `uv sync` for environments, `uv run` for every execution
(`uv run pytest`, `uv run ruff check .`), `pyproject.toml` plus a committed `uv.lock`
as the single dependency source; no `requirements.txt` anywhere in the repository.

## Alternatives

- **pip + venv** — rejected: explicitly forbidden by Guidelines V3.
- **poetry/pipenv** — rejected: not the mandated tool; adds a second lockfile format.

## Consequences

\+ Reproducible environment, machine-checkable compliance, fast installs.
− Contributors must install uv first (documented in README). Any forbidden-tool
mention in docs is a graded violation, so the repo is swept by grep (TODO 1.043, 2.042).
