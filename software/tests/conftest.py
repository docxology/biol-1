"""Shared pytest fixtures for testing."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing.

    Yields:
        Path to temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown_file(temp_dir):
    """Create a sample Markdown file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path to sample Markdown file
    """
    md_file = temp_dir / "sample.md"
    md_content = """# Sample Document

This is a sample Markdown document for testing.

## Section 1

Some content here.

- Item 1
- Item 2

## Section 2

More content.
"""
    md_file.write_text(md_content, encoding="utf-8")
    return md_file


@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path to sample text file
    """
    txt_file = temp_dir / "sample.txt"
    txt_content = "This is a sample text file for testing."
    txt_file.write_text(txt_content, encoding="utf-8")
    return txt_file


@pytest.fixture
def sample_module_structure(temp_dir):
    """Create a sample module structure for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path to sample module directory
    """
    module_dir = temp_dir / "course" / "module-1"
    module_dir.mkdir(parents=True)

    # Create required files
    (module_dir / "README.md").write_text("# Module 1\n", encoding="utf-8")
    (module_dir / "AGENTS.md").write_text("# Module 1 Technical Docs\n", encoding="utf-8")

    # Create assignments directory
    assignments_dir = module_dir / "assignments"
    assignments_dir.mkdir()
    (assignments_dir / "README.md").write_text("# Assignments\n", encoding="utf-8")
    (assignments_dir / "AGENTS.md").write_text("# Assignments Docs\n", encoding="utf-8")

    return module_dir


@pytest.fixture
def sample_curriculum_files(temp_dir):
    """Create sample files for each curriculum element type.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Dict mapping curriculum types to file paths
    """
    module_dir = temp_dir / "module-1"
    module_dir.mkdir()

    files = {
        "assignment": module_dir / "sample_assignment.md",
        "lab-protocol": module_dir / "sample_lab-protocol.md",
        "lecture-content": module_dir / "sample_lecture-content.md",
        "study-guide": module_dir / "sample_study-guide.md",
    }

    files["assignment"].write_text("# Assignment\nContent.\n", encoding="utf-8")
    files["lab-protocol"].write_text("# Lab Protocol\nContent.\n", encoding="utf-8")
    files["lecture-content"].write_text("# Lecture\nContent.\n", encoding="utf-8")
    files["study-guide"].write_text("# Study Guide\nContent.\n", encoding="utf-8")

    return {"module_dir": module_dir, "files": files}
