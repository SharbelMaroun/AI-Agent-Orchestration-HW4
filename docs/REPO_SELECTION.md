# Target-Repository Selection (EX04)

> Version: 1.04 | Status: Single submitted target | Course: AI Agent Orchestration - HW4 (EX04)

The active submission uses one PDF-listed repository:

- Primary target: `https://github.com/andela/buggy-python`
- Config path: `config/setup.json`
- Graph artifact: `artifacts/buggy-python-graph.json`
- Obsidian vault: `obsidian/`
- Bug report and repair transcript: `deliverables/BUG_REPORT.md`

## 1. Submitted Selection

| Role | Repository | Branch | Reason |
|---|---|---|---|
| Submitted target | `https://github.com/andela/buggy-python` | `master` | PDF-listed debugging corpus; pure Python, stdlib-only, reproducible with the repo's own `main.py` harness |

Implementation note: `config/setup.json` still contains a `fallback_repo` block because the
RepoAgent implementation and tests support one retry path when cloning or validation fails. That
fallback is an internal resilience feature only. It is not used in the submitted graph,
Obsidian vault, bug report, patch, token comparison, or demo output.

## 2. Why This Repo

`andela/buggy-python` is small enough to inspect honestly, but the first failure is still
cross-module: `main.py` imports through the `snippets/__init__.py` re-export hub, and the missing
hub edges hide leaf defects in `loop.py`, `io.py`, and `foobar.py`. That makes it a good fit for
the assignment requirement to show graph-first localization instead of linear file reading.

The repository has no Docker or third-party dependency setup, so the failing-to-passing story is
reproducible in the same uv-managed environment used by this project.

## 3. Evidence

| Requirement | Evidence |
|---|---|
| Graphify graph | `artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md` |
| Obsidian navigation | `obsidian/index.md`, `obsidian/hot.md`, `obsidian/localization.md`, `obsidian/repair.md` |
| Reverse engineering | `obsidian/architecture.md`, `obsidian/findings.md` |
| Bug localization | `src/archlens/agents/bug_localizer.py`, `obsidian/localization.md` |
| Code repair | `deliverables/BUG_REPORT.md` |
| Token efficiency | `metrics/out/debug_token_study.json` |
| Runnable demo | `uv run python src/main.py debug-demo` |
