"""Tests for validation module (main.py and utils.py)."""

from src.validation.main import (
    validate_outputs,
    validate_published,
    validate_published_directory,
    generate_validation_report,
    get_output_summary,
    _validate_module_outputs,
    _validate_syllabus_outputs,
)
from src.validation.utils import check_dashboard_invariant, check_lab_files


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

    def test_default_formats_legacy(self, temp_dir):
        """When formats is omitted, only pdf+html are tallied (legacy behavior)."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        for ext in ("pdf", "docx", "md", "html"):
            (output_dir / f"lab-01_intro.{ext}").write_text(f"{ext} content", encoding="utf-8")

        result = check_lab_files(temp_dir)

        assert set(result["formats_checked"]) == {"pdf", "html"}
        assert result["output_files"] == {"pdf": 1, "html": 1}

    def test_formats_aware_counts_pdf_docx_md(self, temp_dir):
        """Format-aware lab counting only tallies currently supported lab formats."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        (output_dir / "lab-01_intro.pdf").write_text("pdf", encoding="utf-8")

        dashboards_dir = labs_dir / "dashboards"
        dashboards_dir.mkdir()

        result = check_lab_files(temp_dir, formats=["pdf", "docx", "md"])

        assert result["formats_checked"] == ["pdf"]
        assert result["formats_skipped"] == ["docx", "md"]
        assert result["output_files"]["pdf"] == 1
        assert result["missing_outputs"] == []

    def test_formats_aware_filters_unsupported(self, temp_dir):
        """Requested formats outside the renderable set (e.g., mp3) are dropped."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        output_dir = labs_dir / "output"
        output_dir.mkdir()
        (output_dir / "lab-01_intro.pdf").write_text("pdf", encoding="utf-8")

        result = check_lab_files(temp_dir, formats=["pdf", "mp3"])

        assert result["formats_checked"] == ["pdf"]
        assert "mp3" not in result["output_files"]

    def test_numbered_vs_supplemental_split(self, temp_dir):
        """Numbered protocols and follow-up labs are counted separately."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        (labs_dir / "lab-02_cells.md").write_text("# Lab 2\n", encoding="utf-8")
        (labs_dir / "lab-14_microbiology-followup.md").write_text("# Follow-up\n", encoding="utf-8")
        (labs_dir / "lab-overview.md").write_text("# Overview\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        (labs_dir / "dashboards").mkdir()

        result = check_lab_files(temp_dir)

        assert result["source_labs"] == 4
        assert result["source_labs_numbered"] == 2
        assert result["source_labs_supplemental"] == 2

    def test_max_lab_keeps_supplemental_in_scope(self, temp_dir):
        """max_lab limits numbered labs but keeps supplementals for in-scope numbers."""
        labs_dir = temp_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")
        (labs_dir / "lab-14_microbiology.md").write_text("# Lab 14\n", encoding="utf-8")
        (labs_dir / "lab-14_microbiology-followup.md").write_text("# Follow-up\n", encoding="utf-8")
        (labs_dir / "lab-18_evolution.md").write_text("# Lab 18\n", encoding="utf-8")

        output_dir = labs_dir / "output"
        output_dir.mkdir()
        (labs_dir / "dashboards").mkdir()

        result = check_lab_files(temp_dir, max_lab=14)

        assert result["source_labs"] == 3
        assert result["source_labs_numbered"] == 2
        assert result["source_labs_supplemental"] == 1


class TestCheckDashboardInvariant:
    """Tests for check_dashboard_invariant strict per-lab check."""

    @staticmethod
    def _scaffold(temp_dir, course_name, labs, dashboards):
        course_dir = temp_dir / course_name
        labs_dir = course_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        for stem in labs:
            (labs_dir / f"{stem}.md").write_text(f"# {stem}\n", encoding="utf-8")
        if dashboards is not None:
            dashboards_dir = labs_dir / "dashboards"
            dashboards_dir.mkdir()
            for stem in dashboards:
                (dashboards_dir / f"{stem}.html").write_text("<html></html>", encoding="utf-8")
        return course_dir

    def test_no_labs_directory(self, temp_dir):
        """Missing labs/ short-circuits to valid (nothing to check)."""
        result = check_dashboard_invariant(temp_dir, course_name="biol-8")

        assert result["valid"] is True
        assert result["per_lab"] == {}
        assert result["issues"] == []

    def test_default_one_per_lab_passes(self, temp_dir):
        """BIOL-1-style default: one dashboard per numbered lab passes."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-1",
            labs=["lab-01_intro", "lab-02_cells"],
            dashboards=[
                "lab-01_intro-dashboard",
                "lab-02_cells-dashboard",
            ],
        )

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is True
        assert set(result["checked_labs"]) == {1, 2}
        assert result["per_lab"][1]["found"] == 1
        assert result["per_lab"][2]["found"] == 1

    def test_biol8_lab15_requires_two_dashboards(self, temp_dir):
        """BIOL-8 Lab 15 override requires exactly two dashboards."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-8",
            labs=[
                "lab-14_microbiology",
                "lab-14_microbiology-followup",
                "lab-15_cardiovascular-system",
            ],
            dashboards=[
                "lab-14_microbiology-dashboard",
                "lab-15_cardiovascular-system-dashboard",
                "lab-15_respiratory-system-dashboard",
            ],
        )

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is True
        assert result["per_lab"][15]["expected"] == 2
        assert result["per_lab"][15]["found"] == 2
        # Follow-up file must not appear as a numbered lab in checked_labs.
        assert 15 in result["checked_labs"]
        assert result["per_lab"][14]["expected"] == 1

    def test_missing_dashboard_flagged(self, temp_dir):
        """Numbered lab with no dashboard surfaces an issue and invalidates."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-1",
            labs=["lab-01_intro", "lab-02_cells"],
            dashboards=["lab-01_intro-dashboard"],
        )

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is False
        assert any("lab-02" in issue for issue in result["issues"])

    def test_lab15_missing_second_dashboard_flagged(self, temp_dir):
        """BIOL-8 Lab 15 with only one dashboard fails the override."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-8",
            labs=["lab-15_cardiovascular-system"],
            dashboards=["lab-15_cardiovascular-system-dashboard"],
        )

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is False
        assert any("lab-15" in issue and "found 1" in issue for issue in result["issues"])

    def test_max_lab_caps_check(self, temp_dir):
        """max_lab limits the strict check to numbered labs ≤ cap."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-1",
            labs=["lab-01_intro", "lab-02_cells", "lab-03_microscopy"],
            dashboards=["lab-01_intro-dashboard"],
        )

        result = check_dashboard_invariant(course_dir, max_lab=1)

        assert result["valid"] is True
        assert result["checked_labs"] == [1]

    def test_missing_dashboards_directory(self, temp_dir):
        """Numbered labs without a dashboards/ dir invalidates strictly."""
        course_dir = temp_dir / "biol-1"
        labs_dir = course_dir / "course" / "labs"
        labs_dir.mkdir(parents=True)
        (labs_dir / "lab-01_intro.md").write_text("# Lab 1\n", encoding="utf-8")

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is False
        assert any("dashboards/ directory not found" in issue for issue in result["issues"])

    def test_supplemental_only_lab_does_not_require_dashboard(self, temp_dir):
        """A lab number that only has a follow-up file is not required to ship a dashboard."""
        course_dir = self._scaffold(
            temp_dir,
            "biol-8",
            labs=["lab-99_thought-experiment-followup"],
            dashboards=[],
        )

        result = check_dashboard_invariant(course_dir)

        assert result["valid"] is True
        assert result["per_lab"] == {}


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


class TestValidateModuleOutputs:
    """Tests for _validate_module_outputs function."""

    def test_module_without_output_dir(self, temp_dir):
        """Module without output directory is invalid."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()

        result = _validate_module_outputs(module_dir)

        assert result["valid"] is False
        assert result["has_output_dir"] is False
        assert "output/" in result["missing_files"]

    def test_module_with_output_dir_but_no_files(self, temp_dir):
        """Module with empty output directory has missing files."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        (module_dir / "output").mkdir()

        result = _validate_module_outputs(module_dir)

        assert result["has_output_dir"] is True
        assert result["name"] == "module-01"

    def test_module_with_complete_study_guides(self, temp_dir):
        """Module with study guides in output directory."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        output_dir = module_dir / "output"
        sg_dir = output_dir / "study-guides"
        sg_dir.mkdir(parents=True)

        # Create study guide files
        for ext in ["pdf", "docx", "mp3", "txt", "html"]:
            (sg_dir / f"study-guide.{ext}").write_text(f"{ext} content", encoding="utf-8")

        result = _validate_module_outputs(module_dir)

        assert result["has_output_dir"] is True
        # Study guides should be checked
        assert "study_guides" in result

    def test_module_with_website_files(self, temp_dir):
        """Module with website files in output directory."""
        module_dir = temp_dir / "module-01"
        module_dir.mkdir()
        output_dir = module_dir / "output"
        website_dir = output_dir / "website"
        website_dir.mkdir(parents=True)

        # Create website files
        (website_dir / "index.html").write_text("<html>", encoding="utf-8")

        result = _validate_module_outputs(module_dir)

        assert result["has_output_dir"] is True
        assert "website" in result

    def test_module_website_skipped_without_html_format(self, temp_dir):
        """Website output is optional unless HTML is explicitly requested."""
        module_dir = temp_dir / "module-01"
        sg_dir = module_dir / "output" / "study-guides"
        sg_dir.mkdir(parents=True)
        for base in ("keys-to-success", "questions"):
            for ext in ("pdf", "docx"):
                (sg_dir / f"module-01-{base}.{ext}").write_text(
                    f"{base} {ext}", encoding="utf-8"
                )

        result = _validate_module_outputs(module_dir, formats=["pdf", "docx"])

        assert result["valid"] is True
        assert result["website"] == {"index.html": "skipped (html not in formats)"}

    def test_module_website_required_with_html_format(self, temp_dir):
        """HTML validation requires website/index.html."""
        module_dir = temp_dir / "module-01"
        sg_dir = module_dir / "output" / "study-guides"
        sg_dir.mkdir(parents=True)
        for base in ("keys-to-success", "questions"):
            for ext in ("pdf", "docx", "html"):
                (sg_dir / f"module-01-{base}.{ext}").write_text(
                    f"{base} {ext}", encoding="utf-8"
                )

        result = _validate_module_outputs(
            module_dir, formats=["pdf", "docx", "html"]
        )

        assert result["valid"] is False
        assert "website/index.html" in result["missing_files"]


