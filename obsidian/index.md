# Index — Bug Investigation: andela/buggy-python

Read this first. **Project:** `andela/buggy-python` (a lecturer-suggested buggy repo, EX04 §2).

## The bug (symptom)
Running the harness `python main.py` fails at import time:
`ImportError: cannot import name 'lambda_array' from 'snippets'` (exit 1).

## The failure chain (entry → hub → leaf)
`main.py` (entry) imports **6** symbols from the `snippets` package → the re-export **hub**
`snippets/__init__.py` → three **leaf** modules `loop.py`, `io.py`, `foobar.py`. The hub re-exports
only **1** of the 6 needed symbols, so the import dies before any assertion runs; once the hub is
fixed, defects in the leaves surface in turn.

## Read next (max 3 — Part B navigation rule)
- [[hot]] — the bug hotspot / ranked suspects from the graph
- [[suspects]] — candidate defect sites with graph evidence
- [[repair]] — per-file root cause and the exact fix

## Artifacts
- `../deliverables/BUG_REPORT.md` — full bug-analysis report (symptom → root cause → fix → verify)
- `../artifacts/buggy-python-graph.json` — the Graphify graph (19 nodes / 28 edges / 4 communities)
