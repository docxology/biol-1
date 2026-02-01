"""Tests for validation module (main.py and utils.py)."""

from src.validation.main import validate_outputs
from src.validation.utils import check_lab_files


class TestCheckLabFiles:
    """Tests for check_lab_files function."""

    def test_no_labs_directory(self, temp_dir):
        """No labs directory returns empty result."""
        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 0
        assert result["output_files"] == {}
        assert result["dashboards"] == 0
        assert result["missing_outputs"] == []
        assert result["issues"] == []

    def test_labs_dir_no_output_dir(self, temp_dir):
        """Labs dir exists but no output dir populates issues."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 1
        assert "Lab output directory not found" in result["issues"]

    def test_flat_output_files(self, temp_dir):
        """Labs dir with flat output files (existing structure) counts correctly."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        (labs_dir / "lab-02_cells.md").write_text("# Lab 2\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        (output_dir / "lab-01_intro.pdf").write_text("PDF content", encoding="utf-8")
        (output_dir / "lab-02_cells.pdf").write_text("PDF content", encoding="utf-8")
        (output_dir / "lab-01_intro.html").write_text("<html>", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 2
        assert result["output_files"]["pdf"] == 2
        assert result["output_files"]["html"] == 1
        assert result["missing_outputs"] == []

    def test_subdirectory_output_files(self, temp_dir):
        """Labs dir with subdirectory output files (new structure) counts correctly."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        pdf_dir = output_dir / "pdf"
        html_dir = output_dir / "html"
        pdf_dir.mkdir(parents=True)
        html_dir.mkdir(parents=True)
        (pdf_dir / "lab-01_intro.pdf").write_text("PDF content", encoding="utf-8")
        (html_dir / "lab-01_intro.html").write_text("<html>", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 1
        assert result["output_files"]["pdf"] == 1
        assert result["output_files"]["html"] == 1
        assert result["missing_outputs"] == []

    def test_source_lab_missing_rendered_output(self, temp_dir):
        """Source lab missing rendered output appears in missing_outputs."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        (labs_dir / "lab-02_cells.md").write_text("# Lab 2\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        # Only lab-01 has output, lab-02 does not
        (output_dir / "lab-01_intro.pdf").write_text("PDF content", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 2
        assert "lab-02_cells" in result["missing_outputs"]
        assert "lab-01_intro" not in result["missing_outputs"]

    def test_empty_output_file_treated_as_missing(self, temp_dir):
        """Empty (0-byte) output file is treated as missing."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        # Create 0-byte file
        (output_dir / "lab-01_intro.pdf").write_text("", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert "lab-01_intro" in result["missing_outputs"]

    def test_dashboard_counting(self, temp_dir):
        """Dashboards are counted correctly."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        dashboards_dir = labs_dir / "dashboards"
        dashboards_dir.mkdir()
        (dashboards_dir / "lab-01_dashboard.html").write_text("<html>", encoding="utf-8")
        (dashboards_dir / "lab-02_dashboard.html").write_text("<html>", encoding="utf-8")

        # Need output dir to avoid that issue
        output_dir = labs_dir / "output"
        output_dir.mkdir()

        result = check_lab_files(temp_dir)

        assert result["dashboards"] == 2

    def test_no_dashboards_dir(self, temp_dir):
        """No dashboards directory adds issue when source labs exist."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()

        result = check_lab_files(temp_dir)

        assert "Dashboards directory not found" in result["issues"]


class TestValidateOutputsWithLabs:
    """Tests for validate_outputs integration with lab validation."""

    def test_lab_results_included(self, temp_dir):
        """Lab results are included in validate_outputs return."""
        course_dir = temp_dir / "biol-test"
        course_dir.mkdir()
        (course_dir / "course").mkdir()

        result = validate_outputs(str(course_dir))

        assert "labs" in result

    def test_lab_issues_merged(self, temp_dir):
        """Lab issues are merged into top-level issues."""
        course_dir = temp_dir / "biol-test"
        labs_dir = course_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        # No output dir, no dashboards dir — should produce issues

        result = validate_outputs(str(course_dir))

        lab_issues = [i for i in result["issues"] if "Lab" in i or "lab" in i.lower() or "Dashboard" in i or "dashboard" in i.lower()]
        assert len(lab_issues) > 0

    def test_lab_missing_outputs_reported(self, temp_dir):
        """Lab missing outputs reported as issues."""
        course_dir = temp_dir / "biol-test"
        labs_dir = course_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        # lab-01 has no rendered output

        dashboards_dir = labs_dir / "dashboards"
        dashboards_dir.mkdir()

        result = validate_outputs(str(course_dir))

        missing_issues = [i for i in result["issues"] if "missing rendered output" in i.lower()]
        assert len(missing_issues) == 1
        assert "lab-01_intro" in missing_issues[0]
