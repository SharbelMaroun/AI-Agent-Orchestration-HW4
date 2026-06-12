"""ArchLensSDK — the single entry point for all business logic.

GUI/CLI layers hold zero logic; they call this facade exclusively.
"""

from archlens.shared.version import get_version


class ArchLensSDK:
    """Facade over all ArchLens capabilities (grows phase by phase)."""

    def version(self) -> str:
        return get_version()
