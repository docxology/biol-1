"""Tests for batch processing utility functions."""

from pathlib import Path
from unittest.mock import patch, MagicMock
from src.batch_processing.utils import (
    find_markdown_files,
    find_audio_files,
    should_process_file,
    get_relative_output_path,
    get_courses_to_process,
    get_formats_to_process,
    generate_dry_run_report,
)
from src.shared.file_utils import ensure_output_directory
from src.batch_processing import config


def test_find_markdown_files(temp_dir):
    """Test finding markdown files."""
    (temp_dir / "test.md").touch()
    (temp_dir / "test.markdown").touch()
    (temp_dir / "test.txt").touch()
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    (subdir / "sub.md").touch()

    files = find_markdown_files(temp_dir)
    filenames = [f.name for f in files]
    
    assert "test.md" in filenames
    assert "test.markdown" in filenames
    assert "sub.md" in filenames
    assert "test.txt" not in filenames


def test_find_audio_files(temp_dir):
    """Test finding audio files."""
    (temp_dir / "test.mp3").touch()
    (temp_dir / "test.wav").touch()
    (temp_dir / "test.txt").touch()

    files = find_audio_files(temp_dir)
    filenames = [f.name for f in files]
    
    assert "test.mp3" in filenames
    assert "test.wav" in filenames
    assert "test.txt" not in filenames


def test_should_process_file():
    """Test skipping logic."""
    skip_dirs = ["skip_me", "output"]
    
    assert should_process_file(Path("a/b/c.md"), skip_dirs) is True
    assert should_process_file(Path("a/skip_me/c.md"), skip_dirs) is False
    assert should_process_file(Path("output/c.md"), skip_dirs) is False


def test_ensure_output_directory(temp_dir):
    """Test creating output directory."""
    out_dir = temp_dir / "new_dir" / "subdir"
    ensure_output_directory(out_dir)
    assert out_dir.exists()


def test_get_relative_output_path():
    """Test relative path calculation."""
    source_dir = Path("/src")
    out_dir = Path("/out")
    
    # /src/a/file.md -> /out/a/file.md
    source_file = Path("/src/a/file.md")
    result = get_relative_output_path(source_file, source_dir, out_dir)
    
    assert result == Path("/out/a/file.md")


def test_get_courses_to_process():
    """Test course selection logic."""
    # Mock available courses to ensure stable test
    with patch("src.batch_processing.config.AVAILABLE_COURSES", ["biol-1"]):
        assert get_courses_to_process("all") == [("course_development/biol-1", "BIOL-1")]
        assert get_courses_to_process("biol-1") == [("course_development/biol-1", "BIOL-1")]
        assert get_courses_to_process("biol-1") == [("course_development/biol-1", "BIOL-1")]
        # "biol" matches ends_with so it won't match "biol-1" correctly unless exact?
        # logic is: if c.endswith(course_arg)
        # "biol-1".endswith("biol-1") is True.
        assert get_courses_to_process("invalid") == []


def test_get_formats_to_process(caplog):
    """Test format parsing logic."""
    with patch("src.batch_processing.config.AVAILABLE_FORMATS", {"pdf", "html"}):
        assert set(get_formats_to_process("all")) == {"pdf", "html"}
        assert get_formats_to_process("pdf") == ["pdf"]
        assert get_formats_to_process("PDF, html") == ["pdf", "html"]
        assert get_formats_to_process("pdf, invalid") == ["pdf"]
        
        assert "Unknown formats will be ignored" in caplog.text


def test_generate_dry_run_report(temp_dir):
    """Test dry run report generation."""
    repo_root = temp_dir
    course_path = repo_root / "course_development/biol-1"
    course_path.mkdir(parents=True)
    
    # Create module structure
    module_dir = course_path / "course" / "module-01"
    module_dir.mkdir(parents=True)
    (module_dir / "test.md").touch()
    
    # Assignments
    (module_dir / "assignments").mkdir()
    (module_dir / "assignments" / "assign.md").touch()
    
    # Syllabus
    syllabus_dir = course_path / "syllabus"
    syllabus_dir.mkdir()
    (syllabus_dir / "Syllabus.md").touch()
    
    # Labs
    labs_dir = course_path / "course" / "labs"
    labs_dir.mkdir(parents=True)
    (labs_dir / "lab-1.md").touch()
    
    courses = [("course_development/biol-1", "BIOL-1")]
    formats = ["pdf", "html"]
    
    # Mock matches_module_number using patch since it's imported inside the function
    with patch("src.module_organization.utils.matches_module_number", return_value=True):
        report = generate_dry_run_report(
            repo_root, 
            courses, 
            formats,
            module_filter=None,
            generate_website=True,
            skip_labs=False
        )
        
    assert "DRY RUN" in report
    assert "BIOL-1" in report
    assert "module-01" in report
    assert "1 root files" in report
    assert "1 assignments" in report
    assert "website/index.html" in report
    assert "Syllabus: 1 files" in report
    assert "Labs: 1 files" in report
    assert "pdf, html" in report


def test_generate_dry_run_report_filter(temp_dir):
    """Test dry run report with module filter."""
    repo_root = temp_dir
    course_path = repo_root / "course_development/biol-1"
    course_path.mkdir(parents=True)
    (course_path / "course" / "module-01").mkdir(parents=True)
    
    courses = [("course_development/biol-1", "BIOL-1")]
    formats = ["pdf"]
    
    # Mock matches_module_number to return False (simulating filter mismatch)
    with patch("src.module_organization.utils.matches_module_number", return_value=False):
        report = generate_dry_run_report(
            repo_root, 
            courses, 
            formats,
            module_filter=99
        )
        
    # Should not show any modules
    assert "module-01" not in report
