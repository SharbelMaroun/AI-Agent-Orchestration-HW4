"""ArchLens exception taxonomy with machine-readable codes (task 8.008)."""

from archlens.shared.constants import EXCEPTION_CODE_PREFIX


class ArchLensError(Exception):
    """Base for every ArchLens error; carries a machine-readable code and source context."""

    code = f"{EXCEPTION_CODE_PREFIX}-000"

    def __init__(self, message: str = "", source_context: str | None = None,
                 retryable: bool = False) -> None:
        self.source_context = source_context
        self.retryable = retryable
        super().__init__(message)


class ConfigError(ArchLensError):
    """A configuration file is missing, malformed, or has an invalid key."""

    code = f"{EXCEPTION_CODE_PREFIX}-CONFIG"


class RepoError(ArchLensError):
    """A target-repository operation (clone, validate) failed."""

    code = f"{EXCEPTION_CODE_PREFIX}-REPO"


class GraphifyError(ArchLensError):
    """A Graphify pipeline stage or graph-parsing step failed."""

    code = f"{EXCEPTION_CODE_PREFIX}-GRAPHIFY"


class AnalysisError(ArchLensError):
    """Graph analysis could not produce a valid report."""

    code = f"{EXCEPTION_CODE_PREFIX}-ANALYSIS"


class RefactorError(ArchLensError):
    """A refactor plan could not be produced or applied."""

    code = f"{EXCEPTION_CODE_PREFIX}-REFACTOR"


class QAGateError(ArchLensError):
    """A quality gate (tests, lint, line cap) rejected a change."""

    code = f"{EXCEPTION_CODE_PREFIX}-QAGATE"


class GatekeeperError(ArchLensError):
    """An egress call through the gatekeeper failed."""

    code = f"{EXCEPTION_CODE_PREFIX}-GATEKEEPER"


class TokenBudgetError(ArchLensError):
    """An operation would exceed the configured token budget."""

    code = f"{EXCEPTION_CODE_PREFIX}-TOKENBUDGET"
