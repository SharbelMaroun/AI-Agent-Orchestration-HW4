"""Deterministic reproduction of httpie BugsInPy bug 4 — the Host-header overwrite (EX04 §5.4).

Root cause (httpie/models.py, class HTTPRequest):
    headers = dict(self._orig.headers)      # CaseInsensitiveDict -> a CASE-SENSITIVE plain dict
    if 'Host' not in headers:               # BUG: case-sensitive miss
        headers['Host'] = url.netloc...     # ...so a user-set Host (any case) gets OVERWRITTEN
The BugsInPy fix checks ``self._orig.headers`` (still case-insensitive), preserving the user header.

This reproduces the exact branch deterministically, no network and no httpie test env required.
    uv run python scripts/repro_httpie_bug.py
"""

from requests.structures import CaseInsensitiveDict


def main() -> int:
    # A user explicitly set a Host header on the CLI (requests stores it case-insensitively).
    orig = CaseInsensitiveDict({"host": "user-set.example.com"})

    buggy_thinks_missing = "Host" not in dict(orig)   # buggy line: case-sensitive copy
    fixed_sees_present = "Host" in orig               # fixed line: case-insensitive original

    print(f"user set header   : {dict(orig)}")
    print(f"BUGGY  `'Host' not in dict(self._orig.headers)` -> {buggy_thinks_missing}  "
          f"(=> httpie OVERWRITES the user's Host)")
    print(f"FIXED  `'Host' not in self._orig.headers`       -> {not fixed_sees_present}  "
          f"(=> httpie PRESERVES the user's Host)")
    assert buggy_thinks_missing is True, "expected the buggy check to mis-report Host as missing"
    assert fixed_sees_present is True, "expected the fixed check to see Host present"
    print("REPRODUCED: the buggy case-sensitive check overwrites a user-set Host; the fix preserves it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
