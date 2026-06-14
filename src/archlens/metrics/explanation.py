"""Savings-explanation flow — fills the Part A amortization template when the target is missed (12.039).

When the assisted protocol does not clear the savings target, a written explanation is required
(PRD_token_metrics). This renders the template with the measured numbers, leaving no placeholders.
"""

from pathlib import Path

from .amortization import Amortization
from .savings import Savings

TEMPLATE_MD = Path("docs/metrics/SAVINGS_EXPLANATION_TEMPLATE.md")
EXPLANATION_MD = Path("docs/metrics/SAVINGS_EXPLANATION.md")


def render_explanation(savings: Savings, amortization: Amortization,
                       template_path: str | Path = TEMPLATE_MD) -> str:
    """Render the template with measured savings/amortization numbers; no placeholders remain."""
    text = Path(template_path).read_text(encoding="utf-8")
    break_even = amortization.break_even_queries
    return (text
            .replace("{{savings_pct}}", f"{savings.savings_pct:.2f}")
            .replace("{{graph_build_tokens}}", str(amortization.graph_build_tokens))
            .replace("{{break_even_queries}}", "never" if break_even is None else str(break_even)))


def write_explanation_if_needed(savings: Savings, amortization: Amortization,
                                path: str | Path = EXPLANATION_MD,
                                template_path: str | Path = TEMPLATE_MD) -> Path | None:
    """Write the filled explanation only when the savings target was missed; else return None."""
    if savings.target_met:
        return None
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_explanation(savings, amortization, template_path), encoding="utf-8")
    return target
