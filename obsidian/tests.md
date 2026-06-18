# Tests — How the Fix and the Tooling Are Verified (EX04 §5.1)

The vault page for the **tests** topic the spec asks for. It covers both the target-repo fix
verification and this project's own test suite.

## Verifying the target fix (`andela/buggy-python`)
The repo ships its **own** unmodifiable test harness, `main.py`, which encodes the expected behaviour as
assertions. Success criterion (after applying the [[repair]]):

```text
$ cd runs/buggy-python && PYTHONIOENCODING=utf-8 python main.py
All test passed successfully!! 😀   (exit 0)
```

All 8 assertions pass (`lambdas[0](10) == 19`, `len(loans) == 15`, `calculate_unpaid_loans == 11062`,
`calculate_paid_loans == 29493.85304`, `average_paid_loans == 2681.2593672727276`, and `foo() == ["baz"]`
on both calls). The committed gate is **`../tests/debug/test_buggy_python_entry.py`**, which runs that
harness as a subprocess and asserts `returncode == 0`; it skips cleanly when the git-ignored clone is
absent and points to `../deliverables/BUG_REPORT.md` as the committed proof.

## This project's own suite (ArchLens)
- **936 tests** across the repo module, the Graphify pipeline, the agents, the gatekeeper, the metrics,
  and the vault — full report at **`../reports/test_report.md`**.
- Gates run on every push: **coverage ≥ 85%** (`uv run pytest --cov=archlens --cov-branch`) and
  **zero Ruff violations** (`uv run ruff check .`).
- The improvement loop runs the target suite after **every** change: the Phase-11 `--loop` path uses the
  real `uv run pytest` `TestGate`; mutation spot-checks are in `../reports/mutation_spotchecks.md`.

## Why this matters to the investigation
The graph told us *where* to look ([[hot]], [[suspects]]); the harness told us *whether the fix is
correct*. A green harness is what turned the ranked suspects in [[findings]] into a confirmed
[[repair]].

---
**Navigation:** back to [[index]] · root cause & fix in [[repair]] · research answers in [[findings]].