class TestValidateSyllabusOutputs:
    """Tests for _validate_syllabus_outputs function."""

    def test_no_syllabus_output_dir(self, temp_dir):
        """No syllabus output directory returns invalid."""
        result = _validate_syllabus_outputs(temp_dir)

        assert result["valid"] is False
        assert "Syllabus output directory not found" in result["issues"]

    def test_empty_syllabus_output_dir(self, temp_dir):
        """Empty syllabus output directory is invalid."""
        syllabus_output = temp_dir / "syllabus" / "output"
        syllabus_output.mkdir(parents=True)

        result = _validate_syllabus_outputs(temp_dir)

        assert result["valid"] is False
        # Should report missing formats
        assert any("pdf" in issue.lower() for issue in result["issues"])

    def test_complete_syllabus_outputs(self, temp_dir):
        """Syllabus with all required formats is valid when those formats requested."""
        syllabus_output = temp_dir / "syllabus" / "output"
        syllabus_output.mkdir(parents=True)

        # Create required format files
        for fmt in ["pdf", "docx", "html", "txt"]:
            (syllabus_output / f"syllabus.{fmt}").write_text(f"{fmt} content", encoding="utf-8")

        # Pass explicit formats to match what we created
        result = _validate_syllabus_outputs(temp_dir, formats=["pdf", "docx", "html", "txt"])

        assert result["valid"] is True
        assert result["files"]["pdf"] == 1
        assert result["files"]["docx"] == 1
        assert result["files"]["html"] == 1
        assert result["files"]["txt"] == 1

    def test_syllabus_missing_one_format(self, temp_dir):
        """Syllabus missing one required format is invalid when that format is requested."""
        syllabus_output = temp_dir / "syllabus" / "output"
        syllabus_output.mkdir(parents=True)

        # Create all but one required format
        for fmt in ["pdf", "docx", "html"]:
            (syllabus_output / f"syllabus.{fmt}").write_text(f"{fmt} content", encoding="utf-8")
        # Missing txt

        # Request txt format so it will report as missing
        result = _validate_syllabus_outputs(temp_dir, formats=["pdf", "docx", "html", "txt"])

        assert result["valid"] is False
        assert any("txt" in issue.lower() for issue in result["issues"])

    def test_syllabus_mp3_optional(self, temp_dir):
        """Syllabus MP3 is optional and doesn't affect validity."""
        syllabus_output = temp_dir / "syllabus" / "output"
        syllabus_output.mkdir(parents=True)

        # Create required format files (no MP3)
        for fmt in ["pdf", "docx", "html", "txt"]:
            (syllabus_output / f"syllabus.{fmt}").write_text(f"{fmt} content", encoding="utf-8")

        # Request all formats including mp3
        result = _validate_syllabus_outputs(temp_dir, formats=["pdf", "docx", "html", "txt", "mp3"])

        assert result["valid"] is True
        assert result["files"]["mp3"] == 0  # Tracked but not required

    def test_syllabus_default_formats(self, temp_dir):
        """Syllabus with default formats (pdf,docx) passes when only those exist."""
        syllabus_output = temp_dir / "syllabus" / "output"
        syllabus_output.mkdir(parents=True)

        # Create only PDF and DOCX (the new defaults)
        for fmt in ["pdf", "docx"]:
            (syllabus_output / f"syllabus.{fmt}").write_text(f"{fmt} content", encoding="utf-8")

        # No formats specified = use default (pdf, docx)
        result = _validate_syllabus_outputs(temp_dir)

        assert result["valid"] is True
        assert result["files"]["pdf"] == 1
        assert result["files"]["docx"] == 1


