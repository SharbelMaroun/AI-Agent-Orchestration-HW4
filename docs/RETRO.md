# ArchLens - Post-Submission Retrospective

Version: 1.01 | Course: AI Agent Orchestration - HW4 (EX04) | Task 16.045

## Process

ArchLens was built phase by phase under strict TDD red-green discipline with a
150-effective-line cap, Ruff zero, and a >= 85% branch-coverage gate. Work stayed
config-driven, and external calls route through the single gatekeeper egress.

## Metrics Outcome

- **Token savings: 97.08%** - naive full-context baseline 1,368,538 tokens vs Graphify-assisted
  39,950 tokens over 10 standard questions on the historical httpie scale study. Break-even after
  **2 queries** even counting the one-time graph-build cost.
- **Single submitted target:** the active configured target is now the PDF-listed
  `andela/buggy-python` repository.
- **Debugging evidence:** the submission includes a concrete graph-first bug-localization and repair
  track (`deliverables/BUG_REPORT.md`, `obsidian/`, `artifacts/`).
- **Quality gates:** merge verification passed with 938 tests, 1 skipped, 96.75% coverage, Ruff 0,
  line cap OK, forbidden-tooling 0, and mutation spot checks retained.

## Lessons Learned

1. **The 150-line cap is a design forcing function, not a nuisance.** It pushed every concern into a
   small, testable unit.
2. **A real artifact beats a mock.** Running measurements against real graphs surfaced data shapes
   fixtures would have hidden.
3. **Meta-tests catch what unit tests miss.** Public-API and no-bypass guard tests repeatedly flagged
   architecture violations early.
4. **Config-as-single-source-of-truth scales.** Typed config blocks made repo retargeting possible
   without code rewrites.

## Known Issues & Planned Fixes

1. **Obsidian vault community pages are titled by number, not topic.** Planned fix: consume Graphify
   labels and render readable aliases in `index.md`.
2. **Some research artifacts are scoped as historical or supportive.** The project keeps them honest
   rather than presenting stale measurements as current target proof.
3. **The full 10-task blind quality rubric remains the best next expansion.** The current debug
   study is honest and reproducible, but a live full-rubric run would be stronger.
