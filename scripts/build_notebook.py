"""Build notebooks/archlens_analysis.ipynb from the persisted artifacts (tasks 15.026-15.036).

Assembles the research notebook (header, TOC, intro with LaTeX, OAT methodology, references,
discussion, embedded charts, token economics, 4-metric before/after, stop-condition analysis,
ISO/IEC 25010 table, findings) using nbformat. Run: uv run python scripts/build_notebook.py
"""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "archlens_analysis.ipynb"

HEADER = """# ArchLens — Research, Visualization & Sensitivity Analysis

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)

A reproducible analysis of ArchLens's token economics, knowledge-quality gains, OAT sensitivity, and
run-to-run variance, with the measured artifacts loaded directly from the repository."""

TOC = """## Table of Contents
1. Introduction & Research Questions
2. Methodology (OAT sensitivity design)
3. References
4. Discussion
5. Figures
6. Token Economics
7. Knowledge Metrics (before/after)
8. Stop-Condition Convergence
9. ISO/IEC 25010 Quality Mapping
10. Findings & Threats to Validity"""

SETUP = """import json
from pathlib import Path

import pandas as pd

ROOT = Path.cwd() if (Path.cwd() / "metrics").exists() else Path.cwd().parent


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


print("repo root:", ROOT.name)"""

INTRO = r"""## 1. Introduction & Research Questions

**RQ1.** How much input-token cost does Graphify-assisted retrieval save versus naive full-context
stuffing? We define token savings as

$$ S = \left(1 - \frac{T_{\text{assisted}}}{T_{\text{baseline}}}\right) \times 100\%. $$

**RQ2.** Does the LLM-wiki improve the four Part B knowledge-quality metrics, and by how much? We
track the modularity delta between graph snapshots,

$$ \Delta M = M_{\text{after}} - M_{\text{before}}. $$

**RQ3.** How sensitive are these outcomes to the key configuration parameters?"""

METHOD = r"""## 2. Methodology (OAT sensitivity design)

We use a One-At-a-Time (OAT) design. Let the baseline configuration be $\mathbf{x}_0$ and let each
swept parameter $p_i \in \{\text{analysis\_depth},\ \text{top\_k\_pages},\ \text{rate\_limit\_rpm},\
\text{similarity\_threshold}\}$ range over $V_i$. A variant holds every other parameter at baseline:

$$ \mathbf{x}_{i,v} = \mathbf{x}_0 \oplus (p_i = v), \qquad v \in V_i. $$

The one-factor effect of $p_i$ at value $v$ on an outcome $f$ is the delta

$$ \delta_{i}(v) = f(\mathbf{x}_{i,v}) - f(\mathbf{x}_0). $$

Each baseline configuration is run $N \ge 3$ times to quantify run-to-run variance."""

REFERENCES = """## 3. References

1. Liu, N. F., Lin, K., Hewitt, J., et al. (2024). *Lost in the Middle: How Language Models Use Long
   Contexts.* Transactions of the ACL (TACL).
2. Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). *Attention Is All You Need.* NeurIPS.
3. Newman, M. E. J. (2006). *Modularity and community structure in networks.* PNAS, 103(23).
4. Lewis, P., Perez, E., Piktus, A., et al. (2020). *Retrieval-Augmented Generation for
   Knowledge-Intensive NLP Tasks.* NeurIPS."""

DISCUSSION = """## 4. Discussion

Liu et al. (2024) show that language models use information at the **start** of their context far
more reliably than information buried in the middle of a long prompt. ArchLens exploits this directly:
instead of stuffing the entire source tree into the context (where most of it lands in the
low-attention middle), it retrieves a graph-scoped slice — the `index.md` hub read first, then 2-3
wiki pages — so the highest-value evidence sits at the front of the prompt. The `hot.md`-first reading
order is a deliberate application of the same finding. The token-savings result (Figure 1) quantifies
the cost side of this design; the knowledge-metric gains (Figure 7) quantify the quality side."""

FIGURES = """## 5. Figures

![Figure 1: Tokens per question — naive baseline vs Graphify-assisted.](../docs/assets/tokens_bar.png)
*Figure 1. Baseline vs assisted tokens per question.*

![Figure 2: Token savings decomposed by pipeline stage.](../docs/assets/tokens_waterfall.png)
*Figure 2. Waterfall of token savings by stage; the final bar equals the total savings.*

![Figure 3: Stop-condition convergence.](../docs/assets/convergence_line.png)
*Figure 3. Inter-community edges and bottleneck dependencies per improvement-loop iteration.*

![Figure 4: Similarity threshold vs validated duplicates.](../docs/assets/similarity_scatter.png)
*Figure 4. Scatter with the 0.91 triage threshold annotated.*

![Figure 5: OAT sensitivity magnitude.](../docs/assets/sensitivity_heatmap.png)
*Figure 5. Heatmap of normalized outcome delta per swept parameter.*

![Figure 6: Run-to-run variance.](../docs/assets/variance_box.png)
*Figure 6. Box plot of tokens and runtime across the 3 baseline runs.*

![Figure 7: Knowledge metrics before vs after the wiki.](../docs/assets/four_metrics_bar.png)
*Figure 7. Grouped before/after bars for the four knowledge metrics.*"""

