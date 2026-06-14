"""Typed error taxonomy for the repo module — no bare excepts anywhere (task 3.042)."""


class RepoError(Exception):
    """Base class for every repo-module failure."""


class CloneNetworkError(RepoError):
    """Transient network failure during clone (DNS, connection, unknown remote errors)."""


class CloneAuthError(RepoError):
    """Authentication/authorization failure — permanent, never retried."""


class CloneTimeoutError(RepoError):
    """Clone exceeded the configured timeout_s — treated as transient."""


class DiskFullError(RepoError):
    """No space left on device — permanent, never retried."""


class RetryExhaustedError(RepoError):
    """All configured retry attempts failed."""


class SandboxViolationError(RepoError):
    """A path escaped the sandbox root or a run id was malformed."""


class RepoValidationError(RepoError):
    """The cloned repository failed validation checks."""


class GitCommandError(RepoError):
    """A local git command (branch/revert/inspect) returned non-zero or timed out."""
