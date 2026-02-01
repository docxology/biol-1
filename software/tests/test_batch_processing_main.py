"""Comprehensive tests for batch processing main module."""

from pathlib import Path
import pytest

from src.batch_processing.main import (
    clear_all_outputs,
    generate_module_media,
    process_module_by_type,
    process_module_to_audio,
    process_module_to_pdf,
    process_module_to_text,
    process_module_website,
    process_syllabus,
)


class TestProcessModuleToPdf:
    """Tests for process_module_to_pdf function."""

    def test_process_module_to_pdf_success(self, sample_module_structure):
        """Test converting module markdown to PDFs."""
        output_dir = sample_module_structure.parent / "pdf_output"
        
        result = process_module_to_pdf(str(sample_module_structure), str(output_dir))
        
        assert isinstance(result, list)
        # PDFs should be generated for markdown files
        assert all(f.endswith(".pdf") for f in result)

    def test_process_module_to_pdf_nonexistent(self, temp_dir):
        """Test processing non-existent module raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            process_module_to_pdf(str(temp_dir / "nonexistent"), str(temp_dir / "output"))

    def test_process_module_to_pdf_empty_module(self, temp_dir):
        """Test processing empty module returns empty list."""
        empty_module = temp_dir / "empty_module"
        empty_module.mkdir()
        output_dir = temp_dir / "output"
        
        result = process_module_to_pdf(str(empty_module), str(output_dir))
        
        assert result == []


class TestProcessModuleToAudio:
    """Tests for process_module_to_audio function."""

    @pytest.mark.requires_internet
    def test_process_module_to_audio_success(self, sample_module_structure):
        """Test converting module text to audio (requires internet for gTTS)."""
        output_dir = sample_module_structure.parent / "audio_output"
        
        result = process_module_to_audio(str(sample_module_structure), str(output_dir))
        
        assert isinstance(result, list)
        assert all(f.endswith(".mp3") for f in result)

    def test_process_module_to_audio_nonexistent(self, temp_dir):
        """Test processing non-existent module raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            process_module_to_audio(str(temp_dir / "nonexistent"), str(temp_dir / "output"))


class TestProcessModuleToText:
    """Tests for process_module_to_text function."""

    def test_process_module_to_text_nonexistent(self, temp_dir):
        """Test processing non-existent module raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            process_module_to_text(str(temp_dir / "nonexistent"), str(temp_dir / "output"))

    def test_process_module_to_text_no_audio(self, temp_dir):
        """Test processing module with no audio files."""
        module_dir = temp_dir / "module"
        module_dir.mkdir()
        output_dir = temp_dir / "output"
        
        result = process_module_to_text(str(module_dir), str(output_dir))
        
        assert result == []


class TestGenerateModuleMedia:
    """Tests for generate_module_media function."""

    def test_generate_module_media_structure(self, sample_module_structure):
        """Test that generate_module_media returns correct structure."""
        output_dir = sample_module_structure.parent / "media_output"
        
        result = generate_module_media(str(sample_module_structure), str(output_dir))
        
        assert "pdf_files" in result
        assert "audio_files" in result
        assert "text_files" in result
        assert "errors" in result

    def test_generate_module_media_nonexistent(self, temp_dir):
        """Test generating media for non-existent module raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            generate_module_media(str(temp_dir / "nonexistent"), str(temp_dir / "output"))


