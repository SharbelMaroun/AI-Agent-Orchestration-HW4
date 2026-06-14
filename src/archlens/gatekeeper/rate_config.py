"""Gatekeeper rate-limit config loader — reuses the shared §3.1 loader (task 9.009).

No numeric limit literals live here: all 30/500/5/3 values come from config/rate_limits.json,
version-validated at boot by the shared loader.
"""

from ..shared.constants import RATE_LIMITS_FILE
from ..shared.rate_limits import RateLimitsConfig, ServiceLimits, load_rate_limits

__all__ = ["RateLimitConfig", "ServiceLimits", "load_rate_config", "service_limits"]

RateLimitConfig = RateLimitsConfig


def load_rate_config(path=RATE_LIMITS_FILE) -> RateLimitsConfig:
    """Load and boot-version-validate config/rate_limits.json."""
    return load_rate_limits(path)


def service_limits(config: RateLimitsConfig) -> ServiceLimits:
    """Return the default service's limit block (rpm, rph, concurrent_max, retry, max_retries)."""
    return config.rate_limits.services.default
