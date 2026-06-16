"""Tests for repository-level contract validation."""

from pathlib import Path
from subprocess import CompletedProcess

from src.validation import repo_contracts
from src.validation.repo_contracts import validate_repo_contracts


BIOL1_LAB_FRONT_MATTER = (
    "# Lab 1: Active Topic\n\n"
    "**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay\n\n"
    "**Name:** {fill:text} **Date:** {fill:text}\n\n"
    "---\n\n"
    "## Learning Objectives\n\n"
    "1. Practice one skill.\n"
)


def test_repo_contracts_pass_for_current_tree():
    """Current repository satisfies documentation and publish contracts."""
    repo_root = Path(__file__).resolve().parents[2]
    report = validate_repo_contracts(repo_root)

    assert report.valid is True, "\n".join(report.issues)
    assert report.summary["published_files_tracked"] > 0
    assert report.summary["production_python_files_checked"] > 0


def test_published_tracking_contract_fails_when_untracked(temp_dir, monkeypatch):
    """PUBLISHED/ must remain tracked for subtree publishing."""
    (temp_dir / ".gitignore").write_text("", encoding="utf-8")

    def fake_run(*args, **kwargs):
        return CompletedProcess(args=args, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(repo_contracts.subprocess, "run", fake_run)

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_published_tracking(temp_dir, report)

    assert report.valid is False
    assert any("PUBLISHED/" in issue for issue in report.issues)


def test_production_code_contract_flags_test_doubles(temp_dir):
    """Production source must not import mock/test-double helpers."""
    src_dir = temp_dir / "software" / "src" / "example"
    src_dir.mkdir(parents=True)
    (src_dir / "main.py").write_text(
        "from unittest.mock import Mock\n\nvalue = Mock()\n",
        encoding="utf-8",
    )

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_production_code_no_test_doubles(temp_dir, report)

    assert report.valid is False
    assert any("production test-double pattern" in issue for issue in report.issues)


def test_module_heading_contract_flags_wrong_number(temp_dir):
    """Module headings must match the module folder number."""
    module_dir = temp_dir / "course_development" / "biol-1" / "course" / "module-07-topic"
    module_dir.mkdir(parents=True)
    (module_dir / "README.md").write_text("# Module 08 Wrong\n", encoding="utf-8")
    (module_dir / "keys-to-success.md").write_text("# Module 7: Topic\n", encoding="utf-8")
    (module_dir / "questions.md").write_text(
        "# Module 7: Topic\n\n1. Question one?\n",
        encoding="utf-8",
    )

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_module_materials(
        temp_dir,
        "biol-1",
        temp_dir / "course_development" / "biol-1",
        7,
        report,
    )

    assert report.valid is False
    assert any("heading says module 8, expected 7" in issue for issue in report.issues)


def test_lab_dashboard_contract_flags_slug_mismatch(temp_dir):
    """A dashboard must match the active lab markdown stem, not just its number."""
    labs_dir = temp_dir / "course_development" / "biol-1" / "course" / "labs"
    dashboards_dir = labs_dir / "dashboards"
    dashboards_dir.mkdir(parents=True)
    (labs_dir / "lab-01_active-topic.md").write_text(
        BIOL1_LAB_FRONT_MATTER,
        encoding="utf-8",
    )
    (dashboards_dir / "lab-01_old-topic-dashboard.html").write_text(
        "<title>Lab 1 Dashboard: Old Topic</title>",
        encoding="utf-8",
    )

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_lab_materials(
        temp_dir,
        "biol-1",
        temp_dir / "course_development" / "biol-1",
        1,
        report,
    )

    assert report.valid is False
    assert any("slug-mismatched" in issue for issue in report.issues)
    assert any("does not match an active lab markdown stem" in issue for issue in report.issues)


def test_lab_contract_flags_missing_standard_front_matter(temp_dir):
    """BIOL-1 labs must start with the documented course/name/objectives block."""
    labs_dir = temp_dir / "course_development" / "biol-1" / "course" / "labs"
    dashboards_dir = labs_dir / "dashboards"
    dashboards_dir.mkdir(parents=True)
    (labs_dir / "lab-01_active-topic.md").write_text(
        "# Lab 1: Active Topic\n\n"
        "**BIOL-1: Wrong Course** | College of the Redwoods\n\n"
        "**Name:** {fill:text} **Date:** {fill:text}\n\n"
        "---\n\n"
        "## Overview\n\nNo standard header.\n",
        encoding="utf-8",
    )
    (dashboards_dir / "lab-01_active-topic-dashboard.html").write_text(
        "<title>Lab 1 Dashboard: Active Topic</title>",
        encoding="utf-8",
    )

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_lab_materials(
        temp_dir,
        "biol-1",
        temp_dir / "course_development" / "biol-1",
        1,
        report,
    )

    assert report.valid is False
    assert any("course subtitle" in issue for issue in report.issues)
    assert any("first section" in issue for issue in report.issues)


def test_slide_contract_flags_out_of_range_module(temp_dir):
    """Active slide assets must not advertise modules outside the active range."""
    slides_dir = temp_dir / "course_development" / "biol-1" / "resources" / "slides"
    slides_dir.mkdir(parents=True)
    (slides_dir / "module-16-slides-full.pdf").write_bytes(b"%PDF-1.4\n")

    report = repo_contracts.RepoContractReport()
    repo_contracts._check_slide_numbering(
        temp_dir,
        "biol-1",
        temp_dir / "course_development" / "biol-1",
        15,
        report,
    )

    assert report.valid is False
    assert any("outside active range 1-15" in issue for issue in report.issues)
