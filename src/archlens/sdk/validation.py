"""Target-repo validation checks and the aggregated validate_repo entry (tasks 3.028-3.036)."""

from dataclasses import dataclass, field
from pathlib import Path

from archlens.shared.config import ValidationBlock

LICENSE_MARKERS = ("MIT", "Apache", "BSD", "GPL", "MPL", "ISC", "Unlicense")
LICENSE_FILENAMES = ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING")
PYTEST_CONFIG_FILES = ("pytest.ini", "tox.ini", "setup.cfg")


@dataclass
class CheckResult:
    name: str
    passed: bool
    reason: str


@dataclass
class ValidationResult:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def failing(self) -> list[str]:
        return [c.name for c in self.checks if not c.passed]

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "checks": [{"name": c.name, "passed": c.passed, "reason": c.reason} for c in self.checks],
        }


def _files(repo_dir: Path) -> list[Path]:
    return [p for p in Path(repo_dir).rglob("*") if p.is_file() and ".git" not in p.parts]


def check_is_python(repo_dir: Path, min_share: float) -> CheckResult:
    files = _files(repo_dir)
    if not files:
        return CheckResult("is_python", False, "empty repository: no files found")
    share = sum(1 for f in files if f.suffix == ".py") / len(files)
    has_project = any((Path(repo_dir) / n).is_file() for n in ("pyproject.toml", "setup.py"))
    if share >= min_share and has_project:
        return CheckResult("is_python", True, f"python share {share:.2f} >= {min_share}, project config present")
    return CheckResult(
        "is_python", False, f"python share {share:.2f} (min {min_share}), project config present: {has_project}"
    )


def check_size_bounds(repo_dir: Path, min_files: int, max_files: int, max_size_mb: int) -> CheckResult:
    files = _files(repo_dir)
    size_mb = sum(f.stat().st_size for f in files) / (1024 * 1024)
    if min_files <= len(files) <= max_files and size_mb <= max_size_mb:
        return CheckResult("size_bounds", True, f"{len(files)} files, {size_mb:.1f} MB within bounds")
    return CheckResult(
        "size_bounds",
        False,
        f"{len(files)} files (bounds {min_files}-{max_files}), {size_mb:.1f} MB (max {max_size_mb})",
    )


def check_has_tests(repo_dir: Path) -> CheckResult:
    tests_dir = Path(repo_dir) / "tests"
    if tests_dir.is_dir() and any(tests_dir.iterdir()):
        return CheckResult("has_tests", True, "tests/ directory present")
    for name in PYTEST_CONFIG_FILES:
        if (Path(repo_dir) / name).is_file():
            return CheckResult("has_tests", True, f"pytest configuration found in {name}")
    pyproject = Path(repo_dir) / "pyproject.toml"
    if pyproject.is_file() and "[tool.pytest" in pyproject.read_text(encoding="utf-8"):
        return CheckResult("has_tests", True, "pytest configuration found in pyproject.toml")
    return CheckResult("has_tests", False, "no tests/ directory and no pytest configuration detected")


def check_license(repo_dir: Path) -> CheckResult:
    for name in LICENSE_FILENAMES:
        candidate = Path(repo_dir) / name
        if candidate.is_file():
            head = candidate.read_text(encoding="utf-8", errors="replace")[:400]
            for marker in LICENSE_MARKERS:
                if marker in head:
                    return CheckResult("license", True, f"recognized license marker: {marker}")
            return CheckResult("license", False, f"unrecognized license text in {name}")
    return CheckResult("license", False, "no license file found")


def validate_repo(repo_dir: Path, vcfg: ValidationBlock, max_size_mb: int) -> ValidationResult:
    return ValidationResult(
        checks=[
            check_is_python(repo_dir, vcfg.python_min_share),
            check_size_bounds(repo_dir, vcfg.min_file_count, vcfg.max_file_count, max_size_mb),
            check_has_tests(repo_dir),
            check_license(repo_dir),
        ]
    )
