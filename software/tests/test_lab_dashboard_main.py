"""Tests for the lab_dashboard package (render_dashboard, render_all_dashboards, SPECS)."""

from __future__ import annotations

from pathlib import Path

from src.lab_dashboard.main import (
    SPECS,
    LabDashboardSpec,
    render_all_dashboards,
    render_dashboard,
)


class TestSpecsIntegrity:
    """Structural invariants over the SPECS tuple."""

    def test_numbers_are_unique_and_sequential_from_one(self) -> None:
        numbers = [spec.number for spec in SPECS]
        assert numbers == sorted(numbers)
        assert len(numbers) == len(set(numbers))
        assert numbers[0] == 1
        assert numbers == list(range(1, len(SPECS) + 1))

    def test_slugs_are_unique(self) -> None:
        slugs = [spec.slug for spec in SPECS]
        assert len(slugs) == len(set(slugs))

    def test_filename_format(self) -> None:
        for spec in SPECS:
            assert spec.filename == f"lab-{spec.number:02d}_{spec.slug}-dashboard.html"
            assert spec.filename.startswith("lab-")
            assert spec.filename.endswith("-dashboard.html")

    def test_every_spec_has_three_evidence_and_checkpoints_and_four_terms(self) -> None:
        for spec in SPECS:
            assert len(spec.evidence) == 3
            assert len(spec.checkpoints) == 3
            assert len(spec.terms) == 4


class TestRenderDashboard:
    def test_produces_valid_html_with_all_fields_present(self) -> None:
        spec = SPECS[0]
        html = render_dashboard(spec)
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html
        assert spec.title in html
        assert spec.focus in html
        for term in spec.terms:
            assert term in html
        for checkpoint in spec.checkpoints:
            assert checkpoint in html
        for evidence_label in spec.evidence:
            assert evidence_label in html

    def test_escapes_special_characters_in_spec_fields(self) -> None:
        spec = LabDashboardSpec(
            number=99,
            slug="test-slug",
            title='A <script>alert(1)</script> & "title"',
            module="Module 99",
            focus="Focus with <b>tags</b> & ampersands",
            evidence=("Ev & <1>", "Ev 2", "Ev 3"),
            checkpoints=("Check & <2>", "Check 2", "Check 3"),
            terms=("term & <3>", "term2", "term3", "term4"),
        )
        html = render_dashboard(spec)
        assert "<script>alert(1)</script>" not in html
        assert "&lt;script&gt;" in html
        assert "&amp;" in html
        assert "&quot;" in html


class TestRenderAllDashboards:
    def test_writes_exactly_len_specs_files(self, temp_dir: Path) -> None:
        dashboard_dir = temp_dir / "dashboards"
        written = render_all_dashboards(dashboard_dir)

        assert len(written) == len(SPECS)
        html_files = sorted(dashboard_dir.glob("lab-*-dashboard.html"))
        assert len(html_files) == len(SPECS)
        for spec in SPECS:
            assert (dashboard_dir / spec.filename).exists()

    def test_removes_stale_dashboard_files_on_rerun(self, temp_dir: Path) -> None:
        dashboard_dir = temp_dir / "dashboards"
        dashboard_dir.mkdir(parents=True)
        stale = dashboard_dir / "lab-99_stale-topic-dashboard.html"
        stale.write_text("<html>stale</html>", encoding="utf-8")

        render_all_dashboards(dashboard_dir)

        assert not stale.exists()
        assert len(list(dashboard_dir.glob("lab-*-dashboard.html"))) == len(SPECS)

    def test_dry_run_returns_paths_without_writing_to_disk(self, temp_dir: Path) -> None:
        dashboard_dir = temp_dir / "dashboards"

        written = render_all_dashboards(dashboard_dir, dry_run=True)

        assert len(written) == len(SPECS)
        assert not dashboard_dir.exists()

    def test_dry_run_returns_same_path_list_as_real_run(self, temp_dir: Path) -> None:
        dashboard_dir = temp_dir / "dashboards"

        dry_paths = render_all_dashboards(dashboard_dir, dry_run=True)
        real_paths = render_all_dashboards(dashboard_dir, dry_run=False)

        assert dry_paths == real_paths
