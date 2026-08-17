"""Tests for the canonical BIOL-1 course-by-date projection."""

import datetime as dt
import json
from pathlib import Path

import pytest

from src.course_by_date import (
    CourseCalendar,
    GeneratedCalendarError,
    MaterialSpec,
    Meeting,
    generate_course_by_date,
    load_calendar,
    validate_generated_course_by_date,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_biol1_calendar_matches_fall_2026_schedule():
    """The structured map contains every scheduled Fall 2026 meeting."""
    root = _repo_root()
    course_root = root / "course_development" / "biol-1"
    calendar = load_calendar(course_root / "course_calendar.toml")

    calendar.validate(course_root)
    assert len(calendar.meetings) == 33
    assert calendar.meetings[0].date == dt.date(2026, 8, 25)
    assert calendar.meetings[-1].date == dt.date(2026, 12, 15)
    assert sum(meeting.status == "no-class" for meeting in calendar.meetings) == 2
    assert sum(meeting.status == "holiday" for meeting in calendar.meetings) == 0
    assert calendar.textbook_planned
    assert calendar.textbook_used == calendar.textbook_planned


def test_generated_biol1_calendar_has_provenance_and_delivery_outputs():
    """Every generated date folder validates against its source map."""
    root = _repo_root()
    course_root = root / "course_development" / "biol-1"
    calendar = load_calendar(course_root / "course_calendar.toml")

    report = validate_generated_course_by_date(course_root, calendar)

    assert report["meetings"] == 33
    assert report["copied_outputs"] > 150
    assert len(list((course_root / "course" / "course_by_date").glob("*/meeting.json"))) == 33
    date_root = course_root / "course" / "course_by_date" / "2026-08-25"
    assert {path.name for path in date_root.iterdir() if path.is_dir()} == {"materials"}
    materials = list((date_root / "materials").iterdir())
    assert {path.suffix for path in materials} >= {".pdf", ".docx", ".mp4"}
    assert any(path.name.endswith("-key-points.pdf") for path in materials)
    assert any(path.name.endswith("-practice-quiz.docx") for path in materials)
    assert any(path.name.endswith("-questions.pdf") for path in materials)
    assert all(path.suffix.lower() not in {".md", ".json"} for path in materials)
    assert all(path.suffix.lower() not in {".srt", ".vtt"} for path in materials)
    assert all(path.suffix.lower() != ".html" for path in materials)


def test_generator_copies_only_used_materials(temp_dir):
    """Planned-but-unused records remain metadata and are not copied."""
    course_root = temp_dir / "course_development" / "biol-1"
    module_dir = course_root / "course" / "module-01-demo"
    module_dir.mkdir(parents=True)
    for name in ("README.md", "questions.md", "key-points.md", "practice-quiz.md"):
        (module_dir / name).write_text(f"# {name}\n", encoding="utf-8")
    generated_dir = module_dir / "output" / "study-guides"
    generated_dir.mkdir(parents=True)
    (generated_dir / "module-01-demo-key-points.pdf").write_bytes(b"pdf")
    (generated_dir / "module-01-demo-key-points.docx").write_bytes(b"docx")
    (generated_dir / "metadata.json").write_text("{}", encoding="utf-8")
    calendar = CourseCalendar(
        course="biol-1",
        term="Test",
        timezone="UTC",
        source_schedule="test",
        meetings=(
            Meeting(
                date=dt.date(2026, 1, 5),
                week=1,
                day="Mon",
                status="class",
                title="Demo",
                notes="",
                materials=(
                    MaterialSpec("module", "module-01-demo", True, True, ("source", "generated")),
                    MaterialSpec("textbook", "unassigned", False, False),
                ),
            ),
        ),
    )

    result = generate_course_by_date(course_root, calendar)

    assert result["files"] == 2
    metadata = json.loads(
        (course_root / "course" / "course_by_date" / "2026-01-05" / "meeting.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(metadata["copied_outputs"]) == 2
    assert not list((course_root / "course" / "course_by_date").rglob("*textbook*"))


def test_generated_calendar_rejects_tampered_copy():
    """Checksum validation fails closed when a copied output changes."""
    root = _repo_root()
    course_root = root / "course_development" / "biol-1"
    calendar = load_calendar(course_root / "course_calendar.toml")
    target = course_root / "course" / "course_by_date" / "2026-08-25" / "meeting.json"
    metadata = json.loads(target.read_text(encoding="utf-8"))
    copied = metadata["copied_outputs"][0]
    destination = target.parent / copied["destination"]
    original = destination.read_bytes()
    try:
        destination.write_bytes(original + b"tampered")
        with pytest.raises(GeneratedCalendarError, match="checksum mismatch"):
            validate_generated_course_by_date(course_root, calendar)
    finally:
        destination.write_bytes(original)
