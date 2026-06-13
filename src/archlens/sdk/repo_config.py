"""Target-repo config accessor — the SDK's only way to pick a repository block."""

from archlens.shared.config import RepoBlock, SetupConfig


def select_repo(cfg: SetupConfig, use_fallback: bool = False) -> RepoBlock:
    """Return the primary target block, or the fallback block when requested."""
    return cfg.fallback_repo if use_fallback else cfg.target_repo
