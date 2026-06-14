"""AssistedRunner — answers the standard questions from the Graphify vault (task 12.025).

Each question is answered from a compact vault+graph context (never raw source), routed through the
gatekeeper so every call is recorded as a TokenLedgerEntry tagged protocol="assisted".
"""

from ..shared.constants import MAX_WIKI_PAGES_PER_QUESTION, PROTOCOL_ASSISTED
from .assisted_retriever import AssistedRetriever
from .questions import Question

ASSISTED_AGENT = "AssistedRunner"


class AssistedRunner:
    """Runs the Graphify-assisted protocol via the gatekeeper egress."""

    def __init__(self, gatekeeper, model: str, vault_root, graph_json=None,
                 max_wiki_pages: int = MAX_WIKI_PAGES_PER_QUESTION):
        self._gk = gatekeeper
        self._model = model
        self._retriever = AssistedRetriever(vault_root, max_wiki_pages)
        self._graph_json = graph_json

    def run(self, questions: list[Question]):
        """Answer every question from vault+graph context; return the usage ledger."""
        for question in questions:
            context = self._retriever.retrieve(question, self._graph_json)
            messages = [{"role": "user", "content": context}]
            self._gk.execute(self._model, messages, agent=ASSISTED_AGENT,
                             protocol=PROTOCOL_ASSISTED, question_id=question.id)
        return self._gk.usage_ledger
