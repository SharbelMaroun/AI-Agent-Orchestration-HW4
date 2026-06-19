"""Build notebooks/archlens_analysis.ipynb from the persisted artifacts (tasks 15.026-15.036).

Assembles the research notebook (header, TOC, intro with LaTeX, OAT methodology, references,
discussion, embedded charts, token economics, ISO/IEC 25010 table, findings) using nbformat.
Run: uv run python scripts/build_notebook.py
"""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "archlens_analysis.ipynb"

HEADER = """# ArchLens — Research, Visualization & Sensitivity Analysis

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)

A reproducible analysis of ArchLens's token economics, OAT sensitivity, and run-to-run variance, with
the measured artifacts loaded directly from the repository."""

TOC = """## Table of Contents
1. Introduction & Research Questions
2. Methodology (OAT sensitivity design)
3. References
4. Discussion
5. Figures
6. Token Economics
7. ISO/IEC 25010 Quality Mapping
8. Findings & Threats to Validity"""

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

**RQ2.** How sensitive are these outcomes to the key configuration parameters (one-at-a-time design)?"""

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
the cost side of this design."""

FIGURES = """## 5. Figures

> Figures 1, 2 and 6 visualize the **broad knowledge-retrieval pilot** (study B in §6, ~97% on a
> 10-question full-context baseline), *not* the conservative 14.59% focused headline (study A).

![Figure 1: Tokens per question — full-context baseline vs Graphify-assisted.](../docs/assets/tokens_bar.png)
*Figure 1. Broad pilot: input tokens per question, full-context baseline vs Graphify-assisted (live gpt-4.1-mini).*

![Figure 2: Token savings decomposed by pipeline stage.](../docs/assets/tokens_waterfall.png)
*Figure 2. Broad pilot: waterfall of token savings by stage; the final bar equals the total savings.*

![Figure 3: Similarity threshold vs validated duplicates.](../docs/assets/similarity_scatter.png)
*Figure 3. Scatter with the 0.91 triage threshold annotated.*

![Figure 4: OAT sensitivity magnitude.](../docs/assets/sensitivity_heatmap.png)
*Figure 4. Heatmap of normalized outcome delta per swept parameter.*

![Figure 5: Run-to-run variance.](../docs/assets/variance_box.png)
*Figure 5. Box plot of tokens and runtime across the 3 baseline runs.*

![Figure 6: Break-even line chart.](../docs/assets/break_even_line.png)
*Figure 6. Broad pilot: cumulative tokens vs query count; the one-time Graphify build cost T_build is
the assisted curve's y-intercept and the curves cross at the break-even query count (PRD_token_metrics
§9 / FR-TM-10).*"""

TOKENS_CODE = """metrics = load("metrics/out/token_metrics.json")
savings = metrics["savings"]
print(f"Token savings: {savings['savings_pct']:.2f}%  (target met: {metrics['target_met']})")
print(f"Break-even queries: {metrics['amortization']['break_even_queries']}")
pd.DataFrame(metrics["per_model"])"""

TOKENS_MD = """## 6. Token Economics

We report two complementary, separately-measured token studies.

**(A) Focused debug-localization study — the submission headline.** The cell above loads
`metrics/out/token_metrics.json` (regenerated reproducibly from `metrics/out/debug_token_study.json`
by `scripts/build_token_metrics.py`). Locating the first fix site in `andela/buggy-python` used **685
input tokens graph-guided vs 802 naive — 14.59% fewer**, with **60% fewer files read (2 vs 5)** and
**1 vs 2 investigation cycles**. On this intentionally tiny 5-file target the token delta is modest and
does **not** reach the lecture's 70% target (`target_met = false`); the dominant benefit here is
navigation, not raw token count — see `docs/metrics/SAVINGS_EXPLANATION.md`.

**(B) Live scale study (httpie).** A **live** measurement with **real provider token counts**
(gatekeeper ledger deltas, not a `chars//4` estimate) over the class-bearing PDF-listed BugsInPy repo
httpie: graph-scoped retrieval (the AST class map + the one focused module) saves a mean
**79.68% +/- 7.91%** input tokens across six reverse-engineering questions (range 67.7-87.8%), cutting
files read **13 -> 2** and cycles **13 -> 1** with **6/6 (100%)** correct guided localization,
**clearing the lecture's 70% target**. Artifact `metrics/out/token_study_httpie.json`; see
`docs/metrics/TOKEN_STUDY_HTTPIE.md`. The two studies are complementary and never blended:
`buggy-python` is the conservative floor (14.59%), `httpie` is the live scale result. (Figures 1-2/6
below illustrate an *earlier exploratory* ledger pilot.)"""

ISO_CODE = """from IPython.display import Markdown

from archlens.metrics.iso25010_mapping import iso25010_table

Markdown(iso25010_table({
    "coverage_pct": 97, "modularity": 144,
    "token_savings_pct": round(savings["savings_pct"], 1), "ruff_violations": 0,
    "tests_green": True, "spof_count": 1, "uv_only": True, "usability_resolved": True}))"""

FINDINGS_MD = """## 8. Findings & Threats to Validity

**Findings.**
1. On the focused debug-localization task (study A), Graphify-assisted retrieval cut input tokens by
   **14.59%** and files read by **60%** (one cycle to the fix site); on this tiny target the headline
   benefit is navigation, not clearing the 70% token bar (`target_met = false`).
2. On the live scale study (study B, `httpie`, real provider tokens, n=6), graph-scoped retrieval
   saves **79.68% ± 7.91%** input tokens (files 13→2, cycles 13→1, 6/6 localization) — **clearing the
   70% target** on a medium real repo.
3. Context size is the most sensitive OAT outcome: `top_k_pages` and `analysis_depth` move the
   assembled-context token count materially (Figure 4); the rate-limit model is analytical.

**Threats to validity.** The focused study is a single localization task (n=1) on a 5-file target, so
its 14.59% is conservative; the scale study measures **input context size** (the lecture's core claim)
with real provider token counts over six questions, not a live multi-turn agent loop. Per-question
counts are near-deterministic, so run-to-run variance (Figure 5) is dominated by wall-clock runtime.
Results span two targets: `andela/buggy-python` (focused procedural debugging) and `httpie` (OOP class
diagram + live scale token study + Host-header bug)."""


def main() -> int:
    cells = [
        nbf.v4.new_markdown_cell(HEADER), nbf.v4.new_markdown_cell(TOC),
        nbf.v4.new_code_cell(SETUP), nbf.v4.new_markdown_cell(INTRO),
        nbf.v4.new_markdown_cell(METHOD), nbf.v4.new_markdown_cell(REFERENCES),
        nbf.v4.new_markdown_cell(DISCUSSION), nbf.v4.new_markdown_cell(FIGURES),
        nbf.v4.new_code_cell(TOKENS_CODE), nbf.v4.new_markdown_cell(TOKENS_MD),
        nbf.v4.new_code_cell(ISO_CODE), nbf.v4.new_markdown_cell(FINDINGS_MD),
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
