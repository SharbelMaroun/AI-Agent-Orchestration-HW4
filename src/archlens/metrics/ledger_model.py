"""TokenLedgerEntry — one recorded LLM call in the Phase 12 metrics ledger (task 12.005)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenLedgerEntry:
    """One LLM call's token usage, tagged by agent, model, protocol, question, and prompt id/version.

    ``prompt_id``/``prompt_version`` attribute the call to a specific PROMPT_BOOK entry (FR-AO-11),
    so token deltas are traceable to the exact prompt revision; both default to "" for deterministic
    (non-LLM) calls and for ledgers written before prompt tagging existed.
    """

    agent: str
    model: str
    protocol: str
    input_tokens: int
    output_tokens: int
    question_id: str = ""
    prompt_id: str = ""
    prompt_version: str = ""

    def __post_init__(self) -> None:
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("token counts must be non-negative")
        if not self.agent or not self.model or not self.protocol:
            raise ValueError("agent, model, and protocol are required")

    @property
    def total_tokens(self) -> int:
        """Input plus output tokens for this entry."""
        return self.input_tokens + self.output_tokens
