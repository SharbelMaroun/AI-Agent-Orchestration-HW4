# ArchLens - Post-Submission Retrospective

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04) | Task 16.045

## Process

ArchLens was built phase by phase (16 phases, about 770 tasks) under a strict TDD red-green
discipline with a 150-effective-line cap on every file, Ruff zero, and a >= 85% branch-coverage
gate enforced locally and in CI. Work proceeded in small committed batches, config-driven throughout
(no hardcoded values outside `shared/constants.py` and config schemas), and every external call
routed through the single gatekeeper egress.

## Metrics Outcome

- **Token savings: 97.08%** - naive full-context baseline 1,368,538 tokens vs Graphify-assisted
  39,950 tokens over 10 standard questions on the real httpie checkout (real billed gpt-4.1-mini,
  $0.58). Break-even after **2 queries** even counting the one-time graph-build cost.
- **Knowledge-quality proxy:** the live with-vs-without-Graphify study over the top 3 bottlenecks
  shows 84.0% fewer tokens at equal judged quality (5.0 vs 5.0). The four Part B metrics are now
  published as a measured proxy in `metrics/out/knowledge_quality_metrics.json` and
  `docs/metrics/KNOWLEDGE_QUALITY_METRICS.md`.
- **Quality gates:** 930 tests green, 96.81% branch coverage, Ruff 0 violations, every file <= 150
  effective lines, and 3/3 analysis mutants killed.

## Lessons Learned

1. **The 150-line cap is a design forcing function, not a nuisance.** It pushed every concern into a
   small, testable unit (SDK mixins, per-stage modules), which kept coverage high and made the
   public-API meta-test feasible.
2. **A real artifact beats a mock.** Running the token and graph measurements against the actual
   httpie graph produced credible numbers and surfaced real data shapes that fixtures would have
   hidden.
3. **Meta-tests catch what unit tests miss.** Public-API and no-bypass guard tests repeatedly flagged
   untested helpers and architecture violations early.
4. **Config-as-single-source-of-truth scales.** Typed pydantic config blocks made sensitivity sweeps
   easy to express and kept the hardcoded-value audit clean.

## Known Issues & Planned Fixes

1. **Obsidian vault community pages are titled by number, not topic.** The generated vault names pages
   `community-0`, `community-1`, and so on. Graphify labels exist in the sidecar output, but the
   vault builder does not yet consume them. Planned fix: read Graphify community labels and render
   `index.md` links as aliases such as `[[community-6|HTTP Adapters and Sessions]]`.

2. **Some research artifacts were removed rather than presented as real.** The stop-condition
   convergence plot was hardcoded/illustrative and remains removed. Planned fix: rebuild it only after
   a real refactor-and-regraph convergence harness exists.

3. **The four knowledge-quality metrics are restored as a proxy, not the original 10-task blind
   rubric.** The previous synthetic harness was removed. The replacement is measured from the live
   `graph_vs_code` study and is suitable as honest evidence, but strict grading may still prefer a
   full 10-task blind rubric over true httpie ground truth.
