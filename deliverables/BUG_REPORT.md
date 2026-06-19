# Bug Analysis Report — `andela/buggy-python`

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | EX04 §5.3–5.4, §7

**Target repository:** `https://github.com/andela/buggy-python` — one of the three lecturer-suggested
debugging corpora (§2). Pure Python 3, stdlib only (`json`), no third-party deps, no Docker — so it
reproduces cleanly in our uv-only environment. Cloned (read-only, by reference) into the git-ignored
`runs/buggy-python/`; the repo's own `main.py` is the test harness and **must not be modified** (per its
README) — it encodes the expected behaviour as assertions.

## 1. Symptom (the failing test)

Running the harness on the unmodified clone fails immediately at **import time**:

```text
$ cd runs/buggy-python && PYTHONIOENCODING=utf-8 python main.py
Traceback (most recent call last):
  File ".../runs/buggy-python/main.py", line 3, in <module>
    from snippets import (
ImportError: cannot import name 'lambda_array' from 'snippets'
              (.../runs/buggy-python/snippets/__init__.py)
(exit 1)
```

## 2. Graph-first localization (entry → hub → leaf)

This localization is produced **by the graph-first BugLocalizer** (`sdk.localize_bug` →
`src/archlens/agents/bug_localizer.py::localize_import_failure`, also packaged as the
`make_localizer_node` LangGraph node and driven by the `debug-demo` flow — it is the dedicated
localization component, not one of the seven supervisor-orchestration agents). It traces the
dependency graph and emits the suspect + root cause from the **graph neighbourhood only** — no source
reading (see `obsidian/localization.md` for its verbatim output). It is precisely the cross-module
failure the assignment targets, and the graph localizes it faster than reading files linearly:

- **Entry node** `main.py` imports **6** symbols: `lambda_array, read_file, calculate_unpaid_loans,
  calculate_paid_loans, average_paid_loans, foo`.
- **Hub node** `snippets/__init__.py` is the single re-export point every imported symbol must pass
  through (highest fan-in / a Single-Point-of-Failure in graph terms). It re-exports **only 1** (`foo`).
- **5 missing edges** from the hub to `loop.lambda_array` and `io.{read_file, calculate_unpaid_loans,
  calculate_paid_loans, average_paid_loans}` *are* the first defect — they name the failure site directly.
- Once the hub is restored, the failure **propagates** into the **leaf modules** the hub gates
  (`loop.py`, `io.py`, `foobar.py`), where the remaining defects live. The graph routes the investigation
  entry → hub → which-leaf; the per-line fixes inside each leaf are then local.

A naive approach reads `main.py` plus all of `snippets/*` (every line) to find this; the graph approach
reads the hub node and its missing edges first, then only the implicated leaves.

## 3. Root cause (per file) and the fix

The harness's expected values *define* the correct behaviour; the fixes were derived to satisfy them
(e.g. `calculate_unpaid_loans` must total **11062** → the condition is `status == "unpaid"`, which also
shows the original `!==` was both a syntax error *and* the wrong comparison).

| File | Root cause | Fix |
|---|---|---|
| `snippets/__init__.py` | Re-export hub leaves 5 of 6 imports commented out → `ImportError` before any test runs | Uncomment the `loop`/`io` re-exports |
| `snippets/loop.py` | JS-isms: `lambda_methods = {}` (dict, not list); `for i in 10:` (int not iterable); `lambdamethods.push(...)` (undefined name + `.push`) | `[]`, `range(10)`, `lambda_methods.append(...)` — **late binding preserved** so `lambdas[0](10) == 10+9 == 19` |
| `snippets/io.py` | JS-isms / wrong logic: `data("loans")` (call not subscript); `loan.amount`/`loan.status` (attribute access on dicts); `!==` (invalid + wrong comparison); `is "paid"` (identity not equality); `sun()`/`length()` typos | `data["loans"]`, `loan["amount"]`/`loan["status"]`, `== "unpaid"` / `== "paid"`, `sum()`, `len()`; unpaid set→list |
| `snippets/foobar.py` | Mutable default argument `def foo(bar=[])` accumulates across calls → 2nd call returns `["baz","baz"]` | `bar=None` sentinel, allocate a fresh list per call |

### Fix diff (4 files, +28 / −26)

The exact standalone patch is committed at `deliverables/buggy-python-fix.patch` — a valid unified diff
(`git apply`-able from a fresh `andela/buggy-python` clone root; verified with `git apply --check`).

