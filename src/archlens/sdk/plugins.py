"""Agent plugin registry — the AgentPlugin extension point (task 8.031)."""

import threading


class PluginRegistry:
    """Thread-safe registry of agent plugins with duplicate rejection and allowlist filtering."""

    def __init__(self, allowlist: list[str] | None = None) -> None:
        self._plugins: dict[str, object] = {}
        self._allowlist = allowlist
        self._lock = threading.Lock()

    def register_agent_plugin(self, name: str, plugin: object) -> bool:
        """Register a plugin; reject duplicates; skip names not on the configured allowlist."""
        with self._lock:
            if name in self._plugins:
                raise ValueError(f"duplicate plugin name: {name}")
            if self._allowlist is not None and name not in self._allowlist:
                return False
            self._plugins[name] = plugin
            return True

    def get(self, name: str) -> object | None:
        return self._plugins.get(name)

    def names(self) -> list[str]:
        return sorted(self._plugins)
