# Suspects — Ranked Candidate Defects

Derived from the import/call graph (`../artifacts/buggy-python-graph.json`), tracing from the failing
entry point — not from reading the whole codebase. The #1 suspect is produced **by the BugLocalizer
agent** (`sdk.localize_bug` / `make_localizer_node`), graph-first — see [[localization]].

## 1. `snippets/__init__.py` — the re-export hub (PRIMARY)
- **Graph evidence:** highest degree (9); `main` needs 6 symbols but the hub provides only 1 (`foo`);
  the 5 expected `imports` edges from the hub are **missing**.
- **Symptom:** `ImportError: cannot import name 'lambda_array' from 'snippets'`.
- **Verdict:** confirmed root cause of the entry-point failure → see [[repair#hub-snippetsinitpy]].

## 2. `snippets/loop.py` — `lambda_array` (gated by the hub)
- JS-isms: dict instead of list, `for i in 10`, `.push`. → [[repair#leaf-snippetslooppy]].

## 3. `snippets/io.py` — loan calculations (BOTTLENECK)
- dict-call vs subscript, `!==`, `is`, `sun`/`length` typos, wrong unpaid condition. → [[repair#leaf-snippetsiopy]].

## 4. `snippets/foobar.py` — `foo` (self-contained — graph adds little here)
- mutable default argument accumulates across calls. → [[repair#leaf-snippetsfoobarpy]].
