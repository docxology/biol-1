"""Edge-case tests for v0.1.3 coverage push.

Covers:
- module_organization: zero-module course, non-sequential module numbers
- html_website: quiz matching question rendering and validation logic
- format_conversion: conversion error paths
- schedule: batch processing with malformed Markdown
"""

import json
from pathlib import Path

import pytest

from src.format_conversion.main import convert_file
from src.html_website.main import generate_module_website
from src.module_organization.main import (
    create_module_structure,
    get_module_statistics,
    list_course_modules,
)
from src.module_organization.utils import get_next_module_number, list_all_modules
from src.schedule.main import parse_schedule_markdown


class TestModuleOrganizationEdgeCases:
    """Edge cases for module_organization: zero-module, non-sequential."""

    def test_zero_module_course(self, temp_dir):
        """list_course_modules and get_next_module_number on empty course."""
        course_dir = temp_dir / "biol-test"
        course_dir.mkdir()
        (course_dir / "course").mkdir()

        modules = list_course_modules(str(course_dir))
        assert modules == []

        all_mods = list_all_modules(course_dir / "course")
        assert all_mods == []

        next_num = get_next_module_number(course_dir / "course")
        assert next_num == 1

    def test_non_sequential_module_numbers(self, temp_dir):
        """Modules with gaps in numbering (e.g., 1, 3, 5)."""
        course_dir = temp_dir / "biol-test"
        course_dir.mkdir()
        course_subdir = course_dir / "course"
        course_subdir.mkdir()

        # Create modules 1, 3, 5 (non-sequential)
        for num in [1, 3, 5]:
            mod_dir = course_subdir / f"module-{num}"
            mod_dir.mkdir()
            (mod_dir / "README.md").write_text(f"# Module {num}\n", encoding="utf-8")
            (mod_dir / "AGENTS.md").write_text(f"# Module {num} Tech\n", encoding="utf-8")

        modules = list_course_modules(str(course_dir))
        assert len(modules) == 3

        all_mods = list_all_modules(course_dir)
        assert len(all_mods) == 3

        # Next module should be 6 (max + 1)
        next_num = get_next_module_number(course_dir)
        assert next_num == 6

    def test_create_module_in_course_with_non_sequential(self, temp_dir):
        """create_module_structure works after a gap."""
        course_dir = temp_dir / "biol-test"
        course_dir.mkdir()
        course_subdir = course_dir / "course"
        course_subdir.mkdir()

        # Create module 1
        mod1 = create_module_structure(str(course_dir), 1)
        assert Path(mod1).exists()

        # Create module 5 (skip 2-4)
        mod5 = create_module_structure(str(course_dir), 5)
        assert Path(mod5).exists()
        assert "module-5" in mod5

        # Statistics on module 5 should work
        stats = get_module_statistics(mod5)
        assert stats["module_number"] == 5
        assert stats["has_readme"] is True

    def test_statistics_on_module_without_number(self, temp_dir):
        """get_module_statistics on a directory with no module number in name."""
        mod_dir = temp_dir / "random-folder"
        mod_dir.mkdir()
        (mod_dir / "README.md").write_text("# Random\n", encoding="utf-8")

        stats = get_module_statistics(str(mod_dir))
        assert stats["module_number"] is None
        assert stats["has_readme"] is True


class TestHTMLWebsiteQuizMatching:
    """Test matching question rendering and validation in generated websites."""

    def test_matching_question_renders_correct_match_hidden_inputs(self, temp_dir):
        """Matching questions generate hidden correct-match-{qid}-{i} inputs."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        questions_dir = module_dir / "questions"
        questions_dir.mkdir()
        questions_data = {
            "questions": [
                {
                    "id": "q1",
                    "type": "matching",
                    "question": "Match terms to definitions",
                    "items": [
                        {"term": "Cell", "definition": "Basic unit of life"},
                        {"term": "DNA", "definition": "Genetic material"},
                        {"term": "Enzyme", "definition": "Biological catalyst"},
                    ],
                }
            ]
        }
        (questions_dir / "questions.json").write_text(json.dumps(questions_data), encoding="utf-8")

        output_dir = temp_dir / "output"
        result = generate_module_website(str(module_dir), str(output_dir))
        html_content = Path(result).read_text()

        # Hidden correct-match inputs should exist for each item
        assert 'id="correct-match-q1-0"' in html_content
        assert 'id="correct-match-q1-1"' in html_content
        assert 'id="correct-match-q1-2"' in html_content

        # Matching select dropdowns should exist
        assert "matching-select" in html_content
        assert "Select definition..." in html_content

    def test_matching_question_js_validates_answers(self, temp_dir):
        """The inline JS includes matching validation logic (not just 'isCorrect = true')."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        questions_dir = module_dir / "questions"
        questions_dir.mkdir()
        questions_data = {
            "questions": [
                {
                    "id": "q1",
                    "type": "matching",
                    "question": "Match terms to definitions",
                    "items": [
                        {"term": "A", "definition": "Alpha"},
                        {"term": "B", "definition": "Beta"},
                    ],
                }
            ]
        }
        (questions_dir / "questions.json").write_text(json.dumps(questions_data), encoding="utf-8")

        output_dir = temp_dir / "output"
        result = generate_module_website(str(module_dir), str(output_dir))
        html_content = Path(result).read_text()

        # The matching validation should check against correct-match values
        # (not just set isCorrect = true unconditionally)
        assert "correct-match-" in html_content
        # The old placeholder comment should be gone
        assert "Placeholder for complex matching" not in html_content

    def test_module_script_js_has_matching_validation(self):
        """The standalone module_script.js file has matching validation."""
        js_path = (
            Path(__file__).resolve().parent.parent / "src" / "html_website" / "module_script.js"
        )
        js_content = js_path.read_text()

        # The old TODO should be gone
        assert "TODO: implement matching question type validation" not in js_content
        # New validation logic should be present
        assert "correct-match-" in js_content
        assert "Please match all pairs first." in js_content


