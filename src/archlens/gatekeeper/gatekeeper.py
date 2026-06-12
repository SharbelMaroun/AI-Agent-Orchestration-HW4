"""Gatekeeper — the sole path for every external API call.

No other module may touch the network; full queue/retry behavior arrives in Phase 9.
"""

from archlens.shared.rate_limits import RateLimitsConfig, load_rate_limits


class Gatekeeper:
    """Loads rate-limit policy at construction; all external calls route through here."""

    def __init__(self, config: RateLimitsConfig | None = None) -> None:
        self._config = config if config is not None else load_rate_limits()

    @property
    def limits(self) -> RateLimitsConfig:
        return self._config
