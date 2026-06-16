"""Repository-level contract validation.

These checks cover invariants that span documentation, source course layout,
publish configuration, and git tracking. They intentionally avoid rendering
outputs; use ``validate_outputs.py`` for artifact existence checks.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.shared.course_config import active_course_names, archived_course_paths


DOC_REQUIRED_ROOTS = (Path("course_development"), Path("software/src"))
PRODUCTION_CODE_PATHS = (Path("publish.py"), Path("software/scripts"), Path("software/src"))
DOC_EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "htmlcov",
    "output",
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
LAB_NUMBER_PATTERN = re.compile(r"lab-(\d+)")
MODULE_NUMBER_PATTERN = re.compile(r"module-(\d+)")
SLIDE_NUMBER_PATTERN = re.compile(r"module-(\d+)-slides-.*\.pdf$")
SUPPLEMENTAL_LAB_MARKERS = ("followup", "follow-up")
ACTIVE_BIOL1_FORBIDDEN_TEXT = (
    "Spring 2026",
    "Del Norte",
    "Exam 04",
    "Lab 18",
    "lab-18",
    "module-16",
    "Module 16",
    "Introduction to Biology",
    "BIOL-1: Biology 1",
    "Pelican Bay Prison",
    "Pelican Bay State Prison",
)
BIOL1_LAB_COURSE_SUBTITLE = (
    "**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay"
)
LAB_NAME_DATE_LINE = "**Name:** {fill:text} **Date:** {fill:text}"
PLACEHOLDER_LINKS = {"parent.md", "sibling.md", "child.md", "doc1.md", "doc2.md", "url"}
TEST_DOUBLE_PATTERNS = (
    re.compile(r"from\s+unittest\.mock\s+import"),
    re.compile(r"from\s+unittest\s+import\s+mock"),
    re.compile(r"import\s+unittest\.mock"),
    re.compile(r"@patch\("),
    re.compile(r"\bpatch\("),
    re.compile(r"\bMagicMock\b"),
    re.compile(r"\bMock\("),
)


@dataclass
class RepoContractReport:
    """Result for repository-level contract validation."""

    valid: bool = True
    issues: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def add_issue(self, issue: str) -> None:
        self.valid = False
        self.issues.append(issue)


def validate_repo_contracts(repo_root: Path | str) -> RepoContractReport:
    """Validate repository-level contracts that should hold before publishing."""
    root = Path(repo_root).resolve()
    report = RepoContractReport(summary={})

    _check_required_docs(root, report)
    _check_markdown_links(root, report)
    _check_production_code_no_test_doubles(root, report)
    _check_course_counts(root, report)
    _check_active_course_materials(root, report)
    _check_archive_signposts(root, report)
    _check_published_tracking(root, report)

    return report


def _check_required_docs(root: Path, report: RepoContractReport) -> None:
    checked = 0
    for rel_root in DOC_REQUIRED_ROOTS:
        start = root / rel_root
        if not start.exists():
            report.add_issue(f"{rel_root} does not exist")
            continue
        directories = [start, *sorted(path for path in start.rglob("*") if path.is_dir())]
        for directory in directories:
            if any(part in DOC_EXCLUDED_PARTS for part in directory.relative_to(root).parts):
                continue
            checked += 1
            for doc_name in ("README.md", "AGENTS.md"):
                if not (directory / doc_name).exists():
                    report.add_issue(f"{directory.relative_to(root)} missing {doc_name}")
    report.summary["doc_directories_checked"] = checked


def _check_markdown_links(root: Path, report: RepoContractReport) -> None:
    checked = 0
    for md_path in _markdown_files_to_check(root):
        checked += 1
        text = _strip_fenced_blocks(md_path.read_text(encoding="utf-8", errors="ignore"))
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not _should_check_link(target):
                continue
            target_path = (md_path.parent / target).resolve()
            try:
                target_path.relative_to(root)
            except ValueError:
                continue
            if not target_path.exists():
                report.add_issue(
                    f"{md_path.relative_to(root)} has missing link target: {target}"
                )
    report.summary["markdown_files_checked"] = checked


def _markdown_files_to_check(root: Path) -> list[Path]:
    paths: list[Path] = []
    archive_signposts = (
        Path("archive/README.md"),
        Path("archive/AGENTS.md"),
        Path("archive/spring-2026/README.md"),
        Path("archive/spring-2026/AGENTS.md"),
    )
    for rel in (
        Path("README.md"),
        Path("AGENTS.md"),
        Path("software"),
        Path("course_development"),
        *archive_signposts,
    ):
        start = root / rel
        if start.is_file():
            paths.append(start)
        elif start.exists():
            for path in start.rglob("*.md"):
                if any(part in DOC_EXCLUDED_PARTS for part in path.relative_to(root).parts):
                    continue
                paths.append(path)
    return sorted(set(paths))


def _strip_fenced_blocks(text: str) -> str:
    return FENCE_PATTERN.sub("", text)


def _should_check_link(target: str) -> bool:
    if not target or target in PLACEHOLDER_LINKS:
        return False
    if target.startswith(("/", "#", "mailto:")):
        return False
    if re.match(r"^[a-z][a-z0-9+.-]*:", target):
        return False
    return True


def _check_production_code_no_test_doubles(root: Path, report: RepoContractReport) -> None:
    checked = 0
    for py_path in _production_python_files(root):
        checked += 1
        text = py_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in TEST_DOUBLE_PATTERNS:
            if pattern.search(text):
                report.add_issue(
                    f"{py_path.relative_to(root)} contains production test-double pattern: "
                    f"{pattern.pattern}"
                )
                break
    report.summary["production_python_files_checked"] = checked


def _production_python_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for rel in PRODUCTION_CODE_PATHS:
        start = root / rel
        if start.is_file() and start.suffix == ".py":
            paths.append(start)
        elif start.exists():
            for path in start.rglob("*.py"):
                if any(part in DOC_EXCLUDED_PARTS for part in path.relative_to(root).parts):
                    continue
                paths.append(path)
    return sorted(set(paths))


def _check_course_counts(root: Path, report: RepoContractReport) -> None:
    config_path = root / "publish.toml"
    with config_path.open("rb") as handle:
        publish_config = tomllib.load(handle)
    courses_cfg = publish_config["publish"].get("courses", {})

    course_summary: dict[str, dict[str, int | str]] = {}
    for course, course_cfg in courses_cfg.items():
        if not course_cfg.get("enabled", True):
            archive_path = course_cfg.get("archive_path") or course_cfg.get("archived_path")
            active_path = root / str(course_cfg.get("path", f"course_development/{course}"))
            if active_path.exists():
                report.add_issue(
                    f"{course} is disabled in publish.toml but active path exists: "
                    f"{active_path.relative_to(root)}"
                )
            if not archive_path:
                report.add_issue(f"{course} is disabled but has no archive_path")
            elif not (root / str(archive_path)).exists():
                report.add_issue(f"{course} archive_path does not exist: {archive_path}")
            course_summary[course] = {"status": "archived"}
            continue

        course_root = root / str(course_cfg.get("path", f"course_development/{course}"))
        if not course_root.exists():
            report.add_issue(f"{course} active course path does not exist: {course_root}")
            continue
        course_cfg = courses_cfg.get(course, {})
        modules = sorted((course_root / "course").glob("module-*"))
        numbered_modules = [_module_number(path) for path in modules if path.is_dir()]
        numbered_labs, supplemental_labs = _lab_counts(course_root / "course" / "labs")

        expected_modules = int(course_cfg.get("max_module", course_cfg.get("modules", 0)))
        expected_labs = int(course_cfg.get("max_lab", 0))
        actual_modules = len([n for n in numbered_modules if n is not None])

        if expected_modules != actual_modules:
            report.add_issue(
                f"{course} publish.toml max_module/modules={expected_modules}, "
                f"but source has {actual_modules} numbered modules"
            )
        if expected_labs != numbered_labs:
            report.add_issue(
                f"{course} publish.toml max_lab={expected_labs}, "
                f"but source has {numbered_labs} primary numbered labs"
            )

        course_summary[course] = {
            "status": "active",
            "modules": actual_modules,
            "primary_labs": numbered_labs,
            "supplemental_labs": supplemental_labs,
        }

    report.summary["courses"] = course_summary


def _check_active_course_materials(root: Path, report: RepoContractReport) -> None:
    config_path = root / "publish.toml"
    with config_path.open("rb") as handle:
        publish_config = tomllib.load(handle)
    courses_cfg = publish_config["publish"].get("courses", {})

    for course in active_course_names(root):
        course_cfg = courses_cfg.get(course, {})
        course_root = root / str(course_cfg.get("path", f"course_development/{course}"))
        if not course_root.exists():
            continue
        expected_modules = int(course_cfg.get("max_module", course_cfg.get("modules", 0)))
        expected_labs = int(course_cfg.get("max_lab", 0))
        _check_module_materials(root, course, course_root, expected_modules, report)
        _check_lab_materials(root, course, course_root, expected_labs, report)
        _check_assessment_materials(root, course, course_root, report)
        _check_schedule_references(root, course, course_root, expected_modules, expected_labs, report)
        _check_slide_numbering(root, course, course_root, expected_modules, report)
        if course == "biol-1":
            _check_biol1_active_text(root, course_root, report)


def _check_module_materials(
    root: Path,
    course: str,
    course_root: Path,
    expected_modules: int,
    report: RepoContractReport,
) -> None:
    modules = sorted((course_root / "course").glob("module-*"))
    module_numbers = [_module_number(path) for path in modules if path.is_dir()]
    actual = [number for number in module_numbers if number is not None]
    expected = list(range(1, expected_modules + 1))
    if actual != expected:
        report.add_issue(
            f"{course} module folders are not continuous 1-{expected_modules}: {actual}"
        )

    for module_dir in modules:
        if not module_dir.is_dir():
            continue
        module_number = _module_number(module_dir)
        if module_number is None:
            continue
        for rel_file in ("README.md", "keys-to-success.md", "questions.md"):
            path = module_dir / rel_file
            if not path.exists():
                report.add_issue(f"{path.relative_to(root)} missing")
                continue
            heading = _first_heading(path)
            heading_number = _heading_number("Module", heading)
            if heading_number != module_number:
                report.add_issue(
                    f"{path.relative_to(root)} heading says module {heading_number}, "
                    f"expected {module_number}"
                )
        questions_path = module_dir / "questions.md"
        if questions_path.exists():
            _check_continuous_numbered_items(root, questions_path, report)


def _check_lab_materials(
    root: Path,
    course: str,
    course_root: Path,
    expected_labs: int,
    report: RepoContractReport,
) -> None:
    labs_dir = course_root / "course" / "labs"
    dashboards_dir = labs_dir / "dashboards"
    lab_paths = sorted(
        path
        for path in labs_dir.glob("lab-*.md")
        if not any(marker in path.stem.lower() for marker in SUPPLEMENTAL_LAB_MARKERS)
    )
    lab_numbers = [_lab_number(path) for path in lab_paths]
    actual = [number for number in lab_numbers if number is not None]
    expected = list(range(1, expected_labs + 1))
    if actual != expected:
        report.add_issue(f"{course} lab files are not continuous 1-{expected_labs}: {actual}")

    lab_stems = {path.stem for path in lab_paths}
    for lab_path in lab_paths:
        lab_number = _lab_number(lab_path)
        heading = _first_heading(lab_path)
        heading_number = _heading_number("Lab", heading)
        if heading_number != lab_number:
            report.add_issue(
                f"{lab_path.relative_to(root)} heading says lab {heading_number}, "
                f"expected {lab_number}"
            )
        if course == "biol-1":
            _check_biol1_lab_front_matter(root, lab_path, report)
        expected_dashboard = dashboards_dir / f"{lab_path.stem}-dashboard.html"
        if not expected_dashboard.exists():
            report.add_issue(
                f"{course} lab dashboard missing or slug-mismatched for "
                f"{lab_path.relative_to(root)}: expected {expected_dashboard.relative_to(root)}"
            )

    for dashboard_path in sorted(dashboards_dir.glob("lab-*-dashboard.html")):
        lab_stem = dashboard_path.stem.removesuffix("-dashboard")
        if lab_stem not in lab_stems:
            report.add_issue(
                f"{dashboard_path.relative_to(root)} does not match an active lab markdown stem"
            )
            continue
        lab_number = _lab_number(Path(f"{lab_stem}.md"))
        title_number = _heading_number("Lab", _html_title(dashboard_path))
        if title_number != lab_number:
            report.add_issue(
                f"{dashboard_path.relative_to(root)} title says lab {title_number}, "
                f"expected {lab_number}"
            )


def _check_biol1_lab_front_matter(
    root: Path,
    lab_path: Path,
    report: RepoContractReport,
) -> None:
    nonblank_lines = [
        (line_number, line.strip())
        for line_number, line in enumerate(
            lab_path.read_text(encoding="utf-8", errors="ignore").splitlines(),
            1,
        )
        if line.strip()
    ]
    if len(nonblank_lines) < 4:
        report.add_issue(f"{lab_path.relative_to(root)} has incomplete lab front matter")
        return

    expected_prefixes = (
        ("course subtitle", BIOL1_LAB_COURSE_SUBTITLE),
        ("name/date line", LAB_NAME_DATE_LINE),
    )
    for index, (label, expected_text) in enumerate(expected_prefixes, start=1):
        actual_text = nonblank_lines[index][1]
        if actual_text != expected_text:
            report.add_issue(
                f"{lab_path.relative_to(root)} {label} is {actual_text!r}; "
                f"expected {expected_text!r}"
            )

    first_section = next(
        (line for _, line in nonblank_lines if line.startswith("## ")),
        "",
    )
    if first_section != "## Learning Objectives":
        report.add_issue(
            f"{lab_path.relative_to(root)} first section is {first_section!r}; "
            "expected '## Learning Objectives'"
        )


def _check_assessment_materials(
    root: Path,
    course: str,
    course_root: Path,
    report: RepoContractReport,
) -> None:
    practice_dir = course_root / "course" / "practice_tests"
    practice_tests = sorted(
        path
        for path in practice_dir.glob("practice-test-*.md")
        if not path.name.endswith("_key.md")
    )
    practice_numbers = [_practice_test_number(path) for path in practice_tests]
    expected_practice = list(range(1, len(practice_tests) + 1))
    actual_practice = [number for number in practice_numbers if number is not None]
    if actual_practice != expected_practice:
        report.add_issue(f"{course} practice tests are not continuous: {actual_practice}")
    for test_path in practice_tests:
        test_number = _practice_test_number(test_path)
        key_path = test_path.with_name(f"{test_path.stem}_key.md")
        if not key_path.exists():
            report.add_issue(f"{course} practice test key missing: {key_path.relative_to(root)}")
        heading_number = _heading_number("Practice Test", _first_heading(test_path))
        if heading_number != test_number:
            report.add_issue(
                f"{test_path.relative_to(root)} heading says practice test {heading_number}, "
                f"expected {test_number}"
            )
        _check_continuous_numbered_items(root, test_path, report)

    exams_dir = course_root / "course" / "exams"
    for stem in ("exam-01", "exam-02", "exam-03", "final-exam"):
        for suffix in (".md", "_key.md"):
            path = exams_dir / f"{stem}{suffix}"
            if not path.exists():
                report.add_issue(f"{course} assessment file missing: {path.relative_to(root)}")
    if (exams_dir / "exam-04.md").exists():
        report.add_issue(f"{course} has exam-04.md; use final-exam.md for the final")


def _check_schedule_references(
    root: Path,
    course: str,
    course_root: Path,
    expected_modules: int,
    expected_labs: int,
    report: RepoContractReport,
) -> None:
    schedule_path = course_root / "syllabus" / "Schedule.md"
    if not schedule_path.exists():
        report.add_issue(f"{course} missing syllabus/Schedule.md")
        return
    text = schedule_path.read_text(encoding="utf-8", errors="ignore")
    for label, maximum in (("Module", expected_modules), ("Lab", expected_labs)):
        for match in re.finditer(rf"\b{label}\s+0*(\d+)\b", text):
            number = int(match.group(1))
            if number < 1 or number > maximum:
                report.add_issue(
                    f"{schedule_path.relative_to(root)} references {label} {number}, "
                    f"outside active range 1-{maximum}"
                )
    if re.search(r"\bExam\s+04\b", text):
        report.add_issue(
            f"{schedule_path.relative_to(root)} references Exam 04, but active final is final-exam.md"
        )

    required_dates = (
        "August 22, 2026",
        "September 7, 2026",
        "November 11, 2026",
        "November 23-24, 2026",
        "November 25-27, 2026",
        "December 12-18, 2026",
        "December 18, 2026",
    )
    for date_text in required_dates:
        if date_text not in text:
            report.add_issue(
                f"{schedule_path.relative_to(root)} missing Fall 2026 calendar anchor: "
                f"{date_text}"
            )

    required_practice_tests = (
        "Practice Test 01",
        "Practice Test 02",
        "Practice Test 03",
        "Practice Test 04",
        "Practice Test 05",
    )
    for practice_test in required_practice_tests:
        if practice_test not in text:
            report.add_issue(
                f"{schedule_path.relative_to(root)} missing active review reference: "
                f"{practice_test}"
            )


def _check_slide_numbering(
    root: Path,
    course: str,
    course_root: Path,
    expected_modules: int,
    report: RepoContractReport,
) -> None:
    slides_dir = course_root / "resources" / "slides"
    if not slides_dir.exists():
        return
    for slide_path in sorted(slides_dir.glob("*.pdf")):
        match = SLIDE_NUMBER_PATTERN.match(slide_path.name)
        if not match:
            report.add_issue(
                f"{slide_path.relative_to(root)} does not follow module-N-slides-*.pdf"
            )
            continue
        number = int(match.group(1))
        if number < 1 or number > expected_modules:
            report.add_issue(
                f"{slide_path.relative_to(root)} references module {number}, "
                f"outside active range 1-{expected_modules}"
            )


def _check_biol1_active_text(root: Path, course_root: Path, report: RepoContractReport) -> None:
    for md_path in sorted(course_root.rglob("*.md")):
        rel_parts = md_path.relative_to(course_root).parts
        if "private" in rel_parts or "output" in rel_parts:
            continue
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in ACTIVE_BIOL1_FORBIDDEN_TEXT:
            if forbidden in text:
                report.add_issue(
                    f"{md_path.relative_to(root)} contains stale active-course text: {forbidden}"
                )


def _check_archive_signposts(root: Path, report: RepoContractReport) -> None:
    required = (
        Path("archive/README.md"),
        Path("archive/AGENTS.md"),
        Path("archive/spring-2026/README.md"),
        Path("archive/spring-2026/AGENTS.md"),
        Path("archive/spring-2026/course_development/biol-1"),
        Path("archive/spring-2026/course_development/biol-8"),
        Path("archive/spring-2026/PUBLISHED/biol-1"),
        Path("archive/spring-2026/PUBLISHED/biol-8"),
    )
    for rel_path in required:
        if not (root / rel_path).exists():
            report.add_issue(f"Archive signpost or snapshot missing: {rel_path}")

    for course, archive_path in archived_course_paths(root).items():
        if not (root / archive_path).exists():
            report.add_issue(f"{course} configured archive_path missing: {archive_path}")


def _module_number(path: Path) -> int | None:
    match = MODULE_NUMBER_PATTERN.match(path.name)
    return int(match.group(1)) if match else None


def _lab_number(path: Path) -> int | None:
    match = LAB_NUMBER_PATTERN.match(path.stem)
    return int(match.group(1)) if match else None


def _lab_counts(labs_dir: Path) -> tuple[int, int]:
    primary = 0
    supplemental = 0
    for lab_path in sorted(labs_dir.glob("lab-*.md")):
        match = LAB_NUMBER_PATTERN.match(lab_path.stem)
        lower_stem = lab_path.stem.lower()
        is_supplemental = any(marker in lower_stem for marker in SUPPLEMENTAL_LAB_MARKERS)
        if match and not is_supplemental:
            primary += 1
        else:
            supplemental += 1
    return primary, supplemental


def _practice_test_number(path: Path) -> int | None:
    match = re.match(r"practice-test-(\d+)$", path.stem)
    return int(match.group(1)) if match else None


def _first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# "):
            return line
    return ""


def _html_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    return match.group(1) if match else ""


def _heading_number(label: str, text: str) -> int | None:
    match = re.search(rf"\b{re.escape(label)}\s+0*(\d+)\b", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _check_continuous_numbered_items(
    root: Path,
    path: Path,
    report: RepoContractReport,
) -> None:
    numbers: list[int] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = re.match(r"^(?:\*\*)?(\d+)\.(?:\*\*)?\s", line)
        if match:
            numbers.append(int(match.group(1)))
    if not numbers:
        report.add_issue(f"{path.relative_to(root)} has no top-level numbered items")
        return
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        report.add_issue(
            f"{path.relative_to(root)} numbered items are not continuous 1-{len(numbers)}: "
            f"{numbers}"
        )


def _check_published_tracking(root: Path, report: RepoContractReport) -> None:
    result = subprocess.run(
        ["git", "ls-files", "PUBLISHED"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    active = active_course_names(root)
    active_tracked = [
        line
        for line in tracked
        if any(line.startswith(f"PUBLISHED/{course}/") for course in active)
    ]
    report.summary["published_files_tracked"] = len(tracked)
    report.summary["active_published_files_tracked"] = len(active_tracked)
    if result.returncode != 0:
        report.add_issue(f"git ls-files PUBLISHED failed: {result.stderr.strip()}")
    elif not tracked:
        report.add_issue("PUBLISHED/ is not tracked; subtree publishing expects tracked files")
    elif not active_tracked:
        report.add_issue("Active PUBLISHED/ course files are not tracked")

    for course in active:
        if not (root / "PUBLISHED" / course).exists():
            report.add_issue(f"Active published course directory missing: PUBLISHED/{course}")

    gitignore = root / ".gitignore"
    if gitignore.exists():
        for line_number, line in enumerate(gitignore.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and stripped.rstrip("/") == "PUBLISHED":
                report.add_issue(
                    f".gitignore line {line_number} ignores PUBLISHED/, "
                    "but the publish contract keeps it tracked"
                )