class TestFormatConversionErrorPaths:
    """Test format_conversion error handling."""

    def test_convert_file_nonexistent_input(self, temp_dir):
        """convert_file raises FileNotFoundError for missing input."""
        output_path = temp_dir / "output.html"
        with pytest.raises(FileNotFoundError):
            convert_file(str(temp_dir / "nonexistent.md"), "html", str(output_path))

    def test_convert_file_unsupported_format(self, temp_dir):
        """convert_file with an unsupported format raises ValueError or OSError."""
        input_file = temp_dir / "input.md"
        input_file.write_text("# Test\n", encoding="utf-8")
        output_path = temp_dir / "output.xyz"
        with pytest.raises((ValueError, OSError)):
            convert_file(str(input_file), "xyz", str(output_path))

    def test_convert_file_empty_markdown(self, temp_dir):
        """convert_file handles empty markdown gracefully: it succeeds and
        produces a well-formed (if content-empty) HTML document, it does
        not raise."""
        input_file = temp_dir / "empty.md"
        input_file.write_text("", encoding="utf-8")
        output_path = temp_dir / "output.html"

        convert_file(str(input_file), "html", str(output_path))

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "<html>" in content
        assert "<title>empty</title>" in content


class TestScheduleMalformedMarkdown:
    """Test schedule parsing with malformed input."""

    def test_parse_empty_markdown(self, temp_dir):
        """parse_schedule_markdown handles empty file."""
        empty_schedule = temp_dir / "empty.md"
        empty_schedule.write_text("", encoding="utf-8")

        result = parse_schedule_markdown(str(empty_schedule))
        # Should return a dict, not crash
        assert isinstance(result, dict)

    def test_parse_markdown_no_table(self, temp_dir):
        """parse_schedule_markdown with no table content."""
        no_table = temp_dir / "no_table.md"
        no_table.write_text("# Schedule\n\nNo table here, just text.\n", encoding="utf-8")

        result = parse_schedule_markdown(str(no_table))
        assert isinstance(result, dict)

    def test_parse_markdown_malformed_table(self, temp_dir):
        """parse_schedule_markdown with a broken table structure."""
        malformed = temp_dir / "malformed.md"
        malformed.write_text(
            "# Schedule\n\n"
            "| Week | Date |\n"
            "|------|------|\n"
            "| 1 | 9/1 |\n"
            "\n"
            "Some text in the middle.\n"
            "| 2 |\n"  # Incomplete row
            "\n"
            "| 3 | 9/15 | Extra | col |\n",  # Extra columns
            encoding="utf-8",
        )

        result = parse_schedule_markdown(str(malformed))
        assert isinstance(result, dict)

    def test_parse_markdown_missing_file(self, temp_dir):
        """parse_schedule_markdown raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            parse_schedule_markdown(str(temp_dir / "nonexistent.md"))


class TestRepoContractsLinkSkipping:
    """Test that repo_contracts skips links to generated output directories."""

    def test_output_links_are_skipped(self):
        """Links to output/ directories should not be checked by _should_check_link."""
        from src.validation.repo_contracts import _should_check_link

        # Links to generated output should be skipped
        assert _should_check_link("output/file.pdf") is False
        assert _should_check_link("course/labs/output/pdf/lab-01.pdf") is False
        assert _should_check_link("syllabus/output/Schedule.pdf") is False
        assert _should_check_link("syllabus/output/Schedule.docx") is False

        # Normal links should still be checked
        assert _should_check_link("README.md") is True
        assert _should_check_link("course/labs/lab-01_measurement-methods.md") is True
        assert _should_check_link("syllabus/Schedule.md") is True

    def test_repo_contracts_passes_on_fresh_clone(self):
        """Repo contracts validation passes even without generated outputs."""
        repo_root = Path(__file__).resolve().parents[2]
        from src.validation.repo_contracts import validate_repo_contracts

        report = validate_repo_contracts(repo_root)
        # Should not have issues about missing output/ link targets
        output_issues = [i for i in report.issues if "output/" in i and "missing link target" in i]
        assert len(output_issues) == 0, "Output links should be skipped: " + "\n".join(
            output_issues
        )
