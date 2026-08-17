"""Generate the copy-only BIOL-1 course-by-date projection."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .calendar import CourseCalendar, MaterialSpec, Meeting, resolve_material_paths


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_destination(root: Path, destination: Path) -> Path:
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if resolved_root != resolved_destination and resolved_root not in resolved_destination.parents:
        raise ValueError(f"destination escapes generated root: {destination}")
    return destination


def _copy_material(
    course_root: Path,
    meeting_root: Path,
    material: MaterialSpec,
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    material_id = material.identifier.removesuffix(".md")
    material_root = meeting_root / "materials"
    for label, source in resolve_material_paths(course_root, material):
        if label == "source" or source.suffix.lower() in {".md", ".json", ".html", ".srt", ".vtt"}:
            continue
        relative_source = source.relative_to(course_root.parent.parent)
        filename = (
            source.name
            if source.name.startswith(f"{material_id}-")
            else f"{material_id}-{source.name}"
        )
        destination = _safe_destination(meeting_root, material_root / filename)
        if destination.exists():
            raise ValueError(f"duplicate generated destination: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entries.append(
            {
                "kind": material.kind,
                "id": material.identifier,
                "include": label,
                "source": relative_source.as_posix(),
                "destination": destination.relative_to(meeting_root).as_posix(),
                "sha256": _sha256(destination),
            }
        )
    return entries


def _meeting_metadata(meeting: Meeting) -> dict[str, Any]:
    return {
        "date": meeting.date.isoformat(),
        "week": meeting.week,
        "day": meeting.day,
        "status": meeting.status,
        "title": meeting.title,
        "notes": meeting.notes,
        "materials": [
            {
                "kind": item.kind,
                "id": item.identifier,
                "planned": item.planned,
                "used": item.used,
                "include": list(item.includes),
                "notes": item.notes,
            }
            for item in meeting.materials
        ],
    }


def _readme(meeting: Meeting, copied: list[dict[str, str]]) -> str:
    lines = [
        f"# {meeting.date.isoformat()} — {meeting.title}",
        "",
        f"- **Week:** {meeting.week}",
        f"- **Day:** {meeting.day}",
        f"- **Status:** {meeting.status}",
    ]
    if meeting.notes:
        lines.append(f"- **Notes:** {meeting.notes}")
    lines.extend(["", "This folder is generated from the BIOL-1 course date map."])
    if not copied:
        lines.extend(["", "No source outputs are copied for this date."])
    else:
        lines.extend(["", "## Copied outputs", ""])
        lines.extend(f"- `{item['destination']}` ← `{item['source']}`" for item in copied)
    lines.append("")
    return "\n".join(lines)


def generate_course_by_date(
    course_root: Path | str,
    calendar: CourseCalendar,
    *,
    clean: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Generate one date folder per calendar meeting.

    Only files resolved from ``used = true`` material records are copied. The
    generated JSON manifest retains planned and used state for future audits.
    """
    root = Path(course_root).resolve()
    output_root = root / "course" / "course_by_date"
    calendar.validate(root)
    if clean and output_root.exists() and not dry_run:
        shutil.rmtree(output_root)
    if dry_run:
        return {"output": output_root.as_posix(), "meetings": len(calendar.meetings), "files": 0}

    copied_count = 0
    for meeting in calendar.meetings:
        meeting_root = output_root / meeting.slug
        meeting_root.mkdir(parents=True, exist_ok=True)
        (meeting_root / "materials").mkdir()
        copied: list[dict[str, str]] = []
        for material in meeting.materials:
            if material.used:
                copied.extend(_copy_material(root, meeting_root, material))
        (meeting_root / "meeting.json").write_text(
            json.dumps(
                {"meeting": _meeting_metadata(meeting), "copied_outputs": copied},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (meeting_root / "README.md").write_text(_readme(meeting, copied), encoding="utf-8")
        copied_count += len(copied)

    index = {
        "course": calendar.course,
        "term": calendar.term,
        "timezone": calendar.timezone,
        "source_schedule": calendar.source_schedule,
        "textbook": {
            "title": calendar.textbook_title,
            "planned_chapters": list(calendar.textbook_planned),
            "used_chapters": list(calendar.textbook_used),
        },
        "generated_from": "course_calendar.toml",
        "meeting_count": len(calendar.meetings),
        "copied_output_count": copied_count,
        "meetings": [meeting.slug for meeting in calendar.meetings],
    }
    (output_root / "index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_root / "README.md").write_text(
        "# BIOL-1 Course by Date\n\n"
        "Generated from `course_calendar.toml`; edit the map and regenerate.\n\n"
        "Each dated folder contains one flat `materials/` directory of copied\n"
        "teaching deliverables plus a machine-readable provenance manifest.\n"
        "Rebuildable LectureCreate frames, audio intermediates, and hashes stay\n"
        "in `output/lectures/`.\n",
        encoding="utf-8",
    )
    return {
        "output": output_root.as_posix(),
        "meetings": len(calendar.meetings),
        "files": copied_count,
    }
