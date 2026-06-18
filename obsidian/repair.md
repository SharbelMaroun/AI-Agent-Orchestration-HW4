# Repair — Root Cause and Fix (per file)

Fixes applied in the order the trace surfaces them. **Verified:** `python main.py` →
`All test passed successfully!! 😀` (exit 0). Full diff + transcript: `../deliverables/BUG_REPORT.md`.

## Hub: `snippets/__init__.py`
Root cause: 5 of 6 re-exports commented out. Fix: uncomment the `loop` and `io` re-exports.

## Leaf: `snippets/loop.py`
`{}` → `[]`; `for i in 10:` → `for i in range(10):`; `lambdamethods.push(...)` →
`lambda_methods.append(...)`. Late binding preserved so `lambdas[0](10) == 10+9 == 19`.

## Leaf: `snippets/io.py`
`data("loans")` → `data["loans"]`; `loan.amount`/`loan.status` → `loan["amount"]`/`loan["status"]`;
`!== "unpaid"` → `== "unpaid"` (derived from the assertion total **11062**); `is "paid"` → `== "paid"`;
`sun()` → `sum()`; `length()` → `len()`.

## Leaf: `snippets/foobar.py`
`def foo(bar=[])` → `def foo(bar=None): if bar is None: bar = []` (fresh list per call).
