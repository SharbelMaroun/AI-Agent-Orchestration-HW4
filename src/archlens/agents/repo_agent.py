"""RepoAgent LangGraph node — clone + validate with a single fallback attempt (task 3.039)."""

import logging

from archlens.shared.constants import LOGGER_NAME
from archlens.shared.errors import RepoError

logger = logging.getLogger(f"{LOGGER_NAME}.repo_agent")


def _attempt(sdk, run_id: str, use_fallback: bool) -> dict:
    path = sdk.clone_target_repo(run_id, use_fallback=use_fallback)
    result = sdk.validate_repo(path, use_fallback=use_fallback)
    return {
        "target_repo": str(path),
        "validation": result.as_dict(),
        "fallback_used": use_fallback,
        "_passed": result.passed,
    }


def make_repo_agent(sdk):
    """Factory: bind the SDK and return the node callable (state in -> state delta out)."""

    def repo_agent(state: dict) -> dict:
        run_id = state["run_id"]
        try:
            outcome = _attempt(sdk, run_id, use_fallback=False)
            if outcome.pop("_passed"):
                return outcome
            logger.warning("primary repo failed validation for run %s; trying fallback", run_id)
        except RepoError as exc:
            logger.warning("primary clone failed for run %s (%s); trying fallback", run_id, exc)
        outcome = _attempt(sdk, run_id, use_fallback=True)
        outcome.pop("_passed")
        return outcome

    return repo_agent


def make_repo_node(sdk):
    """Orchestration node: clone+validate via the SDK and write a target_repo payload (10.014)."""

    def repo_node(state: dict) -> dict:
        run_id = state.get("run_id", "run")
        path = sdk.clone_target_repo(run_id)
        result = sdk.validate_repo(path)
        return {"target_repo": {"local_path": str(path), "validated": bool(result.passed)}}

    return repo_node
