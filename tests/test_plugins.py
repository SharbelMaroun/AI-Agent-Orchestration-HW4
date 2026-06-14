"""TDD tests for the agent plugin registry (tasks 8.030-8.031)."""

import pytest

from archlens.sdk.plugins import PluginRegistry


def test_register_and_lookup():
    registry = PluginRegistry()
    sentinel = object()
    assert registry.register_agent_plugin("p1", sentinel) is True
    assert registry.get("p1") is sentinel


def test_duplicate_name_is_rejected():
    registry = PluginRegistry()
    registry.register_agent_plugin("p1", object())
    with pytest.raises(ValueError):
        registry.register_agent_plugin("p1", object())


def test_allowlist_filters_unlisted_plugins():
    registry = PluginRegistry(allowlist=["allowed"])
    assert registry.register_agent_plugin("blocked", object()) is False
    assert registry.get("blocked") is None
    assert registry.register_agent_plugin("allowed", object()) is True
    assert registry.get("allowed") is not None


def test_names_lists_registered_plugins_sorted():
    registry = PluginRegistry()
    registry.register_agent_plugin("b", object())
    registry.register_agent_plugin("a", object())
    assert registry.names() == ["a", "b"]
