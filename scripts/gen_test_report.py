"""Generate reports/test_report.md from the pytest JUnit XML (task 13.050).

Lists every test with its name, expected result (from the test's 'Expected:' docstring line when
available, else '-'), and PASS/FAIL status. Run: uv run python scripts/gen_test_report.py
"""

import ast
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JUNIT = ROOT / "reports" / "junit.xml"
REPORT = ROOT / "reports" / "test_report.md"


def _expected_lines() -> dict[str, str]:
    """Map test function name -> its 'Expected:' docstring line across the tests/ tree."""
    expected: dict[str, str] = {}
    for py_file in (ROOT / "tests").rglob("test_*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                doc = ast.get_docstring(node) or ""
                for line in doc.splitlines():
                    if line.strip().startswith("Expected:"):
                        expected[node.name] = line.strip()[len("Expected:"):].strip()
    return expected


def _status(case: ET.Element) -> str:
    if case.find("failure") is not None or case.find("error") is not None:
        return "FAIL"
    if case.find("skipped") is not None:
        return "SKIP"
    return "PASS"


def main() -> int:
    if not JUNIT.is_file():
        raise SystemExit(f"missing JUnit XML: {JUNIT} (run `uv run pytest` first)")
    expected = _expected_lines()
    rows = ["# Test Report", "",
            "Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04)", "",
            "| Test | Expected | Status |", "|---|---|---|"]
    cases = ET.parse(JUNIT).getroot().iter("testcase")
    passed = failed = 0
    for case in cases:
        name = case.get("name", "")
        status = _status(case)
        passed += status == "PASS"
        failed += status == "FAIL"
        rows.append(f"| {name} | {expected.get(name, '-')} | {status} |")
    rows.insert(4, f"Totals: {passed} passed, {failed} failed.\n")
    REPORT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote {REPORT} ({passed} passed, {failed} failed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
