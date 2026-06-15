"""Git clone wrapper — the ONLY module allowed to spawn git (gatekeeper egress).

All retry parameters come from config/rate_limits.json; nothing is hardcoded here.
"""

import subprocess
import time
from pathlib import Path

from ..shared.config import RepoBlock
from ..shared.constants import GIT_BOT_EMAIL, GIT_BOT_NAME
from ..shared.errors import (
    CloneAuthError,
    CloneNetworkError,
    CloneTimeoutError,
    DiskFullError,
    GitCommandError,
    RepoError,
    RetryExhaustedError,
)
from ..shared.rate_limits import ServiceLimits

_AUTH_MARKERS = ("authentication", "permission denied", "403", "could not read username")
_DISK_MARKERS = ("no space left", "disk full")
_GIT_IDENT = ["-c", f"user.email={GIT_BOT_EMAIL}", "-c", f"user.name={GIT_BOT_NAME}"]


def run_local_git(args: list[str], cwd: Path, timeout_s: int) -> str:
    """Run a local (non-network) git command in cwd with a bot identity; return stdout."""
    cmd = ["git", "-C", str(cwd), *_GIT_IDENT, *args]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        raise GitCommandError(f"git timed out after {timeout_s}s: {args[:2]}") from exc
    if proc.returncode != 0:
        raise GitCommandError(f"git {args[:2]} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def classify_git_failure(stderr: str) -> RepoError:
    lowered = stderr.lower()
    if any(marker in lowered for marker in _AUTH_MARKERS):
        return CloneAuthError(f"git authentication failure: {stderr.strip()}")
    if any(marker in lowered for marker in _DISK_MARKERS):
        return DiskFullError(f"git disk failure: {stderr.strip()}")
    return CloneNetworkError(f"git network/unknown failure: {stderr.strip()}")


def _run(cmd: list[str], timeout_s: int) -> None:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        raise CloneTimeoutError(f"git timed out after {timeout_s}s: {' '.join(cmd[:2])}") from exc
    if proc.returncode != 0:
        raise classify_git_failure(proc.stderr)


def run_git_clone(repo: RepoBlock, dest: Path) -> None:
    clone_cmd = ["git", "clone", "--depth", str(repo.clone_depth)]
    if repo.branch:  # empty branch -> clone the remote's default branch (for arbitrary user URLs)
        clone_cmd += ["--branch", repo.branch]
    clone_cmd += [repo.url, str(dest)]
    _run(clone_cmd, repo.timeout_s)
    if repo.pinned_commit not in ("", "HEAD"):
        _run(["git", "-C", str(dest), "checkout", repo.pinned_commit], repo.timeout_s)


def clone_with_retry(
    repo: RepoBlock,
    dest: Path,
    limits: ServiceLimits,
    runner=run_git_clone,
    sleeper=time.sleep,
) -> Path:
    """Retry transient failures per config; permanent failures raise immediately."""
    last_error: RepoError | None = None
    for attempt in range(1, limits.max_retries + 1):
        try:
            runner(repo, dest)
            return dest
        except (CloneNetworkError, CloneTimeoutError) as exc:
            last_error = exc
            if attempt < limits.max_retries:
                sleeper(limits.retry_after_seconds)
    raise RetryExhaustedError(f"clone failed after {limits.max_retries} attempts") from last_error