```diff
# snippets/__init__.py — restore the re-export hub
-# from .loop import lambda_array
-# from .io import (read_file, calculate_unpaid_loans, calculate_paid_loans, average_paid_loans)
+from .loop import lambda_array
+from .io import (read_file, calculate_unpaid_loans, calculate_paid_loans, average_paid_loans)

# snippets/loop.py — JS → Python, keep late binding
-    lambda_methods = {}
-    for i in 10:
-        lambdamethods.push(lambda x: x + i)
+    lambda_methods = []
+    for i in range(10):
+        lambda_methods.append(lambda x: x + i)

# snippets/io.py — dict subscripting, ==, sum/len; the SAME fix applies to all THREE loan funcs:
 def calculate_unpaid_loans(data):
-    loans = data("loans")
-    unpaid_loans = { loan.amount for loan in loans if loan.status !== "unpaid" }
-    return sun(unpaid_loans)
+    loans = data["loans"]
+    unpaid_loans = [ loan["amount"] for loan in loans if loan["status"] == "unpaid" ]
+    return sum(unpaid_loans)
 def calculate_paid_loans(data):
-    loans = data("loans")
-    paid_loans = [ loan.amount for loan in loans if loan.status is "paid" ]
-    return sun(paid_loans)
+    loans = data["loans"]
+    paid_loans = [ loan["amount"] for loan in loans if loan["status"] == "paid" ]
+    return sum(paid_loans)
 def average_paid_loans(data):
-    loans = data("loans"); paid_loans = [ loan.amount for loan in loans if loan.status is "paid" ]
-    sum_paid_loans = sun(paid_loans); number_paid_loans = length(paid_loans)
+    loans = data["loans"]; paid_loans = [ loan["amount"] for loan in loans if loan["status"] == "paid" ]
+    sum_paid_loans = sum(paid_loans); number_paid_loans = len(paid_loans)

# snippets/foobar.py — mutable-default fix
-def foo(bar=[]):
+def foo(bar=None):
+    if bar is None:
+        bar = []
```

## 4. Verification (failing → passing)

```text
$ cd runs/buggy-python && PYTHONIOENCODING=utf-8 python main.py
All test passed successfully!! 😀
(exit 0)
```

All eight assertions pass on the **unmodified** harness: `lambdas[0](10) == 19`, `len(loans) == 15`,
`calculate_unpaid_loans == 11062`, `calculate_paid_loans == 29493.85304`,
`average_paid_loans == 2681.2593672727276`, and `foo() == ["baz"]` on both calls.

## 5. Knowledge before / after (§5.4 — knowledge level)

| | Before investigation | After (graph-guided) |
|---|---|---|
| What we knew | one opaque line — `ImportError: cannot import name 'lambda_array' from 'snippets'`; no idea which of 5 files, or whether it is one bug or many | the failure is a **chain** — entry `main.py` → re-export **hub** `snippets/__init__.py` (the #1-centrality SPOF) → 3 leaf modules, with **4 distinct defects** mapped |
| Obsidian pages | none | `index.md`, `hot.md`, `suspects.md`, `localization.md`, `repair.md`, `architecture.md` |
| Graph evidence | none | the BugLocalizer agent names the hub from its degree + import edges; `contains`/`imports` edges map the leaf defects |
| Code repair evidence | none | `deliverables/buggy-python-fix.patch` plus the passing target harness transcript |

| Architecture view | Before repair | After repair |
|---|---|---|
| Import hub | `snippets/__init__.py` exposes only `foo`; package imports fail at the hub | Hub exports all symbols required by `main.py` |
| Leaf modules | `loop.py`, `io.py`, and `foobar.py` are unreachable or broken behind the failed import | Leaf defects are mapped and repaired while preserving the target harness |
| Verification | Import-time failure, exit 1 | `main.py` prints `All test passed successfully!!`, exit 0 |

The agent + vault turned a single unexplained `ImportError` into a ranked, cited investigation that
named the fix site (the hub) **before** any leaf source was read.

## 6. Reproducibility

```bash
git clone --depth 1 https://github.com/andela/buggy-python runs/buggy-python
cd runs/buggy-python && PYTHONIOENCODING=utf-8 python main.py   # FAILS: ImportError (exit 1)
git apply ../../deliverables/buggy-python-fix.patch             # valid unified diff; paths are repo-root-relative
PYTHONIOENCODING=utf-8 python main.py                            # PASSES: "All test passed successfully!!" (exit 0)
```

The upstream repo has no licence file, so it is referenced by clone (into git-ignored `runs/`), not
vendored into this repository's history.
