"""TDD tests for the sdk config block and the MAX_LOOP_ITERATIONS constant (task 8.005)."""

from archlens.shared.config import load_setup
from archlens.shared.constants import MAX_LOOP_ITERATIONS


def test_sdk_block_keys_are_readable():
    sdk = load_setup().sdk.model_dump()
    assert sdk.get("default_analysis_depth") == "structural"
    assert sdk.get("plugin_allowlist") == []
    assert sdk.get("vault_output_root") == "runs/vault"


def test_max_loop_iterations_is_five():
    assert MAX_LOOP_ITERATIONS == 5