class TestValidatePublished:
    """Tests for validate_published function."""

    def test_published_dir_not_exists(self, temp_dir):
        """Non-existent published directory returns invalid."""
        result = validate_published(str(temp_dir / "nonexistent"))

        assert result["valid"] is False
        assert "does not exist" in result["issues"][0]

    def test_empty_published_dir(self, temp_dir):
        """Empty published directory reports missing courses."""
        pub_dir = temp_dir / "PUBLISHED"
        pub_dir.mkdir()

        result = validate_published(str(pub_dir))

        # Should report missing courses from config
        assert result["total_files"] == 0
        assert len(result["issues"]) > 0

    def test_published_with_course_files(self, temp_dir):
        """Published directory with course files counts correctly."""
        pub_dir = temp_dir / "PUBLISHED"
        course_dir = pub_dir / "biol-1"
        course_dir.mkdir(parents=True)

        # Create some files
        (course_dir / "file.pdf").write_text("PDF", encoding="utf-8")
        (course_dir / "file.docx").write_text("DOCX", encoding="utf-8")

        result = validate_published(str(pub_dir))

        # Should find the course
        if "biol-1" in result["courses"]:
            assert result["courses"]["biol-1"]["total_files"] == 2

    def test_published_with_module_subdirs(self, temp_dir):
        """Published directory with module subdirectories."""
        pub_dir = temp_dir / "PUBLISHED"
        course_dir = pub_dir / "biol-1"
        module_dir = course_dir / "module-01"
        module_dir.mkdir(parents=True)

        # Create files in module
        (module_dir / "study-guide.pdf").write_text("PDF", encoding="utf-8")
        (module_dir / "study-guide.docx").write_text("DOCX", encoding="utf-8")

        result = validate_published(str(pub_dir))

        # Should find modules
        if "biol-1" in result["courses"]:
            modules = result["courses"]["biol-1"]["modules"]
            assert len(modules) > 0

    def test_validate_published_directory_alias_matches_validate_published(
        self, temp_dir
    ):
        """validate_published_directory is an alias with identical behaviour."""
        pub_dir = temp_dir / "PUBLISHED"
        pub_dir.mkdir()

        direct = validate_published(str(pub_dir))
        aliased = validate_published_directory(str(pub_dir))
        assert aliased["valid"] == direct["valid"]
        assert aliased["path"] == direct["path"]
        assert aliased["total_files"] == direct["total_files"]


