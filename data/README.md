# `data/` — Input data

This is the `data/` directory from the EX04 §9 recommended layout. ArchLens has **no static input
corpus to vendor**: its inputs are GitHub repositories fetched at run time (the EX04 debugging subject
`andela/buggy-python` and the architectural-demo `httpie/cli`), and `git`/Graphify clone them — through
the gatekeeper — into the **git-ignored `runs/<run_id>/`** working area rather than committing them here.

So this directory is intentionally a placeholder:

- **Runtime inputs** (cloned target repos) → `runs/` (git-ignored; see `.gitignore` and the data-flow
  table in `docs/PLAN.md` §8).
- **Graph artifacts** produced from those inputs → `artifacts/` (e.g. `buggy-python-graph.json`,
  `buggy-python-GRAPH_REPORT.md`).
- **Test inputs / fixtures** → `tests/fixtures/`.
- **Metric outputs** → `metrics/out/` and `results/`.

Drop any static input dataset here if a future run needs one; nothing in the pipeline depends on this
folder being populated.
