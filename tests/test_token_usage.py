"""sdk.token_usage reports the real per-call tokens the gatekeeper recorded (no longer a stub)."""

from archlens.sdk.sdk import ArchLensSDK


def test_token_usage_is_zero_before_any_call():
    assert ArchLensSDK().token_usage()["total"] == 0


def test_token_usage_reflects_real_gatekeeper_usage_after_a_call():
    # mock mode (autouse) records deterministic input/output tokens per call.
    sdk = ArchLensSDK()
    sdk.ask_llm("interpret this graph")
    usage = sdk.token_usage()
    assert usage["total"] > 0
    assert usage["total"] == usage["input"] + usage["output"]
    assert usage["assisted"] == usage["total"]   # kept for measure_tokens compatibility
    assert usage["rows"] and usage["rows"][0]["agent"] == "orchestrator"
