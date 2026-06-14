"""OAT (one-at-a-time) sensitivity variant generation (task 15.004).

For each swept parameter, vary it across its configured range while holding every other parameter
at its baseline value. Values come exclusively from the SensitivityBlock; nothing is hardcoded.
"""

PARAMS = ("analysis_depth", "top_k_pages", "rate_limit_rpm", "similarity_threshold")


def oat_variants(block) -> dict[str, list[dict]]:
    """Return {param: [config dicts]} where each config varies only `param` from the baseline."""
    baseline = dict(block.baseline)
    variants: dict[str, list[dict]] = {}
    for param in PARAMS:
        rows = []
        for value in getattr(block, param):
            config = dict(baseline)
            config[param] = value
            rows.append(config)
        variants[param] = rows
    return variants
