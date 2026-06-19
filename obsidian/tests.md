# Tests - How the Fix and the Tooling Are Verified (EX04)

The vault page for the **tests** topic the spec asks for. It covers both the target-repo fix
verification and this project's own test suite.

## Verifying The Target Fix (`andela/buggy-python`)

The repo ships its **own** unmodifiable test harness, `main.py`, which encodes the expected behaviour
as assertions. Success criterion after applying the repair:

```text
$ cd runs/buggy-python && PYTHONIOENCODING=utf-8 python main.py
All test passed successfully!!   (exit 0)
```

All 8 assertions pass: `lambdas[0](10) == 19`, `len(loans) == 15`,
`calculate_unpaid_loans == 11062`, `calculate_paid_loans == 29493.85304`,
`average_paid_loans == 2681.2593672727276`, and `foo() == ["baz"]` on both calls.

The committed gate is **`../tests/debug/test_buggy_python_entry.py`**, which runs that harness as a
subprocess and asserts `returncode == 0`. It skips cleanly when the git-ignored clone is absent and
points to `../deliverables/BUG_REPORT.md` as the committed reproduction proof.

## This Project's Own Suite (ArchLens)

- **951 passed** (a fresh clone shows **950 passed, 1 skipped** — the debug-harness test is skipped
  until `runs/buggy-python/` is cloned) across the repo module, Graphify pipeline, agents, gatekeeper,
  metrics, and vault. Full report: **`../reports/test_report.md`**.
- Coverage gate: `uv run pytest --cov=src --cov-branch` -> **96.8%** (≥85% enforced).
- Ruff gate: `uv run ruff check .` -> **0 violations**.
- The improvement loop runs QA after changes; mutation spot-checks are in
  `../reports/mutation_spotchecks.md`.

## Why This Matters

The graph told us *where* to look ([[hot]], [[suspects]]); the harness told us *whether the fix is
correct*. A green harness is what turned the ranked suspects in [[findings]] into a confirmed
[[repair]].

---

**Navigation:** back to [[index]] - root cause and fix in [[repair]] - research answers in [[findings]].
