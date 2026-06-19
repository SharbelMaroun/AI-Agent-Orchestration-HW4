# Target-Repository Selection (EX04)

> Version: 1.05 | Status: Two PDF-listed targets (procedural debug + class-bearing scale) | Course: AI Agent Orchestration - HW4 (EX04)

The submission uses **two** PDF-listed targets, each playing a distinct role:

- **Class-bearing primary** (OOP / scale / bug): `httpie` — a PDF-listed soarsmu/BugsInPy project
  (`https://github.com/httpie/cli` at buggy commit `8c892edd`). It carries the §5.2 OOP class diagram
  (`deliverables/CLASS_SCHEMA.md`, 44 classes), the headline **live** scale token study
  (`docs/metrics/TOKEN_STUDY_HTTPIE.md`, 79.68% ± 7.91%), and the real BugsInPy bug 4 (Host-header
  overwrite in `HTTPRequest.headers`, `deliverables/BUG_REPORT_httpie.md`). Clone in `runs/httpie-bug`.
- **Focused procedural debug example**: `https://github.com/andela/buggy-python`
  - Config path: `config/setup.json`
  - Graph artifact: `artifacts/buggy-python-graph.json`
  - Obsidian vault: `obsidian/`
  - Bug report and repair transcript: `deliverables/BUG_REPORT.md`

## 1. Submitted Selection

| Role | Repository | Branch / commit | Reason |
|---|---|---|---|
| Class-bearing primary (OOP + scale + bug) | `https://github.com/httpie/cli` (via soarsmu/BugsInPy bug 4) | `8c892edd` | PDF-listed BugsInPy project; real class hierarchy (44 classes) for the §5.2 OOP diagram, a real recorded bug with a regression test, and enough scale for a live 70%+ token study |
| Focused procedural debug example | `https://github.com/andela/buggy-python` | `master` | PDF-listed debugging corpus; pure Python, stdlib-only, reproducible with the repo's own `main.py` harness; the cross-module re-export-hub import failure showcases graph-first localization on a tiny target |

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

## 2.1 Candidates Considered (all three PDF-listed repos)

The assignment (§2) offers three base repositories. We evaluated all three before choosing:

| Candidate | Character | Decision |
|---|---|---|
| `andela/buggy-python` | A few stdlib-only Python scripts with their own `main.py` assertion harness; one cross-module import failure through a package re-export hub. | **CHOSEN (focused procedural debug)** — small enough to investigate honestly, yet the first failure is genuinely cross-module (entry → hub → leaves), which is exactly what graph-first localization is meant to beat linear reading on. No external setup, so the failing→passing story reproduces in the same uv env. |
| `soarsmu/BugsInPy` — **httpie** (bug 4) | Real bugs mined from large real-world projects; the most realistic scenario. We selected one tractable, class-bearing project from this corpus: **httpie**. | **CHOSEN (class-bearing primary)** — httpie is a real OOP codebase (44 classes), giving the §5.2 inheritance/composition class diagram on the investigated target itself, plus a real recorded bug (Host-header overwrite in `HTTPRequest.headers`) with a regression test, and enough scale for a **live** 70%+ token study. We pin the single buggy commit (`8c892edd`) so the bug reproduces deterministically without the full per-project Docker/version-matrix adaptation the PDF warns about for the corpus at large. |
| `martinpeck/broken-python` | A loose collection of broken Python snippets for debugging practice. | **Rejected** — largely Python-2-era, mostly self-contained single-file snippets with little cross-module structure, so it offers a weak dependency graph and a poor fit for the graph-navigation / re-export-hub thesis. (Recorded in `config/setup.json` as "less suitable … py2 snippets".) |

The two chosen targets are complementary: `andela/buggy-python` proves *graph-oriented localization over linear code reading* on a tiny cross-module target with zero environment friction, while the class-bearing `httpie` (via soarsmu/BugsInPy) carries the OOP class diagram, the live scale token study (clearing the 70% target), and a real recorded bug — pinned to one commit to keep BugsInPy's environment cost contained.

## 3. Evidence

| Requirement | Evidence |
|---|---|
| Graphify graph | `artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md` |
| Obsidian navigation | `obsidian/index.md`, `obsidian/hot.md`, `obsidian/localization.md`, `obsidian/repair.md` |
| Reverse engineering | `obsidian/architecture.md`, `obsidian/findings.md` |
| Bug localization | `src/archlens/agents/bug_localizer.py`, `obsidian/localization.md` |
| Code repair | `deliverables/BUG_REPORT.md` (buggy-python); `deliverables/BUG_REPORT_httpie.md` + `scripts/repro_httpie_bug.py` (httpie Host-header bug) |
| OOP class diagram (httpie) | `deliverables/CLASS_SCHEMA.md`, `docs/diagrams/httpie_classes.mmd`, `scripts/gen_httpie_oop.py` |
| Token efficiency | `metrics/out/debug_token_study.json` (buggy-python floor); `metrics/out/token_study_httpie.json` + `docs/metrics/TOKEN_STUDY_HTTPIE.md` (httpie live scale, 79.68%) |
| Runnable demo | `uv run python src/main.py debug-demo` |
