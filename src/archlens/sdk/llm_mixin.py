"""LLM facade — the single SDK method agents use to send a free-form prompt to the active provider.

Routes through the gatekeeper (the sole egress), so the call is rate-limited, logged, and provider-
agnostic (Anthropic / OpenAI / offline mock). Agents never import an API client; they call ask_llm,
which keeps the no-API-client-in-agents guard satisfied and the single-entry-point invariant intact.
"""

from ..gatekeeper.llm_client import extract_text, resolve_model


class LLMMixin:
    """Single-entry free-form LLM access for the agents."""

    def ask_llm(self, prompt: str, *, system: str | None = None,
               agent: str = "orchestrator", max_tokens: int = 512) -> str:
        """Send one prompt (optional system role) to the active provider via the gatekeeper.

        The system message is provider-agnostic: OpenAI/mock consume the ``system`` role directly,
        and LiveAnthropicClient lifts it into the SDK's top-level ``system`` parameter.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        model = resolve_model(self._config())
        response = self._gk().execute(model, messages, agent=agent, max_tokens=max_tokens)
        return extract_text(response)