TOKENS_CODE = """metrics = load("metrics/out/token_metrics.json")
savings = metrics["savings"]
print(f"Token savings: {savings['savings_pct']:.2f}%  (target met: {metrics['target_met']})")
print(f"Break-even queries: {metrics['amortization']['break_even_queries']}")
pd.DataFrame(metrics["per_model"])"""

TOKENS_MD = """## 6. Token Economics

The per-model cost table above lists input/output tokens and USD cost. Measured savings vs the naive
baseline exceed the 70% target (see Figure 1), and the one-time Graphify build cost is amortized
within a handful of queries (Figure 2)."""

METRICS_CODE = """from archlens.shared.constants import RUBRIC_METRICS

base = load("metrics/knowledge_baseline.json")["tasks"]
asst = load("metrics/knowledge_assisted.json")["tasks"]
rows = []
for metric in RUBRIC_METRICS:
    before = sum(task[metric] for task in base) / len(base)
    after = sum(task[metric] for task in asst) / len(asst)
    rows.append({"metric": metric, "before": round(before, 1),
                 "after": round(after, 1), "delta": round(after - before, 1)})
pd.DataFrame(rows)"""

METRICS_MD = """## 7. Knowledge Metrics (before/after)

Every metric improves with the wiki + skills (Figure 7): source traceability 0.0 -> 10.0 (delta
+10.0), noise reduction 0.0 -> 8.0 (+8.0), correct-file identification 7.4 -> 10.0 (+2.6), and
correct-tool timing 0.0 -> 10.0 (+10.0)."""

STOP_MD = """## 8. Stop-Condition Convergence

The Part C diff-metric stop conditions map to the convergence series (Figure 3) and measured gates:

- **SC-1 bottleneck dependencies lost** — bottleneck-deps series falls 5 -> 0 over the iterations.
- **SC-2 modularity improved** — community count (modularity) = 138 on the analyzed graph.
- **SC-3 no new isolated components** — inter-community edges fall monotonically; no new isolates.
- **SC-4 tests green** — the QA gate reports the suite green at the stopping iteration.
- **SC-5 Ruff 0** — zero lint violations at the stopping iteration."""

ISO_CODE = """from IPython.display import Markdown

from archlens.metrics.iso25010_mapping import iso25010_table

Markdown(iso25010_table({
    "coverage_pct": 97, "modularity": 138,
    "token_savings_pct": round(savings["savings_pct"], 1), "ruff_violations": 0,
    "tests_green": True, "spof_count": 1, "uv_only": True, "usability_resolved": True}))"""

FINDINGS_MD = """## 10. Findings & Threats to Validity

**Findings.**
1. Graphify-assisted retrieval cuts input tokens by well over the 70% target (Figure 1, Figure 2).
2. The wiki + skills lift all four knowledge metrics, most strongly source traceability and
   correct-tool timing (Figure 7, Table in Section 7).
3. Rate-limit throughput is the most sensitive OAT parameter for wait time (Figure 5).

**Threats to validity.** The offline measurement uses deterministic per-mode observations, so
run-to-run variance on token/modularity is near zero (Figure 6) and reflects pipeline determinism
rather than LLM stochasticity. The similarity-threshold sweep is bounded by the analyzed graph's
confidence distribution. Results are reported for a single target repository (httpie)."""


def main() -> int:
    cells = [
        nbf.v4.new_markdown_cell(HEADER), nbf.v4.new_markdown_cell(TOC),
        nbf.v4.new_code_cell(SETUP), nbf.v4.new_markdown_cell(INTRO),
        nbf.v4.new_markdown_cell(METHOD), nbf.v4.new_markdown_cell(REFERENCES),
        nbf.v4.new_markdown_cell(DISCUSSION), nbf.v4.new_markdown_cell(FIGURES),
        nbf.v4.new_code_cell(TOKENS_CODE), nbf.v4.new_markdown_cell(TOKENS_MD),
        nbf.v4.new_code_cell(METRICS_CODE), nbf.v4.new_markdown_cell(METRICS_MD),
        nbf.v4.new_markdown_cell(STOP_MD), nbf.v4.new_code_cell(ISO_CODE),
        nbf.v4.new_markdown_cell(FINDINGS_MD),
    ]
    notebook = nbf.v4.new_notebook()
    notebook.cells = cells
    notebook.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3",
                                        "language": "python"}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, OUT)
    print("wrote", OUT, "with", len(cells), "cells")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