class TestGetOutputSummary:
    """Tests for get_output_summary function."""

    def test_empty_course(self, temp_dir):
        """Empty course directory returns empty summary."""
        course_dir = temp_dir / "test-course"
        course_dir.mkdir()
        (course_dir / "course").mkdir()

        result = get_output_summary(str(course_dir))

        assert result["course"] == "test-course"
        assert result["totals"]["modules"] == 0
        assert result["totals"]["files"] == 0

    def test_course_with_modules(self, temp_dir):
        """Course with modules counts outputs correctly."""
        course_dir = temp_dir / "test-course"
        course_dir.mkdir()
        (course_dir / "course").mkdir()

        # Create two modules with outputs
        for i in range(1, 3):
            module_dir = course_dir / "course" / f"module-{i:02d}"
            output_dir = module_dir / "output"
            output_dir.mkdir(parents=True)

            (output_dir / "study-guide.pdf").write_text("PDF", encoding="utf-8")
            (output_dir / "study-guide.docx").write_text("DOCX", encoding="utf-8")

        result = get_output_summary(str(course_dir))

        assert result["totals"]["modules"] == 2
        assert result["totals"]["files"] == 4  # 2 files per module
        assert result["by_format"]["pdf"] == 2
        assert result["by_format"]["docx"] == 2

    def test_course_with_various_formats(self, temp_dir):
        """Course with various output formats."""
        course_dir = temp_dir / "test-course"
        course_dir.mkdir()
        (course_dir / "course").mkdir()

        module_dir = course_dir / "course" / "module-01"
        output_dir = module_dir / "output"
        output_dir.mkdir(parents=True)

        # Create various format files
        for ext in ["pdf", "docx", "html", "mp3", "txt"]:
            (output_dir / f"study-guide.{ext}").write_text(f"{ext}", encoding="utf-8")

        result = get_output_summary(str(course_dir))

        assert result["by_format"]["pdf"] == 1
        assert result["by_format"]["docx"] == 1
        assert result["by_format"]["html"] == 1
        assert result["by_format"]["mp3"] == 1
        assert result["by_format"]["txt"] == 1
        assert result["totals"]["files"] == 5


