# Target-Repository Selection (EX04 Core Task 1)

> Version: 1.00 | Status: Draft — awaiting lecturer approval | Course: AI Agent Orchestration — HW4 (EX04)

All evidence below was produced by real commands run on 2026-06-13 against fresh
`--depth 1` clones. Repo choice does not affect the grade (L07 §11.2) — what matters
is the documented evaluation.

## 1. Selection criteria (each with an objective check)

| # | Criterion | Pass/fail check command |
|---|---|---|
| C1 | Pure Python, importable under a uv env | `uv run --with-editable . python -c "import <pkg>"` exits 0 |
| C2 | Size within bounds (5k–25k Python LOC) | `find . -name '*.py' -exec cat {} + \| wc -l` in [5000, 25000] |
| C3 | Real pytest suite (≥ 10 test files) | `find . -path '*test*' -name '*.py' \| wc -l` ≥ 10 |
| C4 | OSI license present | `test -f LICENSE` and recognized marker in header |
| C5 | uv-managed environment feasible (no pip/venv) | `uv sync` OK **or** `uv run --with-editable .[dev] --with pytest pytest --collect-only` exits 0 |
| C6 | Graphify/AST-parseable (no compiled extensions) | `find . -name '*.so' -o -name '*.pyd' \| wc -l` = 0 |
| C7 | BugsInPy presence (real bug history) | project listed in the BugsInPy registry |

## 2. Candidate shortlist (measured on the actual clones)

| Repo | BugsInPy | Python files / LOC | Test files | License | uv compatibility |
|---|---|---|---|---|---|
| httpie/cli | Yes | 133 / 19,002 | 44 | BSD-3 | **uv-OK** via `--with-editable` (see §3) |
| tqdm/tqdm | Yes | 69 / 9,378 | 20 | MIT/MPL | uv-OK via `--with-editable`; `uv sync` FAIL (see §3) |
| nvbn/thefuck | Yes | 416 / 16,354 | 204 | MIT | setup.py-only; `uv sync` FAIL |
| psf/requests (fallback) | No | ~35 / ~12k (est.) | ~20 (est.) | Apache-2.0 | modern packaging, uv-friendly |
| pallets/click (fallback) | No | ~40 / ~14k (est.) | ~25 (est.) | BSD-3 | modern pyproject, uv-friendly |

## 3. uv-feasibility evidence (mandatory uv-managed environment)

`uv sync` against each clone, isolated in a temp directory (a first in-repo attempt was
invalidated and rerun: uv's workspace discovery silently resolved the *ArchLens* project
when the clone had no `[project]` table — a real pitfall now documented here):

- **tqdm** — `uv sync` **FAIL** (own `[project]` table, but dependency conflict):
  ```text
  hint: The `requires-python` value (>=3.7) includes Python
  versions that are not supported by your dependencies (e.g.,
  pytest-asyncio>=0.25.0,<=1.2.0 only supports >=3.9).
  ```
- **httpie** — `uv sync` **FAIL**: `setup.py`-only, no `[project]` table for uv to manage.
- **thefuck** — `uv sync` **FAIL**: same cause as httpie.

**Working uv-only strategy** (no pip, no virtualenv/venv): ephemeral env via
`uv run --with-editable`:

```text
$ uv run --with-editable <clone> --with pytest python -c "import httpie; ..."
Installed 21 packages in 743ms
httpie import OK 3.2.4

$ uv run --with-editable <clone> python -c "import tqdm; ..."
Installed 2 packages in 43ms
tqdm import OK 0.1.dev1+gea04fc37f
```

## 4. Top-candidate verification (httpie)

```text
$ cd <httpie clone>
$ uv run --with-editable ".[dev]" --with pytest pytest tests -q --collect-only
1028 tests collected in 1.13s

$ uv run --with-editable ".[dev]" --with pytest pytest tests/test_compress.py -q
16 passed, 1 warning in 2.88s
```

Known caveat (recorded per task 3.006): the full httpie suite includes network-marked
tests; the QAAgent will run the offline subset (`-m "not requires_external"` or
equivalent) — exact marker set to be pinned in Phase 11.

## 5. Fallback is a config-only switch

Switching target requires editing only `config/setup.json` keys
`target_repo.{url,branch,pinned_commit}` — or passing `use_fallback=True` to the SDK.
No code changes. Dry-run log:

```text
$ uv run python -c "from archlens.shared.config import load_setup; ..."
primary : https://github.com/httpie/cli
fallback: https://github.com/psf/requests
```

## 6. Recommendation (per-criterion scores)

| Criterion | httpie | tqdm | thefuck | requests |
|---|---|---|---|---|
| C1 import under uv | PASS | PASS | not probed | expected PASS |
| C2 LOC bounds | PASS (19,002) | PASS (9,378) | PASS (16,354) | PASS (est.) |
| C3 pytest suite | PASS (44 files, 1028 tests) | PASS (20) | PASS (204) | PASS (est.) |
| C4 license | PASS (BSD-3) | PASS (MIT/MPL) | PASS (MIT) | PASS (Apache-2.0) |
| C5 uv env | PASS (`--with-editable`) | PASS (`--with-editable`) | FAIL (`uv sync`), not re-probed | expected PASS |
| C6 AST-parseable | PASS | PASS | PASS | PASS |
| C7 BugsInPy | PASS | PASS | PASS | — (fallback only) |

**Primary: `httpie/cli`** — uv-feasible, largest verified test suite (1028 collected),
real BugsInPy bug history, pure Python.
**Fallback: `psf/requests`** — simpler, extensively tested, the documented
L07 §11.2 "don't get stuck" exit. Both are configured in `config/setup.json`.

Note: the PRD Appendix B draft initially proposed tqdm as primary; the measured
`uv sync` failure (above) flipped the recommendation to httpie. Evidence beats drafts.

## 7. Lecturer approval (task 3.009 — BLOCKED)

| Field | Value |
|---|---|
| Requested | 2026-06-13 (see docs/approvals/target_repo_request.md) |
| Approved repo | _pending_ |
| Approval date | _pending_ |
