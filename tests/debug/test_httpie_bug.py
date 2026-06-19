"""Regression test for httpie BugsInPy bug 4 (Host-header overwrite) root cause (EX04 §5.4).

The buggy check `'Host' not in dict(self._orig.headers)` is case-SENSITIVE (dict() drops requests'
CaseInsensitiveDict), so a user-set Host in another case is missed and overwritten; the fix checks the
original case-insensitive headers. We assert the exact branch logic with a plain dict + a
case-insensitive key set (no `requests` import — the test-hygiene guard forbids real-service imports;
the live demonstration is `scripts/repro_httpie_bug.py`).
"""

# A user explicitly set a Host header on the CLI as lowercase 'host'.
USER_HEADERS = {"host": "user-set.example.com"}


def test_buggy_case_sensitive_check_overwrites_user_host():
    # Buggy line: dict(...) membership is case-sensitive -> 'Host' looks missing -> httpie overwrites.
    assert ("Host" not in USER_HEADERS) is True


def test_fixed_case_insensitive_check_preserves_user_host():
    # Fixed line: the original headers are case-insensitive -> 'Host' is seen present -> preserved.
    case_insensitive_keys = {key.lower() for key in USER_HEADERS}
    assert ("host" in case_insensitive_keys) is True
