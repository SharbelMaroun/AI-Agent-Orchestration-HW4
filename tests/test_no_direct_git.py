"""Guard test: no module outside gatekeeper/ may invoke subprocess or git (task 3.027)."""

from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"


def test_only_gatekeeper_uses_subprocess():
    offenders = []
    for py_file in SRC.rglob("*.py"):
        if "gatekeeper" in py_file.parts:
            continue
        text = py_file.read_text(encoding="utf-8")
        # Flag actual invocation (import / attribute use), not an interface method name.
        invokes_subprocess = "import subprocess" in text or "subprocess." in text
        spawns_git = '"git"' in text or "'git'" in text
        if invokes_subprocess or spawns_git:
            offenders.append(str(py_file))
    assert offenders == [], f"direct git/subprocess usage outside gatekeeper: {offenders}"
