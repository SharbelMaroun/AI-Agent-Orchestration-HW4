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

- **Token savings: 97.65%** — naive full-context baseline 1,481,736 tokens vs Graphify-assisted
  34,801 tokens over 10 standard questions on the real httpie checkout. Break-even after **2 queries**
  even counting the one-time graph-build cost.
- **Knowledge quality: all 4 metrics improved** with the wiki + skills (source traceability +10.0,
  noise reduction +8.0, correct-file identification +2.6, correct-tool timing +10.0).
- **Quality gates:** 800+ tests green, 97.35% branch coverage, ruff 0 violations, every file <= 150
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
