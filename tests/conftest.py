"""Shared fixtures: temp config copies, environment stubs, git fixture factory."""

import json
import shutil
import socket
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

collect_ignore_glob = ["fixtures/*"]
pytest_plugins = ["phase13.fixtures.plugins"]


@pytest.fixture()
def config_copy(tmp_path: Path) -> Path:
    """Mutable copy of the real config/ directory."""
    dest = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, dest)
    return dest


@pytest.fixture()
def setup_json(config_copy: Path) -> Path:
    return config_copy / "setup.json"


@pytest.fixture()
def rate_limits_json(config_copy: Path) -> Path:
    return config_copy / "rate_limits.json"


@pytest.fixture()
def env_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dummy secrets so no test ever needs a real credential."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-dummy")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp-dummy")


@pytest.fixture()
def git_repo_factory(tmp_path: Path):
    """Materialize a fixture directory as a real local git repository (task 3.020)."""

    def _make(source: Path, name: str = "repo") -> Path:
        dest = tmp_path / name
        shutil.copytree(source, dest)
        ident = ["-c", "user.email=fixtures@archlens.local", "-c", "user.name=Fixtures"]
        for args in (["init", "-q"], ["add", "-A"], [*ident, "commit", "-q", "-m", "fixture"]):
            subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True)
        return dest

    return _make


@pytest.fixture()
def oversize_repo(tmp_path: Path) -> Path:
    """mini_repo clone with 60 extra generated modules — exceeds max_file_count (task 3.021)."""
    dest = tmp_path / "oversize"
    shutil.copytree(FIXTURES / "mini_repo", dest)
    for i in range(60):
        (dest / f"gen_{i}.py").write_text(f"VALUE_{i} = {i}\n", encoding="utf-8")
    return dest


class _MockGatekeeper:
    """Deterministic gatekeeper mock: canned responses, no network (task 10.047)."""

    def __init__(self):
        self.calls = []

    def call_llm(self, prompt, **kwargs):
        self.calls.append(("llm", prompt))
        return "canned response"

    def run_subprocess(self, args, **kwargs):
        self.calls.append(("subprocess", args))
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def http_get(self, url, **kwargs):
        self.calls.append(("http", url))
        return SimpleNamespace(status=200, text="")

    def rate_limit_status(self):
        return {"queue_depth": 0}


class _MockSDK:
    """Canned SDK for orchestration integration tests (no network, deterministic)."""

    def clone_target_repo(self, run_id, use_fallback=False):
        return Path("/clone")

    def validate_repo(self, path, use_fallback=False):
        return SimpleNamespace(passed=True)

    def run_graphify_pipeline(self, repo):
        return SimpleNamespace(graph_json="g.json", node_count=10, edge_count=8, report_md="R.md")

    def load_analysis_graph(self, source):
        return "G"

    def density_communities(self, graph):
        return [{"a"}, {"b"}]

    def node_centrality(self, graph):
        return [SimpleNamespace(node_id="hub", degree_total=4, betweenness=0.5)]

    def classify_nodes(self, graph):
        return [SimpleNamespace(node_id="gate", verdict="BOTTLENECK", source_file="gate.py")]

    def triage_edges(self, graph):
        return {"EXTRACTED": [1], "INFERRED": [], "AMBIGUOUS": []}

    def single_points_of_failure(self, graph):
        return [SimpleNamespace(node_id="ss", citations=[SimpleNamespace(source_file="ss.py")])]

    def run_quality_gates(self, repo_path=None):
        return SimpleNamespace(tests_green=True, coverage_pct=97.0, ruff_violations=0)

    def token_usage(self):
        return {"baseline": 100, "assisted": 30, "rows": [{"model": "x", "in": 10}]}

    def ask_llm(self, prompt, *, agent="orchestrator", max_tokens=512):
        return "canned llm reply"

    def apply_fix(self, finding, repo_path, graph_json=None):
        return True


@pytest.fixture()
def mock_gatekeeper():
    return _MockGatekeeper()


@pytest.fixture()
def mock_sdk():
    return _MockSDK()


@pytest.fixture()
def blocked_sockets(monkeypatch):
    """Block all outbound socket connections so orchestration tests make zero network calls."""
    def _blocked(*args, **kwargs):
        raise RuntimeError("outbound socket blocked in mock mode")

    monkeypatch.setattr(socket.socket, "connect", _blocked)
    return True


@pytest.fixture()
def fake_clock():
    """A deterministic FakeClock for gatekeeper window/retry/drain tests (task 9.007)."""
    from archlens.gatekeeper.clock import FakeClock

    return FakeClock()


@pytest.fixture()
def rate_config_factory(tmp_path):
    """Write a temp rate_limits.json with overridable version/limits; return its path."""
    def _make(version="1.00", **overrides):
        default = {"requests_per_minute": 30, "requests_per_hour": 500, "concurrent_max": 5,
                   "retry_after_seconds": 30, "max_retries": 3}
        default.update({k: v for k, v in overrides.items() if k in default})
        data = {"version": version, "rate_limits": {"services": {"default": default}},
                "queue": {"max_depth": 100, "backpressure_warn_ratio": 0.8}}
        path = tmp_path / "rate_limits.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    return _make


@pytest.fixture()
def synthetic_ledger():
    """Factory for a synthetic Phase 12 TokenLedger with configurable entries (task 12.003)."""
    from archlens.metrics.ledger import TokenLedger
    from archlens.metrics.ledger_model import TokenLedgerEntry

    def _make(n=10, agents=("RepoAgent", "GraphAgent", "AnalystAgent"),
              models=("claude-opus-4-8", "claude-haiku-4-5"),
              protocols=("baseline", "assisted")):
        ledger = TokenLedger()
        for i in range(n):
            ledger.append(TokenLedgerEntry(
                agent=agents[i % len(agents)], model=models[i % len(models)],
                protocol=protocols[i % len(protocols)],
                input_tokens=100 + i * 10, output_tokens=10 + i,
                question_id=f"Q{i % 10 + 1:02d}"))
        return ledger

    return _make


@pytest.fixture()
def mock_anthropic():
    """Factory for a deterministic Anthropic client double with canned token usage."""
    def _make(text="canned response", in_tokens=10, out_tokens=5):
        def create(model, messages, **kwargs):
            usage = SimpleNamespace(input_tokens=in_tokens, output_tokens=out_tokens)
            return SimpleNamespace(text=text, model=model, usage=usage)

        return SimpleNamespace(create=create)

    return _make
