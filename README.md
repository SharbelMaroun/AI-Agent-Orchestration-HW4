# ArchLens

Version: 1.00 | Course: AI Agent Orchestration - HW4 / EX04

ArchLens is a graph-guided reverse-engineering and debugging project. The submitted EX04 run uses
one PDF-listed repository end to end:

`https://github.com/andela/buggy-python`

The project builds and uses a code graph, documents the investigation in an Obsidian-style vault,
localizes a real bug with a graph-first agent, explains the repair, and compares graph-guided
debugging with a naive source-reading path.

## Quick Run

From the project root:

```powershell
uv sync; uv run python src/main.py --version; uv run python src/main.py debug-demo; uv run python src/main.py analyze; uv run pytest --cov=archlens --cov-branch
```

Expected high-level output:

- version: `1.00`
- debug target: `https://github.com/andela/buggy-python`
- first suspect: `snippets/__init__.py`
- analysis graph: `19` nodes, `28` edges
- tests: `939 passed, 1 skipped`
- coverage: about `96.80%`

## Submitted Target

| Item | Value |
|---|---|
| Repository | `https://github.com/andela/buggy-python` |
| Reason | PDF-listed, pure Python, stdlib-only, small but cross-module |
| Failing symptom | `ImportError: cannot import name 'lambda_array' from 'snippets'` |
| First fix site | `snippets/__init__.py` |
| Graph artifact | `artifacts/buggy-python-graph.json` |
| Graph report | `artifacts/buggy-python-GRAPH_REPORT.md` |
| Obsidian vault | `obsidian/` |
| Bug report | `deliverables/BUG_REPORT.md` |
| Token study | `metrics/out/debug_token_study.json` |

The committed Graphify report has 19 nodes, 28 edges, and 4 Graphify communities. The ArchLens
`analyze` command reports 3 density communities using the project's internal detector.

## What The Run Does

`uv run python src/main.py debug-demo` prints the assignment-aligned debugging flow:

1. Reads the committed `buggy-python` graph.
2. Uses the `BugLocalizer` graph-first agent.
3. Traces the failure from `main.py` to the package re-export hub.
4. Identifies `snippets/__init__.py` as the first file to fix.
5. Explains the root cause and repair path.
6. Points to the Obsidian notes, bug report, and token study.

`uv run python src/main.py analyze` reads the submitted graph artifact and reports the architectural
summary:

```text
AnalysisReport(node_count=19, edge_count=28, community_count=3,
  hubs=('snippets_init', 'main', 'snippets_io', 'readme_buggy_python', 'snippets_foobar'),
  bottlenecks=('snippets_io', 'readme_buggy_python', 'snippets_foobar', 'snippets_loop'),
  spofs=())
```

## Bug Story

The target repo's `main.py` imports six symbols from `snippets`. The graph shows this path:

```text
main.py -> snippets/__init__.py -> leaf modules
```

The re-export hub `snippets/__init__.py` exposes only part of the package API, so importing
`lambda_array` fails before the test harness can run. After the hub is restored, the remaining leaf
bugs are in:

- `snippets/loop.py`
- `snippets/io.py`
- `snippets/foobar.py`

The full root-cause table, diff, and failing-to-passing transcript are in
`deliverables/BUG_REPORT.md`.

## Graph And Obsidian Evidence

Read these files first:

- `obsidian/index.md` - investigation overview
- `obsidian/hot.md` - graph hotspots
- `obsidian/localization.md` - BugLocalizer output
- `obsidian/suspects.md` - ranked suspects
- `obsidian/repair.md` - repair notes
- `obsidian/architecture.md` - block/OOP diagrams
- `obsidian/findings.md` - assignment research questions
- `obsidian/tests.md` - verification notes

## Token Efficiency

The debug token study compares locating the first file to fix with and without graph navigation:

| Metric | Naive | Graph-guided |
|---|---:|---:|
| Input tokens | 802 | 685 |
| Files / units read | 5 | 2 |
| Investigation cycles | 2 | 1 |
| Correct first fix site | `snippets/__init__.py` | `snippets/__init__.py` |

On this small repo, the token saving is modest (14.59%), but the graph path reads 60% fewer
files/units and reaches the correct hub in one cycle.

## Deliverables Map

| PDF requirement | Evidence |
|---|---|
| Choose a PDF-listed repo | `config/setup.json`, `docs/REPO_SELECTION.md` |
| Graphify representation | `artifacts/buggy-python-graph.json`, `artifacts/buggy-python-GRAPH_REPORT.md` |
| Obsidian documentation | `obsidian/` |
| Reverse engineering | `deliverables/ARCHITECTURE.md`, `deliverables/CLASS_SCHEMA.md`, `obsidian/architecture.md` |
| Agentic debugging | `src/archlens/agents/bug_localizer.py`, `obsidian/localization.md` |
| Code repair | `deliverables/BUG_REPORT.md` |
| Token proof | `metrics/out/debug_token_study.json`, `docs/metrics/GRAPH_VS_CODE.md` |
| Quality gates | `uv run pytest --cov=archlens --cov-branch` |

## Useful Commands

```powershell
uv sync
uv run python src/main.py --version
uv run python src/main.py debug-demo
uv run python src/main.py analyze
uv run pytest --cov=archlens --cov-branch
uv run ruff check .
uv run python scripts/check_line_cap.py
uv run python scripts/check_forbidden_tools.py
```

## Project Structure

```text
artifacts/                 committed target graph/report
config/setup.json           active target repo config
deliverables/               submission reports
docs/                       PRDs, plan, metrics, checklists
metrics/out/                token and comparison outputs
obsidian/                   Obsidian-style investigation vault
skills/                     graph-reading/refactor guidance
src/archlens/               application source
tests/                      regression and quality tests
```

## Notes

- `runs/` is git-ignored and used for local cloned repos or generated runs.
- The target project is procedural, so the class schema intentionally contains no classes.
- The skipped test is expected when `runs/buggy-python` is absent; `deliverables/BUG_REPORT.md`
  documents how to reproduce the target harness manually.

## License & Credits

Course: AI Agent Orchestration HW4 / EX04. Graph generation is based on Graphify-style artifacts.
The submitted debugging corpus is `andela/buggy-python`. Dependencies are listed in
`pyproject.toml` and locked in `uv.lock`.
