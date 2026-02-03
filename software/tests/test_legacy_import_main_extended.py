"""Extended tests for legacy_import main module to improve coverage."""

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.legacy_import.main import (
    create_for_upload_files,
    process_chapter_questions,
)


class TestCreateForUploadFiles:
    """Tests for create_for_upload_files function."""

    @pytest.fixture
    def mock_dependencies(self):
        with patch("src.markdown_to_pdf.main.render_markdown_to_pdf") as mock_pdf, \
             patch("src.format_conversion.main.convert_file") as mock_docx:
            yield mock_pdf, mock_docx

    def test_create_files_success(self, temp_dir, mock_dependencies):
        """Test successful creation of upload files."""
        mock_pdf, mock_docx = mock_dependencies

        module_path = temp_dir / "module-01"
        module_path.mkdir()
        resources_dir = module_path / "resources"
        resources_dir.mkdir()
        
        # specific files to skip/include
        (resources_dir / "keys-to-success.md").touch()
        (resources_dir / "README.md").touch() # Should be excluded
        
        slides_dir = module_path / "slides"
        slides_dir.mkdir()
        (slides_dir / "lecture.pdf").touch()

        result = create_for_upload_files(module_path, 1, dry_run=False)

        assert result["summary"]["pdf"] == 1 
        assert result["summary"]["docx"] == 1
        assert result["summary"]["slides_copied"] == 1
        assert result["errors"] == []

        assert (module_path / "for_upload").exists()
        assert (module_path / "for_upload" / "lecture.pdf").exists()
        
        # Verify calls
        mock_pdf.assert_called()
        mock_docx.assert_called()

    def test_dry_run(self, temp_dir):
        """Test dry run logic for for_upload files."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()
        resources_dir = module_path / "resources"
        resources_dir.mkdir()
        (resources_dir / "test.md").touch()

        result = create_for_upload_files(module_path, 1, dry_run=True)

        assert result["summary"]["pdf"] == 0
        assert not (module_path / "for_upload").exists()

    def test_error_handling(self, temp_dir, mock_dependencies):
        """Test error handling during conversion."""
        mock_pdf, _ = mock_dependencies
        mock_pdf.side_effect = Exception("Conversion failed")

        module_path = temp_dir / "module-01"
        module_path.mkdir()
        resources_dir = module_path / "resources"
        resources_dir.mkdir()
        (resources_dir / "test.md").touch()

        result = create_for_upload_files(module_path, 1, dry_run=False)

        assert result["summary"]["errors"] == 1
        assert "Conversion failed" in result["errors"][0]["error"]


class TestProcessChapterQuestionsExtended:
    """Extended tests for process_chapter_questions."""

    @pytest.fixture
    def mock_convert(self):
        with patch("src.format_conversion.utils.convert_docx_to_markdown") as mock:
            mock.return_value = "# Converted Content"
            yield mock

    def test_process_real_files(self, temp_dir, mock_convert):
        """Test actual processing of files (dry_run=False)."""
        source_dir = temp_dir / "questions"
        source_dir.mkdir()
        (source_dir / "Chapter 01 Questions.docx").touch()

        course_root = temp_dir / "biol-1"
        course_dir = course_root / "course"
        course_dir.mkdir(parents=True)
        # Ensure module exists
        (course_dir / "module-1").mkdir(parents=True)

        # We need to mock get_chapter_to_module_mapping implicitly used
        with patch("src.legacy_import.main.get_chapter_to_module_mapping", return_value={1: 1}):
            results = process_chapter_questions(
                source_dir, course_root, course_dir, dry_run=False
            )

        assert results["summary"]["converted"] == 1
        
        output_file = course_dir / "module-1" / "resources" / "module-1-keys-to-success.md"
        assert output_file.exists()
        assert output_file.read_text() == "# Converted Content"

    def test_process_creates_module(self, temp_dir, mock_convert):
        """Test that processing creates module if missing."""
        source_dir = temp_dir / "questions"
        source_dir.mkdir()
        (source_dir / "Chapter 02 Questions.docx").touch()

        course_root = temp_dir / "biol-1"
        course_dir = course_root / "course"
        course_dir.mkdir(parents=True)
        
        # Patch utils.create_module_structure because that's where ensures_module_exists calls it
        # Also patch get_chapter_to_module_mapping
        with patch("src.legacy_import.main.get_chapter_to_module_mapping", return_value={2: 2}), \
             patch("src.legacy_import.utils.create_module_structure") as mock_utils_create:
            
            # ensure ensure_module_exists calls create_module_structure
            # use side_effect to actually create dir
            def side_effect(root, num):
                p = course_dir / f"module-{num}"
                p.mkdir()
                return p
            
            mock_utils_create.side_effect = side_effect

            results = process_chapter_questions(
                source_dir, course_root, course_dir, dry_run=False
            )
            
            assert results["summary"]["converted"] == 1
            mock_utils_create.assert_called_with(str(course_root), 2)
