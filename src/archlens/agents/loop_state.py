"""LoopState model — per-run improvement-loop bookkeeping (task 11.006).

Tracks the iteration counter, the applied-fix history, the feature branches created, and
the per-iteration metrics snapshots that later feed the graph-diff stop conditions.
"""

from pydantic import BaseModel, ConfigDict, Field


class AppliedFix(BaseModel):
    """One fix applied in an iteration, with its branch and accept/reject outcome."""

    model_config = ConfigDict(extra="forbid")

    fix_id: str
    priority: str
    branch: str
    accepted: bool


class LoopState(BaseModel):
    """Mutable record of loop progress: counter, fix history, branches, metric snapshots."""

    model_config = ConfigDict(extra="forbid")

    iteration: int = 0
    applied_fixes: list[AppliedFix] = Field(default_factory=list)
    branches: list[str] = Field(default_factory=list)
    metrics_snapshots: list[dict] = Field(default_factory=list)

    def record_fix(self, fix: AppliedFix) -> None:
        """Append a fix to history and track its feature branch (deduplicated)."""
        self.applied_fixes.append(fix)
        if fix.branch not in self.branches:
            self.branches.append(fix.branch)

    def snapshot(self, metrics: dict) -> None:
        """Store a copy of a metrics snapshot for later diffing."""
        self.metrics_snapshots.append(dict(metrics))

    def at_cap(self, max_iterations: int) -> bool:
        """True once the iteration counter has reached the hard cap."""
        return self.iteration >= max_iterations
