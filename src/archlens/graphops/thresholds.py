"""Analysis thresholds sourced from config/setup.json for cfg.get access (6.034, 6.038)."""

from ..shared.config import load_setup


def thresholds() -> dict:
    """Return the analysis-threshold block as a plain dict, read from config/setup.json."""
    return load_setup().analysis.model_dump()
