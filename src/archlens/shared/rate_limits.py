"""rate_limits.json nested schema (PRD_api_gatekeeper §3.1) and loader."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from archlens.shared.config import _read_json, check_config_version
from archlens.shared.constants import RATE_LIMITS_FILE


class ServiceLimits(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requests_per_minute: int
    requests_per_hour: int
    concurrent_max: int
    retry_after_seconds: int
    max_retries: int


class ServicesBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default: ServiceLimits


class RateLimitsBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")

    services: ServicesBlock


class QueueConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_depth: int
    backpressure_warn_ratio: float


class RateLimitsConfig(BaseModel):
    """Typed view of config/rate_limits.json; unknown keys are rejected."""

    model_config = ConfigDict(extra="forbid")

    version: str
    rate_limits: RateLimitsBlock
    queue: QueueConfig


def load_rate_limits(path: str | Path = RATE_LIMITS_FILE) -> RateLimitsConfig:
    source = Path(path)
    cfg = RateLimitsConfig.model_validate(_read_json(source))
    check_config_version(cfg.version, source)
    return cfg