class TestProcessModuleByType:
    """Tests for process_module_by_type function."""

    def test_process_module_by_type_structure(self, sample_module_structure):
        """Test that process_module_by_type returns correct structure."""
        output_dir = sample_module_structure.parent / "typed_output"
        
        result = process_module_by_type(str(sample_module_structure), str(output_dir))
        
        assert "by_type" in result
        assert "summary" in result
        assert "errors" in result
        assert "assignments" in result["by_type"]
        assert "lecture-content" in result["by_type"]

    def test_process_module_by_type_nonexistent(self, temp_dir):
        """Test processing non-existent module raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            process_module_by_type(str(temp_dir / "nonexistent"), str(temp_dir / "output"))

    def test_process_module_by_type_with_assignments(self, temp_dir):
        """Test processing module with assignments directory."""
        module_dir = temp_dir / "module"
        module_dir.mkdir()
        assignments_dir = module_dir / "assignments"
        assignments_dir.mkdir()
        (assignments_dir / "assignment-1.md").write_text("# Assignment 1\n\nContent", encoding="utf-8")
        
        output_dir = temp_dir / "output"
        result = process_module_by_type(str(module_dir), str(output_dir))
        
        assert "by_type" in result
        assert "errors" in result

    def test_process_module_by_type_curriculum_types(self, temp_dir):
        """Test processing module with various curriculum types."""
        module_dir = temp_dir / "module"
        module_dir.mkdir()
        
        # Create sample files for each type
        (module_dir / "sample_lecture-content.md").write_text("# Lecture\n\nContent", encoding="utf-8")
        (module_dir / "sample_study-guide.md").write_text("# Study Guide\n\nContent", encoding="utf-8")
        (module_dir / "sample_lab-protocol.md").write_text("# Lab Protocol\n\nContent", encoding="utf-8")
        (module_dir / "sample_assignment.md").write_text("# Assignment\n\nContent", encoding="utf-8")
        
        output_dir = temp_dir / "output"
        result = process_module_by_type(str(module_dir), str(output_dir))
        
        # Should have processed multiple types
        total = sum(result["summary"].values())
        assert total > 0


class TestProcessSyllabus:
    """Tests for process_syllabus function."""

    def test_process_syllabus_structure(self, temp_dir):
        """Test that process_syllabus returns correct structure."""
        syllabus_dir = temp_dir / "syllabus"
        syllabus_dir.mkdir()
        (syllabus_dir / "Syllabus.md").write_text("# Syllabus\n\nCourse overview", encoding="utf-8")
        
        output_dir = temp_dir / "output"
        result = process_syllabus(str(syllabus_dir), str(output_dir))
        
        assert "by_format" in result
        assert "summary" in result
        assert "errors" in result

    def test_process_syllabus_nonexistent(self, temp_dir):
        """Test processing non-existent syllabus raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            process_syllabus(str(temp_dir / "nonexistent"), str(temp_dir / "output"))

    def test_process_syllabus_skips_readme(self, temp_dir):
        """Test that README and AGENTS files are skipped."""
        syllabus_dir = temp_dir / "syllabus"
        syllabus_dir.mkdir()
        (syllabus_dir / "README.md").write_text("# README", encoding="utf-8")
        (syllabus_dir / "AGENTS.md").write_text("# AGENTS", encoding="utf-8")
        (syllabus_dir / "Syllabus.md").write_text("# Syllabus", encoding="utf-8")
        
        output_dir = temp_dir / "output"
        result = process_syllabus(str(syllabus_dir), str(output_dir))
        
        # Only Syllabus.md should be processed
        assert result["summary"]["pdf"] <= 1


class TestClearAllOutputs:
    """Tests for clear_all_outputs function."""

    def test_clear_all_outputs_structure(self, temp_dir):
        """Test that clear_all_outputs returns correct structure."""
        result = clear_all_outputs(temp_dir)
        
        assert "cleared_directories" in result
        assert "total_files_removed" in result
        assert "errors" in result

    def test_clear_all_outputs_clears_files(self, temp_dir):
        """Test that clear_all_outputs removes files."""
        # Create a mock course structure
        course_dir = temp_dir / "biol-1" / "course" / "module-1" / "output"
        course_dir.mkdir(parents=True)
        (course_dir / "test.pdf").write_text("test", encoding="utf-8")
        
        result = clear_all_outputs(temp_dir)
        
        # Should have cleared the output directory
        assert result["total_files_removed"] >= 1 or len(result["cleared_directories"]) >= 1

    def test_clear_all_outputs_no_courses(self, temp_dir):
        """Test clear_all_outputs with no course directories."""
        result = clear_all_outputs(temp_dir)
        
        assert result["cleared_directories"] == []
        assert result["errors"] == []


