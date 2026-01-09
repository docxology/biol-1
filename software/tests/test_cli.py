"""Tests for CLI functionality of generation scripts."""

import subprocess
import sys
from pathlib import Path

import pytest


# Path to the scripts directory
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
SOFTWARE_DIR = Path(__file__).parent.parent


class TestGenerateAllOutputsCLI:
    """Test CLI for generate_all_outputs.py."""

    def test_help_output(self):
        """Test that --help displays usage information."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_all_outputs.py"), "--help"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--course" in result.stdout
        assert "--module" in result.stdout
        assert "--formats" in result.stdout
        assert "--dry-run" in result.stdout
        assert "--skip-clear" in result.stdout
        assert "--no-website" in result.stdout

    def test_course_choices(self):
        """Test that --course only accepts valid choices."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_all_outputs.py"), "--course", "invalid"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower()

    def test_dry_run_mode(self):
        """Test that dry-run mode doesn't generate files."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_all_outputs.py"),
                "--dry-run",
                "--course",
                "biol-1",
            ],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        assert "DRY RUN" in result.stdout or "DRY RUN" in result.stderr
        assert "No files were generated" in result.stdout or "No files were generated" in result.stderr

    def test_module_filter_display(self):
        """Test that module filter is displayed correctly."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_all_outputs.py"),
                "--dry-run",
                "--course",
                "biol-1",
                "--module",
                "1",
            ],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        # Check that module filter is mentioned
        output = result.stdout + result.stderr
        assert "module-1" in output.lower() or "module filter" in output.lower()


class TestGenerateModuleRenderingsCLI:
    """Test CLI for generate_module_renderings.py."""

    def test_help_output(self):
        """Test that --help displays usage information."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_module_renderings.py"), "--help"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--course" in result.stdout
        assert "--module" in result.stdout

    def test_course_choices(self):
        """Test that --course only accepts valid choices."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_module_renderings.py"), "--course", "invalid"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower()

    def test_invalid_module_shows_available(self):
        """Test that invalid module number shows available modules."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_module_renderings.py"),
                "--course",
                "biol-1",
                "--module",
                "999",
            ],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 1
        # Should show available modules
        assert "available" in result.stdout.lower() or "module-" in result.stdout.lower()


class TestGenerateSyllabusRenderingsCLI:
    """Test CLI for generate_syllabus_renderings.py."""

    def test_help_output(self):
        """Test that --help displays usage information."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_syllabus_renderings.py"), "--help"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--course" in result.stdout

    def test_course_choices(self):
        """Test that --course only accepts valid choices."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_syllabus_renderings.py"), "--course", "invalid"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower()


class TestGenerateModuleWebsiteCLI:
    """Test CLI for generate_module_website.py."""

    def test_help_output(self):
        """Test that --help displays usage information."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_module_website.py"), "--help"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--course" in result.stdout
        assert "--module" in result.stdout

    def test_course_choices(self):
        """Test that --course only accepts valid choices."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_module_website.py"), "--course", "invalid"],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower()

    def test_invalid_module_shows_available(self):
        """Test that invalid module number shows available modules."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_module_website.py"),
                "--course",
                "biol-8",
                "--module",
                "999",
            ],
            capture_output=True,
            text=True,
            cwd=str(SOFTWARE_DIR),
        )
        assert result.returncode == 1
        # Should show available modules
        assert "available" in result.stdout.lower() or "module-" in result.stdout.lower()
