"""Validation for generated BIOL-1 course-by-date projections."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .calendar import CourseCalendar


class GeneratedCalendarError(ValueError):
    """Raised when generated date folders are incomplete or stale."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_generated_course_by_date(
    course_root: Path | str, calendar: CourseCalendar
) -> dict[str, Any]:
    """Validate date folders, copied-source provenance, and delivery contents."""
    root = Path(course_root).resolve()
    output_root = root / "course" / "course_by_date"
    calendar.validate(root)
    if not output_root.is_dir():
        raise GeneratedCalendarError(f"generated calendar is missing: {output_root}")

    index_path = output_root / "index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise GeneratedCalendarError(f"invalid generated index: {index_path}") from exc
    expected_slugs = [meeting.slug for meeting in calendar.meetings]
    if index.get("meetings") != expected_slugs:
        raise GeneratedCalendarError("generated index meeting order does not match calendar")
    expected_textbook = {
        "title": calendar.textbook_title,
        "planned_chapters": list(calendar.textbook_planned),
        "used_chapters": list(calendar.textbook_used),
    }
    if index.get("textbook") != expected_textbook:
        raise GeneratedCalendarError("generated index textbook mapping is stale")

    copied_count = 0
    for meeting in calendar.meetings:
        meeting_root = output_root / meeting.slug
        metadata_path = meeting_root / "meeting.json"
        readme_path = meeting_root / "README.md"
        if not metadata_path.is_file() or not readme_path.is_file():
            raise GeneratedCalendarError(f"incomplete generated meeting folder: {meeting.slug}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("meeting", {}).get("date") != meeting.slug:
            raise GeneratedCalendarError(f"meeting metadata date mismatch: {meeting.slug}")
        child_directories = {path.name for path in meeting_root.iterdir() if path.is_dir()}
        if child_directories != {"materials"}:
            raise GeneratedCalendarError(
                f"date folder must contain only one materials directory: {meeting.slug}"
            )
        materials_root = meeting_root / "materials"
        for item in metadata.get("copied_outputs", []):
            destination = meeting_root / item["destination"]
            source = root.parent.parent / item["source"]
            if not destination.is_file():
                raise GeneratedCalendarError(f"missing copied output: {destination}")
            if not source.is_file():
                raise GeneratedCalendarError(f"missing provenance source: {source}")
            if _sha256(destination) != item["sha256"]:
                raise GeneratedCalendarError(f"copied output checksum mismatch: {destination}")
            if destination.parent != materials_root:
                raise GeneratedCalendarError(
                    f"copied output is not flat under materials/: {destination}"
                )
            if destination.suffix.lower() in {".md", ".json", ".html", ".srt", ".vtt"}:
                raise GeneratedCalendarError(
                    f"source/metadata/web/caption file copied into materials/: {destination}"
                )
            copied_count += 1
        forbidden = [
            path
            for path in meeting_root.rglob("*")
            if path.is_file()
            and (path.suffix in {".wav", ".hash"} or path.name.startswith("frame_"))
        ]
        if forbidden:
            raise GeneratedCalendarError(
                f"build intermediate copied into {meeting.slug}: {forbidden[0]}"
            )

    if index.get("copied_output_count") != copied_count:
        raise GeneratedCalendarError("generated index copied-output count is stale")
    return {"meetings": len(calendar.meetings), "copied_outputs": copied_count}