class TestProcessModuleByTypeFormats:
    """Tests for process_module_by_type formats parameter."""

    def test_formats_none_generates_all(self, temp_dir):
        """formats=None generates all formats (default behavior)."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        (module_dir / "keys-to-success.md").write_text(
            "# Keys to Success\n\nStudy hard.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_module_by_type(str(module_dir), str(output_dir), formats=None)

        assert "summary" in result
        # All format keys should exist in summary
        for fmt in ["pdf", "mp3", "docx", "html", "txt"]:
            assert fmt in result["summary"]

    def test_formats_txt_only(self, temp_dir):
        """formats=["txt"] only generates TXT, skips others."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        (module_dir / "keys-to-success.md").write_text(
            "# Keys to Success\n\nStudy hard.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_module_by_type(str(module_dir), str(output_dir), formats=["txt"])

        assert result["summary"]["txt"] >= 1
        assert result["summary"]["pdf"] == 0
        assert result["summary"]["mp3"] == 0
        assert result["summary"]["docx"] == 0
        assert result["summary"]["html"] == 0

    def test_formats_unrecognized_ignored(self, temp_dir):
        """Unrecognized format in list is silently ignored."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        (module_dir / "keys-to-success.md").write_text(
            "# Keys to Success\n\nStudy hard.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_module_by_type(
            str(module_dir), str(output_dir), formats=["txt", "xyz"]
        )

        # TXT should have outputs, xyz does nothing
        assert result["summary"]["txt"] >= 1
        # Standard formats not requested should be zero
        assert result["summary"]["pdf"] == 0
        assert result["summary"]["mp3"] == 0
        assert result["summary"]["docx"] == 0
        assert result["summary"]["html"] == 0

    def test_formats_empty_list(self, temp_dir):
        """formats=[] generates nothing."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        (module_dir / "keys-to-success.md").write_text(
            "# Keys to Success\n\nStudy hard.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_module_by_type(str(module_dir), str(output_dir), formats=[])

        assert sum(result["summary"].values()) == 0


class TestProcessSyllabusFormats:
    """Tests for process_syllabus formats parameter."""

    def test_syllabus_formats_none(self, temp_dir):
        """formats=None generates all formats."""
        syllabus_dir = temp_dir / "syllabus"
        syllabus_dir.mkdir()
        (syllabus_dir / "Syllabus.md").write_text(
            "# Syllabus\n\nCourse overview.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_syllabus(str(syllabus_dir), str(output_dir), formats=None)

        assert "summary" in result
        for fmt in ["pdf", "mp3", "docx", "html", "txt"]:
            assert fmt in result["summary"]

    def test_syllabus_formats_txt_only(self, temp_dir):
        """formats=["txt"] only generates TXT."""
        syllabus_dir = temp_dir / "syllabus"
        syllabus_dir.mkdir()
        (syllabus_dir / "Syllabus.md").write_text(
            "# Syllabus\n\nCourse overview.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = process_syllabus(str(syllabus_dir), str(output_dir), formats=["txt"])

        assert result["summary"]["txt"] >= 1
        assert result["summary"]["pdf"] == 0
        assert result["summary"]["mp3"] == 0
        assert result["summary"]["docx"] == 0
        assert result["summary"]["html"] == 0


class TestProcessModuleWebsite:
    """Tests for process_module_website function."""

    def test_process_module_website_success(self, temp_dir):
        """Test generating module website."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()
        
        output_dir = temp_dir / "output" / "website"
        result = process_module_website(str(module_dir), str(output_dir))
        
        assert result.endswith("index.html")
        assert Path(result).exists()

    def test_process_module_website_default_output(self, temp_dir):
        """Test generating module website with default output."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()
        
        result = process_module_website(str(module_dir))
        
        assert "output/website/index.html" in result
