# ArchLens — Post-Submission Retrospective

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Task 16.045

## Process

ArchLens was built phase by phase (16 phases, ~770 tasks) under a strict TDD red-green discipline
with a 150-effective-line cap on every file, ruff-zero, and a >= 85% branch-coverage gate enforced
locally and in CI. Work proceeded in small committed batches (each a coherent red→green slice),
config-driven throughout (no hardcoded values outside `shared/constants.py` and config schemas), and
every external call routed through the single gatekeeper egress. The line cap forced the codebase to
be split into many small, single-purpose modules and SDK mixins rather than a few large files.

## Metrics outcome

- **Token savings: 97.08%** — naive full-context baseline 1,368,538 tokens vs Graphify-assisted
  39,950 tokens over 10 standard questions on the real httpie checkout (real billed gpt-4.1-mini, $0.58).
  Break-even after **2 queries** even counting the one-time graph-build cost.
- **Quality gates:** 904 tests green, 96.96% branch coverage, ruff 0 violations, every file <= 150
  lines, 3/3 analysis mutants killed.

## Lessons learned

1. **The 150-line cap is a design forcing-function, not a nuisance.** It pushed every concern into a
   small, testable unit (SDK mixins, per-stage modules), which kept coverage high and made the
   public-API meta-test feasible. Fighting it (compressing code) would have hurt readability; splitting
   always paid off.
2. **A real artifact beats a mock.** Running the token and knowledge measurements against the actual
   2033-node httpie graph (not synthetic fixtures) produced credible, defensible numbers and surfaced
   real data shapes (e.g. the similarity-threshold distribution) that a fabricated fixture would have
   hidden.
3. **Meta-tests catch what unit tests miss.** The public-API-referenced and no-LLM-bypass guard tests
   repeatedly flagged genuinely-untested helpers and would-be architecture violations the moment they
   were introduced, well before they could rot.
4. **Config-as-single-source-of-truth scales.** Threading every threshold and path through typed
   pydantic config blocks made the OAT sensitivity sweeps trivial to express and kept the "no hardcoded
   values" audit clean at the end.

## Known issues & planned fixes

1. **Obsidian vault community pages are titled by number, not by topic.** The generated vault
   (`runs/vault/wiki/`) names each cluster page `community-0`, `community-1`, … instead of by a
   human-readable topic. The semantic names *do* exist — graphify's LLM `label` step produces them
   (e.g. `community-6` = "HTTP Adapters and Sessions") and stores them in
   `graphify-out/.graphify_labels.json` and the labelled `graph.html` — but the ArchLens vault builder
   titles each page by its numeric cluster id and does not consume that label sidecar, so the two
   outputs are not wired together. The vault is correct and navigable (every page lists its real member
   symbols and the bridge links resolve), but it is harder to browse than topic-named pages would be.
   **Planned fix:** have `src/archlens/vault/builder.py` read the graphify community labels and title
   each `community-N.md` with its semantic name (falling back to `community-N` when no label exists),
   and render the `index.md` links as aliases (`[[community-6|HTTP Adapters and Sessions]]`) so the hub
   reads as topics instead of numbers.

2. **Several "research" results were illustrative stand-ins, now re-measured for real or removed.** A
   late audit found that parts of the research were synthetic rather than measured, so they were
   corrected:
   - **Now real (live, gpt-4.1-mini):** token economics (97.08% savings, $0.58), the top-k and
     run-to-run-variance sweeps, and `analysis_depth` / `rate_limits` (the latter measured through the
     real limiter). `similarity_threshold` already counted real graph edges.
   - **Removed** rather than presented as real: the **stop-condition convergence** plot (the production
     loop's `apply`/`regraph` are no-ops, so the curve had been hardcoded) and the **4 knowledge-quality
     metrics** (`knowledge_eval.py` hard-coded "assisted = perfect, baseline = bad" from the answer key
     over fake ground-truth files; one metric did not map to real behaviour).
   **Planned fix:** restore either honestly by building a real refactor-and-re-graph convergence harness
   and a real LLM-judge knowledge eval against true httpie ground truth.
