"""SDK research / sensitivity methods (Phase 15) — a mixin to honour the 150-line file cap."""

from ..metrics.sensitivity_grid import oat_variants
from ..metrics.sensitivity_runner import run_param_sweep


class ResearchMixin:
    """Phase 15 OAT sensitivity entry points on the SDK facade."""

    def oat_variants(self) -> dict[str, list[dict]]:
        """Generate the OAT sensitivity variants from config/setup.json."""
        return oat_variants(self._config().sensitivity)

    def run_sensitivity(self, param: str, runner, out_dir="results/sensitivity"):
        """Run one pipeline per OAT variant of `param` via the injected runner; persist the JSON."""
        return run_param_sweep(param, self.oat_variants()[param], runner, out_dir)
