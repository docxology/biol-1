"""Tests for legacy import utility functions."""

from pathlib import Path
from unittest.mock import patch
import pytest

from src.legacy_import.utils import (
    extract_chapter_number,
    ensure_module_exists,
    create_comprehension_questions,
    create_questions_directory,
)


class TestExtractChapterNumber:
    """Tests for extract_chapter_number function."""

    def test_valid_patterns(self):
        """Test valid chapter filename patterns."""
        assert extract_chapter_number("Chapter 1 Keys.docx") == 1
        assert extract_chapter_number("Chapter 01 Keys.docx") == 1
        assert extract_chapter_number("General Biology Chapter 05 Slides.pdf") == 5
        assert extract_chapter_number("Chapter 10 Review.md") == 10

    def test_invalid_patterns(self):
        """Test invalid filename patterns raise ValueError."""
        with pytest.raises(ValueError, match="Could not extract"):
            extract_chapter_number("No Number Here.docx")
        
        with pytest.raises(ValueError):
            extract_chapter_number("Module 01.docx")


class TestEnsureModuleExists:
    """Tests for ensure_module_exists function."""

    @pytest.fixture
    def mock_create(self):
        with patch("src.legacy_import.utils.create_module_structure") as mock:
            mock.return_value = Path("/mock/module-01")
            yield mock

    @pytest.fixture
    def mock_get_path(self):
        with patch("src.module_organization.utils.get_module_path") as mock:
            yield mock

    def test_module_already_exists(self, temp_dir, mock_get_path, mock_create):
        """Test existing module returns path without creation."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()
        mock_get_path.return_value = module_path

        result = ensure_module_exists(temp_dir, 1, dry_run=False)

        assert result == module_path
        mock_create.assert_not_called()

    def test_create_new_module(self, temp_dir, mock_get_path, mock_create):
        """Test creating new module."""
        module_path = temp_dir / "module-02"
        mock_get_path.return_value = module_path  # it doesn't exist yet

        ensure_module_exists(temp_dir, 2, dry_run=False)

        mock_create.assert_called_once_with(str(temp_dir), 2)

    def test_dry_run_skips_creation(self, temp_dir, mock_get_path, mock_create):
        """Test dry run skips creation."""
        module_path = temp_dir / "module-03"
        mock_get_path.return_value = module_path

        ensure_module_exists(temp_dir, 3, dry_run=True)

        mock_create.assert_not_called()

    def test_skip_already_exists_error(self, temp_dir, mock_get_path, mock_create):
        """Test handling of concurrent creation race condition."""
        module_path = temp_dir / "module-04"
        mock_get_path.return_value = module_path
        
        # Simulate race condition where it exists when create_module_structure runs
        mock_create.side_effect = ValueError("Directory already exists")

        ensure_module_exists(temp_dir, 4, dry_run=False)
        # Should catch error and log debug, not propagate
        mock_create.assert_called_once()


class TestCreateComprehensionQuestions:
    """Tests for create_comprehension_questions function."""

    def test_create_file(self, temp_dir):
        """Test file creation with correct content."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()

        create_comprehension_questions(module_path, 1, dry_run=False)

        file_path = module_path / "resources" / "comprehension-questions.md"
        assert file_path.exists()
        content = file_path.read_text("utf-8")
        assert "# Comprehension Questions - Module 1" in content

    def test_dry_run(self, temp_dir):
        """Test dry run does not create file."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()

        create_comprehension_questions(module_path, 1, dry_run=True)

        file_path = module_path / "resources" / "comprehension-questions.md"
        assert not file_path.exists()

    def test_skip_existing(self, temp_dir):
        """Test skips if file already exists."""
        module_path = temp_dir / "module-01"
        (module_path / "resources").mkdir(parents=True)
        file_path = module_path / "resources" / "comprehension-questions.md"
        file_path.write_text("Old content")

        create_comprehension_questions(module_path, 1, dry_run=False)

        assert file_path.read_text() == "Old content"


class TestCreateQuestionsDirectory:
    """Tests for create_questions_directory function."""

    def test_create_full_structure(self, temp_dir):
        """Test creating directory and all files."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()

        create_questions_directory(module_path, 1, dry_run=False)

        q_dir = module_path / "questions"
        assert q_dir.exists()
        assert (q_dir / "questions.json").exists()
        assert (q_dir / "README.md").exists()
        assert (q_dir / "AGENTS.md").exists()

        json_content = (q_dir / "questions.json").read_text("utf-8")
        assert '"questions": []' in json_content

    def test_dry_run(self, temp_dir):
        """Test dry run creates nothing."""
        module_path = temp_dir / "module-01"
        module_path.mkdir()

        create_questions_directory(module_path, 1, dry_run=True)

        q_dir = module_path / "questions"
        assert not q_dir.exists()

    def test_skip_existing_files(self, temp_dir):
        """Test skips overwriting existing files."""
        module_path = temp_dir / "module-01"
        q_dir = module_path / "questions"
        q_dir.mkdir(parents=True)
        (q_dir / "questions.json").write_text("old json")

        create_questions_directory(module_path, 1, dry_run=False)

        assert (q_dir / "questions.json").read_text() == "old json"
        # Others should still be created
        assert (q_dir / "README.md").exists()
