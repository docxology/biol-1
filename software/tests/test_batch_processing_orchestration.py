"""Tests for batch processing orchestration functions."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from src.batch_processing.main import (
    process_course_modules,
    process_course_syllabus,
    process_course_labs,
    process_course_practice_tests,
    process_course_exams,
)


class TestProcessCourseModules:
    """Tests for process_course_modules function."""

    @pytest.fixture
    def mock_process_by_type(self):
        with patch("src.batch_processing.main.process_module_by_type") as mock:
            mock.return_value = {
                "summary": {"pdf": 1, "mp3": 1, "docx": 1, "html": 1, "txt": 1, "md": 1},
                "errors": [],
            }
            yield mock

    @pytest.fixture
    def mock_process_website(self):
        with patch("src.batch_processing.main.process_module_website") as mock:
            mock.return_value = "index.html"
            yield mock

    @pytest.fixture
    def mock_matches_module(self):
        with patch("src.module_organization.utils.matches_module_number") as mock:
            mock.return_value = True
            yield mock

    def test_process_course_modules_success(
        self, temp_dir, mock_process_by_type, mock_process_website
    ):
        """Test successful processing of course modules."""
        # Setup course structure
        course_dir = temp_dir / "course"
        course_dir.mkdir()
        (course_dir / "module-01").mkdir()
        (course_dir / "module-02").mkdir()

        result = process_course_modules(temp_dir, "Test Course")

        assert result["course"] == "Test Course"
        assert len(result["modules"]) == 2
        assert result["errors"] == []
        assert mock_process_by_type.call_count == 2
        assert mock_process_website.call_count == 2

    def test_process_course_modules_missing_dir(self, temp_dir):
        """Test processing with missing course directory."""
        result = process_course_modules(temp_dir, "Test Course")
        
        assert result["modules"] == []
        assert result["errors"] == []

    def test_process_course_modules_filter(
        self, temp_dir, mock_process_by_type, mock_process_website
    ):
        """Test filtering modules by number."""
        course_dir = temp_dir / "course"
        course_dir.mkdir()
        (course_dir / "module-01").mkdir()
        (course_dir / "module-02").mkdir()

        # Mock matches_module_number to only match module-01
        with patch("src.module_organization.utils.matches_module_number") as mock_match:
            mock_match.side_effect = lambda name, num: name == "module-01"
            
            result = process_course_modules(
                temp_dir, "Test Course", module_filter=1
            )

        assert len(result["modules"]) == 1
        assert result["modules"][0]["name"] == "module-01"
        assert mock_process_by_type.call_count == 1

    def test_process_course_modules_error_handling(
        self, temp_dir, mock_process_by_type, mock_process_website
    ):
        """Test handling of processing errors."""
        course_dir = temp_dir / "course"
        course_dir.mkdir()
        (course_dir / "module-01").mkdir()

        mock_process_by_type.side_effect = Exception("Processing failed")

        result = process_course_modules(temp_dir, "Test Course")

        assert len(result["errors"]) > 0
        assert "Processing failed" in result["errors"][0]

    def test_process_course_modules_internal_errors(
        self, temp_dir, mock_process_by_type, mock_process_website
    ):
        """Test handling of errors reported by process_module_by_type."""
        course_dir = temp_dir / "course"
        course_dir.mkdir()
        (course_dir / "module-01").mkdir()

        mock_process_by_type.return_value = {
            "summary": {"pdf": 0, "mp3": 0, "docx": 0, "html": 0, "txt": 0, "md": 0},
            "errors": ["Some internal error"],
        }
        # Reset side effect
        mock_process_by_type.side_effect = None

        result = process_course_modules(temp_dir, "Test Course")

        assert len(result["errors"]) > 0
        assert "Some internal error" in result["errors"][0]


class TestProcessCourseSyllabus:
    """Tests for process_course_syllabus function."""

    @pytest.fixture
    def mock_process_syllabus(self):
        with patch("src.batch_processing.main.process_syllabus") as mock:
            mock.return_value = {
                "summary": {"pdf": 1, "mp3": 1, "docx": 1, "html": 1, "txt": 1, "md": 1},
                "errors": [],
            }
            yield mock

    def test_process_course_syllabus_success(self, temp_dir, mock_process_syllabus):
        """Test successful syllabus processing."""
        (temp_dir / "syllabus").mkdir()
        
        result = process_course_syllabus(temp_dir, "Test Course")
        
        assert result["processed"] is True
        assert result["errors"] == []
        assert mock_process_syllabus.called

    def test_process_course_syllabus_missing_dir(self, temp_dir):
        """Test processing with missing syllabus directory."""
        result = process_course_syllabus(temp_dir, "Test Course")
        
        assert result["processed"] is False
        assert result["errors"] == []

    def test_process_course_syllabus_error(self, temp_dir, mock_process_syllabus):
        """Test handling of exceptions."""
        (temp_dir / "syllabus").mkdir()
        mock_process_syllabus.side_effect = Exception("Syllabus failed")
        
        result = process_course_syllabus(temp_dir, "Test Course")
        
        assert result["processed"] is False
        assert len(result["errors"]) > 0
        assert "Syllabus failed" in result["errors"][0]


class TestProcessCourseLabs:
    """Tests for process_course_labs function."""

    @pytest.fixture
    def mock_render_labs(self):
        with patch("src.lab_manual.main.batch_render_lab_manuals") as mock:
            mock.return_value = ["lab1.pdf", "lab2.pdf"]
            yield mock

    def test_process_course_labs_success(self, temp_dir, mock_render_labs):
        """Test successful lab processing."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        
        result = process_course_labs(temp_dir, "Test Course", formats=["pdf"])
        
        assert result["processed"] is True
        assert len(result["files"]) > 0
        assert result["errors"] == []
        assert mock_render_labs.called

    def test_process_course_labs_missing_dir(self, temp_dir):
        """Test processing with missing labs directory."""
        result = process_course_labs(temp_dir, "Test Course")
        
        assert result["processed"] is False
        assert result["errors"] == []

    def test_process_course_labs_no_formats(self, temp_dir):
        """Test processing with no compatible formats."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        
        result = process_course_labs(
            temp_dir, "Test Course", formats=["docx", "mp3"]
        )
        
        assert result["processed"] is False
        assert result["files"] == []


class TestProcessCoursePracticeTests:
    """Tests for process_course_practice_tests function."""

    @pytest.fixture
    def mock_render_pdf(self):
        with patch("src.markdown_to_pdf.main.render_markdown_to_pdf") as mock:
            yield mock

    def test_process_practice_tests_success(self, temp_dir, mock_render_pdf):
        """Test successful practice test processing."""
        pt_dir = temp_dir / "course" / "practice_tests"
        pt_dir.mkdir(parents=True)
        (pt_dir / "test-1.md").write_text("# Test", encoding="utf-8")
        
        result = process_course_practice_tests(
            temp_dir, "Test Course", formats=["pdf"]
        )
        
        assert result["processed"] is True
        assert len(result["files"]) == 1
        assert mock_render_pdf.called

    def test_process_practice_tests_missing_dir(self, temp_dir):
        """Test processing with missing directory."""
        result = process_course_practice_tests(temp_dir, "Test Course")
        
        assert result["processed"] is False

    def test_process_practice_tests_skip_formats(self, temp_dir):
        """Test skipping when PDF not requested."""
        pt_dir = temp_dir / "course" / "practice_tests"
        pt_dir.mkdir(parents=True)
        (pt_dir / "test-1.md").write_text("# Test", encoding="utf-8")
        
        result = process_course_practice_tests(
            temp_dir, "Test Course", formats=["docx", "html"]
        )
        
        assert result["processed"] is False
        assert result["files"] == []


class TestProcessCourseExams:
    """Tests for process_course_exams function."""

    @pytest.fixture
    def mock_render_pdf(self):
        with patch("src.markdown_to_pdf.main.render_markdown_to_pdf") as mock:
            yield mock

    @pytest.fixture
    def mock_convert_file(self):
        with patch("src.format_conversion.main.convert_file") as mock:
            yield mock

    def test_process_exams_success(self, temp_dir, mock_render_pdf):
        """Test successful exam rendering to PDF."""
        exams_dir = temp_dir / "course" / "exams"
        exams_dir.mkdir(parents=True)
        (exams_dir / "exam-01.md").write_text("# Exam 1", encoding="utf-8")

        result = process_course_exams(
            temp_dir, "Test Course", formats=["pdf"]
        )

        assert result["processed"] is True
        assert len(result["files"]) == 1
        assert mock_render_pdf.called

    def test_process_exams_missing_dir(self, temp_dir):
        """Test processing with missing exams directory."""
        result = process_course_exams(temp_dir, "Test Course")

        assert result["processed"] is False
        assert result["errors"] == []

    def test_process_exams_skip_formats(self, temp_dir):
        """Test skipping when no exam-compatible formats requested."""
        exams_dir = temp_dir / "course" / "exams"
        exams_dir.mkdir(parents=True)
        (exams_dir / "exam-01.md").write_text("# Exam 1", encoding="utf-8")

        result = process_course_exams(
            temp_dir, "Test Course", formats=["mp3", "html"]
        )

        assert result["processed"] is False
        assert result["files"] == []

    def test_process_exams_includes_keys(self, temp_dir, mock_render_pdf):
        """Test that answer keys ARE rendered locally (unlike publish which excludes them)."""
        exams_dir = temp_dir / "course" / "exams"
        exams_dir.mkdir(parents=True)
        (exams_dir / "exam-01.md").write_text("# Exam 1", encoding="utf-8")
        (exams_dir / "exam-01_key.md").write_text("# Key", encoding="utf-8")
        (exams_dir / "README.md").write_text("# README", encoding="utf-8")

        result = process_course_exams(
            temp_dir, "Test Course", formats=["pdf"]
        )

        assert result["processed"] is True
        # Both exam and key are rendered, README is skipped
        assert len(result["files"]) == 2
        assert mock_render_pdf.call_count == 2

    def test_process_exams_pdf_and_docx(
        self, temp_dir, mock_render_pdf, mock_convert_file
    ):
        """Test rendering exams to both PDF and DOCX formats."""
        exams_dir = temp_dir / "course" / "exams"
        exams_dir.mkdir(parents=True)
        (exams_dir / "exam-01.md").write_text("# Exam 1", encoding="utf-8")

        result = process_course_exams(
            temp_dir, "Test Course", formats=["pdf", "docx"]
        )

        assert result["processed"] is True
        assert len(result["files"]) == 2  # 1 PDF + 1 DOCX
        assert mock_render_pdf.call_count == 1
        assert mock_convert_file.call_count == 1
