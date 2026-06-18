# Knowledge-Quality Metrics

Version: 1.01 | Course: AI Agent Orchestration - HW4 (EX04)

This file records the current knowledge-quality proxy after retargeting the project to the
PDF-listed BugsInPy repository. The measurement is intentionally conservative: the regenerated
`graph_vs_code` run used the local/offline canned response path, so it does **not** prove a quality
improvement.

## Scope

- Source artifact: `metrics/out/graph_vs_code.json`
- Machine-readable result: `metrics/out/knowledge_quality_metrics.json`
- Sample: top 3 bottlenecks from the BugsInPy graph
- Baseline: answer from full source context
- Assisted: answer from Graphify neighbourhood context
- Measured tokens: 45 baseline vs 45 assisted, 0.0% fewer tokens
- LLM-judge quality: 0.0 baseline vs 0.0 assisted

## Scores

| Metric | Baseline | Assisted | Delta | Rationale |
| --- | ---: | ---: | ---: | --- |
| Source traceability | 2 | 2 | +0 | Rows retain `source_file` evidence, but canned responses prevent stronger credit. |
| Noise reduction | 0 | 0 | +0 | The regenerated proxy measured 45 tokens in both arms. |
| Correct-file identification | 0 | 0 | +0 | Both arms scored 0/5 in the local judge path. |
| Correct tool at the right time | 2 | 2 | +0 | The assisted path used Graphify, but the answers were not meaningful. |

Average score: baseline 1.0, assisted 1.0, delta +0.0.

## Submission Note

The project now uses the correct PDF-listed repository, but this specific quality metric should be
expanded with a live 10-task evaluation if the grader expects the full Part B rubric.
