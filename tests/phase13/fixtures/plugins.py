"""Phase 13 shared fixtures, registered via tests/conftest.py ``pytest_plugins``.

Lives under a ``fixtures`` path component so it is exempt from the 150-line cap, but under the
``phase13`` top-level package so it never shadows tests/graphops/fixtures.py. Provides the larger
Phase 13 testing fixtures (repo trees, graph samples, mocks, vault layout, autouse no-network).
"""

import datetime
import hashlib
import json
import socket
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPORTS = Path(__file__).resolve().parents[3] / "reports"


def pytest_sessionfinish(session, exitstatus):
    """Write a timestamped run log into reports/ after every session (task 13.048)."""
    _REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    (_REPORTS / f"pytest_{stamp}.log").write_text(
        f"pytest session finished\nexitstatus={exitstatus}\n"
        f"collected={session.testscollected}\n", encoding="utf-8")


@pytest.fixture()
def fixture_repo(tmp_path):
    """Mini repo: 3 packages, an a<->b import cycle, and a >150-line module (task 13.007)."""
    root = tmp_path / "fixture_repo"
    for pkg in ("pkg_a", "pkg_b", "pkg_c"):
        (root / pkg).mkdir(parents=True)
        (root / pkg / "__init__.py").write_text("", encoding="utf-8")
    (root / "pkg_a" / "mod.py").write_text(
        "from pkg_b.mod import b_fn\n\n\ndef a_fn():\n    return b_fn()\n", encoding="utf-8")
    (root / "pkg_b" / "mod.py").write_text(
        "from pkg_a.mod import a_fn  # import cycle\n\n\ndef b_fn():\n    return 1\n", encoding="utf-8")
    big = "\n".join(f"VALUE_{i} = {i}" for i in range(170))
    (root / "pkg_c" / "big.py").write_text(big + "\n", encoding="utf-8")
    return root


@pytest.fixture()
def fixture_graph_json(tmp_path):
    """Schema-valid Graphify graph.json with known nodes, edges, communities (task 13.008)."""
    data = {
        "directed": True, "multigraph": False, "graph": {},
        "nodes": [
            {"id": "a", "label": "a.py", "file_type": "code", "source_file": "a.py", "community": 0},
            {"id": "b", "label": "b.py", "file_type": "code", "source_file": "b.py", "community": 0},
            {"id": "c", "label": "c.py", "file_type": "code", "source_file": "c.py", "community": 1},
        ],
        "links": [
            {"source": "a", "target": "b", "relation": "imports", "type": "EXTRACTED",
             "confidence": 0.95, "source_file": "a.py"},
            {"source": "b", "target": "c", "relation": "calls", "type": "INFERRED",
             "confidence": 0.70, "source_file": "b.py"},
        ],
        "hyperedges": [],
    }
    path = tmp_path / "graph.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return SimpleNamespace(path=path, data=data)


@pytest.fixture()
def mock_llm_responses():
    """Canned completions keyed by prompt hash; identical prompts return identical payloads (13.010)."""
    store: dict[str, SimpleNamespace] = {}

    def _respond(prompt: str) -> SimpleNamespace:
        key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        if key not in store:
            store[key] = SimpleNamespace(
                text=f"canned:{key[:8]}",
                usage=SimpleNamespace(input_tokens=len(prompt) // 4, output_tokens=5))
        return store[key]

    return _respond


@pytest.fixture()
def mock_git(tmp_path):
    """Offline clone/checkout/status onto tmp_path repos; no remote contacted (task 13.011)."""
    calls: list = []

    def _clone(url, dest, *args, **kwargs):
        Path(dest).mkdir(parents=True, exist_ok=True)
        (Path(dest) / "README.md").write_text("cloned\n", encoding="utf-8")
        calls.append(("clone", url, str(dest)))
        return Path(dest)

    def _op(name):
        def _run(*args, **kwargs):
            calls.append((name, args, kwargs))
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return _run

    return SimpleNamespace(clone=_clone, checkout=_op("checkout"),
                           status=_op("status"), calls=calls)


@pytest.fixture()
def mock_graphify(tmp_path):
    """Canned detect->extract->build->cluster->export artifacts in tmp_path (task 13.012)."""
    out = tmp_path / "graphify-out"
    out.mkdir(parents=True)
    (out / "graph.json").write_text(json.dumps({"nodes": [], "links": []}), encoding="utf-8")
    (out / "graph.html").write_text("<html></html>", encoding="utf-8")
    (out / "REPORT.md").write_text("# Graph Report\n", encoding="utf-8")
    return out


@pytest.fixture()
def fake_vault_fs(tmp_path):
    """tmp_path-backed Obsidian vault: hot.md, index.md, wiki/, log.md (task 13.013)."""
    root = tmp_path / "vault"
    (root / "wiki").mkdir(parents=True)
    (root / "hot.md").write_text("# Hot Nodes\n", encoding="utf-8")
    (root / "index.md").write_text("# Index\n", encoding="utf-8")
    (root / "log.md").write_text("# Log\n", encoding="utf-8")
    return root


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Block outbound (non-loopback) socket connects during every test (task 13.014).

    Also pins the gatekeeper to mock LLM mode so an ambient credential never makes a live API call.
    """
    monkeypatch.setenv("ARCHLENS_LLM_MODE", "mock")
    real_connect = socket.socket.connect
    loopback = {"127.0.0.1", "::1", "localhost", ""}

    def _guard(self, address, *args, **kwargs):
        host = address[0] if isinstance(address, tuple) else address
        if host not in loopback:
            raise RuntimeError(f"network blocked in tests: {host!r}")
        return real_connect(self, address, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", _guard)
