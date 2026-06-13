"""Typed errors for the Graphify pipeline and graph parsing (Phase 4)."""


class GraphifyError(Exception):
    """Base class for every graphops failure."""


class GraphifyNotFoundError(GraphifyError):
    """The configured Graphify binary could not be executed (not installed / not on PATH)."""


class GraphifyStageError(GraphifyError):
    """A pipeline stage exited non-zero; carries the stage name and captured stderr."""

    def __init__(self, stage: str, stderr: str) -> None:
        self.stage = stage
        self.stderr = stderr
        super().__init__(f"graphify stage {stage!r} failed: {stderr.strip()}")


class GraphParseError(GraphifyError):
    """graph.json failed schema validation; the message names the offending location."""


class GraphSchemaError(GraphifyError):
    """The analysis loader rejected a graph; the message lists every offending node or edge id."""


class TokenBudgetExceededError(GraphifyError):
    """A semantic pass would exceed the configured per-run token budget."""
