# Reverse-Engineering Deliverables — Human Review Checklist

> Version: 1.00 | Phase 7 (EX04 Core Task 3)
>
> Run `uv run archlens deliverables --graph <canonical graph.json> --src <target src> --prd docs/PRD.md`
> to (re)generate `ARCHITECTURE.md`, `CLASS_SCHEMA.md`, and `ALIGNMENT_AUDIT.md`, then work this list.

## Checklist

1. **Block-diagram accuracy** — every community in `ARCHITECTURE.md` corresponds to a real
   cluster in the target codebase; node count per block looks right.
2. **Block-diagram dependencies** — each inter-block arrow reflects a genuine cross-community
   dependency; edge weights are plausible.
3. **Class-diagram inheritance** — each `<|--` arrow in `CLASS_SCHEMA.md` maps to an actual
   base/derived relationship in the source.
4. **Class-diagram composition** — each `*--` arrow maps to a real has-a relationship
   (attribute instantiation or typed attribute).
5. **Mermaid renders** — paste both fenced blocks into a mermaid viewer (or Obsidian) and
   confirm they render without syntax errors.
6. **Verdict evidence spot-check** — sample 3 verdicts in `ALIGNMENT_AUDIT.md`; confirm each
   cites `relation -> confidence -> source_file` and the cited file actually contains the symbol.
7. **Evidence-tag sampling** — sample 5 claims; confirm each carries exactly one
   `[OBSERVED]` / `[INFERRED]` / `[EXTRACTED]` / `[VALIDATED]` tag and the tag is justified.
8. **Unimplemented requirements** — confirm each listed gap is genuinely unimplemented
   (the searched keywords really do not appear in any module).
9. **Orphan modules** — confirm each orphan module truly maps to no requirement; high-degree
   orphans deserve extra scrutiny.
10. **Shared flows** — confirm each shared-flow module legitimately serves the listed
    requirements; consider whether the coupling is intended.
11. **Confidence bounds** — every reported match confidence is within `[0.55, 0.95]`.
12. **Version headers** — all three deliverables carry a `Version:` header.
13. **Fix patch** - `deliverables/buggy-python-fix.patch` applies to the target repo files named in
    `BUG_REPORT.md` and matches the documented root-cause table.
14. **Submission demo** - `uv run python src/main.py submission-demo` prints the graph artifact,
    Obsidian vault, agent path, fix patch, token comparison, and verification commands.

## Sign-off

| Field | Value |
| --- | --- |
| Reviewer | ____________________ |
| Date | ____________________ |
| Verdict | ☐ Approved ☐ Changes requested |
| Notes | ____________________ |
