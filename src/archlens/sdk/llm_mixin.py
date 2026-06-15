"""LLM facade — the single SDK method agents use to send a free-form prompt to the active provider.

Routes through the gatekeeper (the sole egress), so the call is rate-limited, logged, and provider-
agnostic (Anthropic / OpenAI / offline mock). Agents never import an API client; they call ask_llm,
which keeps the no-API-client-in-agents guard satisfied and the single-entry-point invariant intact.
"""

from ..gatekeeper.llm_client import extract_text, resolve_model


class LLMMixin:
    """Single-entry free-form LLM access for the agents."""

    def ask_llm(self, prompt: str, *, agent: str = "orchestrator", max_tokens: int = 512) -> str:
        """Send one free-form prompt to the active provider via the gatekeeper; return the reply text."""
        messages = [{"role": "user", "content": prompt}]
        model = resolve_model(self._config())
        response = self._gk().execute(model, messages, agent=agent, max_tokens=max_tokens)
        return extract_text(response)
