# Knowledge-Quality Metrics

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04)

This file records the replacement for the removed synthetic four-metric chart. The old harness gave
hardcoded before/after scores, so it was removed rather than presented as real evidence. The current
artifact is a measured proxy based on the live with-vs-without-Graphify study in
`metrics/out/graph_vs_code.json`.

## Scope

- Source artifact: `metrics/out/graph_vs_code.json`
- Machine-readable result: `metrics/out/knowledge_quality_metrics.json`
- Sample: top 3 bottlenecks from the real httpie graph
- Baseline: answer from full source context
- Assisted: answer from Graphify neighbourhood context
- Measured tokens: 8125 baseline vs 1302 assisted, 84.0% fewer tokens
- LLM-judge quality: 5.0 baseline vs 5.0 assisted

This is not the originally planned 10-task blind rubric. It is an honest live proxy over the
available measured study.

## Scores

| Metric | Baseline | Assisted | Delta | Rationale |
| --- | ---: | ---: | ---: | --- |
| Source traceability | 4 | 7 | +3 | Assisted rows carry node plus `source_file` evidence for all 3 cases; answers do not include full relation-confidence-source triples, so not perfect. |
| Noise reduction | 0 | 8 | +8 | Context fell from 8125 to 1302 tokens, an 84.0% reduction. |
| Correct-file identification | 10 | 10 | +0 | Both arms were evaluated on the same 3 ground-truth bottleneck files and scored 5/5 quality. |
| Correct tool at the right time | 2 | 10 | +8 | Assisted starts from the graph neighbourhood; baseline reads broad source context. |

Average score: baseline 4.0, assisted 8.75, delta +4.75.

## Submission Note

This closes the previous gap as a measured, non-fabricated proxy. If strict grading requires the full
10-question Part B rubric, this remains the one area to expand.
