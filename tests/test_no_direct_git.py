"""Guard test: no module outside gatekeeper/ may invoke subprocess or git (task 3.027)."""

from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"


def test_only_gatekeeper_uses_subprocess():
    offenders = []
    for py_file in SRC.rglob("*.py"):
        if "gatekeeper" in py_file.parts:
            continue
        text = py_file.read_text(encoding="utf-8")
        if "subprocess" in text or '"git"' in text or "'git'" in text:
            offenders.append(str(py_file))
    assert offenders == [], f"direct git/subprocess usage outside gatekeeper: {offenders}"
