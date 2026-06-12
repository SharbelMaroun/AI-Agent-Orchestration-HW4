"""TDD import-contract tests for the package skeleton, SDK and Gatekeeper (task 1.031)."""

import importlib

SUBPACKAGES = ["sdk", "gatekeeper", "agents", "graphops", "vault", "metrics", "shared"]


def test_all_subpackages_importable_with_dunder_all():
    for name in SUBPACKAGES:
        module = importlib.import_module(f"archlens.{name}")
        assert hasattr(module, "__all__"), f"archlens.{name} is missing __all__"


def test_sdk_single_entry_point():
    from archlens.sdk.sdk import ArchLensSDK

    assert ArchLensSDK().version() == "1.00"


def test_gatekeeper_loads_rate_limits():
    from archlens.gatekeeper.gatekeeper import Gatekeeper

    gk = Gatekeeper()
    assert gk.limits.rate_limits.services.default.concurrent_max == 5
