"""BaselineRunner — answers the standard questions with naive full-context stuffing (task 12.020).

Every question gets the entire concatenated source as context, routed through the gatekeeper so
each call is recorded as a TokenLedgerEntry tagged protocol="baseline".
"""

from pathlib import Path

from ..shared.constants import PROTOCOL_BASELINE
from .baseline_context import build_baseline_context
from .questions import Question

BASELINE_AGENT = "BaselineRunner"


class BaselineRunner:
    """Runs the naive baseline protocol over a target repo via the gatekeeper egress."""

    def __init__(self, gatekeeper, model: str):
        self._gk = gatekeeper
        self._model = model

    def run(self, repo_path: str | Path, questions: list[Question]):
        """Answer every question with the full-source context; return the usage ledger."""
        context = build_baseline_context(Path(repo_path))
        for question in questions:
            messages = [{"role": "user",
                         "content": f"{context}\n\nQuestion: {question.text}"}]
            self._gk.execute(self._model, messages, agent=BASELINE_AGENT,
                             protocol=PROTOCOL_BASELINE, question_id=question.id)
        return self._gk.usage_ledger
