# Mutation Spot-Checks

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Task 13.052

Three hand-applied mutants on the analysis engine, each reverted immediately after verification.
Every mutant was **killed** (caught by at least one failing test), confirming the assertions are
meaningful and not vacuous.

| # | Mutation | File | Killing test(s) | Result |
|---|----------|------|-----------------|--------|
| 1 | Invert the duplicate-similarity threshold comparison (`>= threshold` → `< threshold`) | `graphops/duplicates.py` | `test_duplicates.py::test_duplicate_boundary_flags_091_and_ignores_0909`, `test_duplicates_never_merge_only_route_to_review`, `test_flow_detector.py::test_duplicate_flow_at_threshold_detected` | KILLED |
| 2 | Swap the hub/bottleneck branch (`"BOTTLENECK" if bypass == 0 else "HUB"` → reversed) | `graphops/classify.py` | `test_classify.py::test_verdict_labels_healthy_hub_as_hub`, `test_verdict_labels_bottleneck_as_bottleneck` | KILLED |
| 3 | Drop betweenness normalization (`betweenness_centrality(graph)` → `..., normalized=False`) | `graphops/centrality.py` | `test_centrality.py::test_betweenness_on_barbell_matches_hand_computed` | KILLED |

**Method:** each mutant was applied in-place, the targeted `tests/graphops/` module was run to
confirm a failure, then the source file was restored with `git checkout --`. After all three runs,
`git status --porcelain src/archlens/graphops/` was empty (clean working tree).

**Conclusion:** 3/3 mutants killed — the duplicate threshold, hub/bottleneck classification, and
centrality normalization are each protected by a hand-computed/boundary assertion.
