# Bug Report - httpie (soarsmu/BugsInPy bug 4: Host-header overwrite)

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04)

The **primary** investigated bug, on the class-bearing PDF-listed BugsInPy target `httpie`
(`https://github.com/httpie/cli` at buggy commit `8c892edd`). It is a real, recorded BugsInPy bug
with an official fix and a regression test.

## 1. Symptom

When a user explicitly sets a `Host` header (e.g. `http example.com Host:custom.example.com`), httpie
**overwrites it** with the host derived from the URL instead of honouring the user's value. BugsInPy
records the failing test `tests/test_regressions.py::test_Host_header_overwrite`.

## 2. Graph-first localization

The dependency graph and the OOP class diagram (`deliverables/CLASS_SCHEMA.md`) route the
request-building concern to **`httpie/models.py`**, class **`HTTPRequest(HTTPMessage)`** — the header
assembly happens in its `headers` property. The graph reaches the class before any line-by-line source
reading (the live token study localizes the request-header concern to `models.py` in **one** cycle vs
a 13-module naive scan).

## 3. Root cause

In `HTTPRequest.headers` (httpie/models.py):

```python
headers = dict(self._orig.headers)     # self._orig.headers is a requests CaseInsensitiveDict
if 'Host' not in headers:              # BUG: dict() made a CASE-SENSITIVE copy
    headers['Host'] = url.netloc.split('@')[-1]
```

`requests` stores headers in a **case-insensitive** `CaseInsensitiveDict`. `dict(self._orig.headers)`
collapses it into a **case-sensitive** plain dict, so a user header set as `host` (or any non-`Host`
casing) is **missed** by `'Host' not in headers`, and httpie overwrites it.

## 4. Fix (the official BugsInPy patch)

```diff
-        if 'Host' not in headers:
+        if 'Host' not in self._orig.headers:
```

Checking the original `CaseInsensitiveDict` restores case-insensitive detection, so any user-set Host
(any casing) is preserved.

## 5. Verification

- **Deterministic reproduction (no network, no httpie test env):**
  `uv run python scripts/repro_httpie_bug.py` →
  `BUGGY 'Host' not in dict(self._orig.headers) -> True (OVERWRITES)`,
  `FIXED 'Host' not in self._orig.headers -> False (PRESERVES)`. Exit 0.
- **Official regression test:** from a BugsInPy checkout,
  `pytest tests/test_regressions.py::test_Host_header_overwrite` fails on the buggy commit and passes
  after the one-line fix.

## 6. Before / after (knowledge level)

Before: the failure looked like a header bug "somewhere in request handling". After graph navigation:
the suspect narrows to one class method (`HTTPRequest.headers`) and the root cause is a **type
conversion that drops case-insensitivity** — a one-line, behaviour-preserving fix. The OOP class
diagram makes the `HTTPMessage -> HTTPRequest` location explicit.