class TestGenerateValidationReport:
    """Tests for generate_validation_report function."""

    def test_nonexistent_course(self, temp_dir):
        """Report for non-existent course shows errors."""
        # Create minimal structure
        (temp_dir / "course_development").mkdir()
        (temp_dir / "PUBLISHED").mkdir()

        result = generate_validation_report("nonexistent-course", str(temp_dir))

        assert result["course"] == "nonexistent-course"
        assert result["source_validation"]["valid"] is False

    def test_report_structure(self, temp_dir):
        """Report has expected structure."""
        # Create course structure
        course_dir = temp_dir / "course_development" / "test-course"
        course_dir.mkdir(parents=True)
        (course_dir / "course").mkdir()

        # Create published structure
        pub_dir = temp_dir / "PUBLISHED"
        pub_dir.mkdir()

        result = generate_validation_report("test-course", str(temp_dir))

        assert "course" in result
        assert "timestamp" in result
        assert "source_validation" in result
        assert "published_validation" in result
        assert "summary" in result

    def test_report_summary(self, temp_dir):
        """Report summary contains expected fields."""
        course_dir = temp_dir / "course_development" / "test-course"
        course_dir.mkdir(parents=True)
        (course_dir / "course").mkdir()

        pub_dir = temp_dir / "PUBLISHED"
        pub_dir.mkdir()

        result = generate_validation_report("test-course", str(temp_dir))

        summary = result["summary"]
        assert "source_valid" in summary
        assert "source_modules_valid" in summary
        assert "published_valid" in summary
        assert "published_files" in summary
