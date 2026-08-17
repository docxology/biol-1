"""Load and validate the canonical BIOL-1 course-by-date map."""

from __future__ import annotations

import datetime as dt
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class CalendarError(ValueError):
    """Raised when a course calendar is malformed or inconsistent."""


ALLOWED_STATUSES = {"class", "no-class", "holiday", "break", "exam"}
ALLOWED_MATERIAL_KINDS = {"module", "lab", "practice_test", "exam", "review", "textbook"}
ALLOWED_INCLUDES = {"source", "generated", "slides", "lecture", "dashboard"}


@dataclass(frozen=True)
class MaterialSpec:
    """One planned or used material in a class meeting."""

    kind: str
    identifier: str
    planned: bool
    used: bool
    includes: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class Meeting:
    """One scheduled date and its material mapping."""

    date: dt.date
    week: int
    day: str
    status: str
    title: str
    notes: str
    materials: tuple[MaterialSpec, ...]

    @property
    def slug(self) -> str:
        """Return the stable folder name for this meeting."""
        return self.date.isoformat()


@dataclass(frozen=True)
class CourseCalendar:
    """Validated course calendar loaded from TOML."""

    course: str
    term: str
    timezone: str
    source_schedule: str
    meetings: tuple[Meeting, ...]
    textbook_title: str = ""
    textbook_planned: tuple[str, ...] = ()
    textbook_used: tuple[str, ...] = ()

    def validate(self, course_root: Path | None = None) -> None:
        """Validate structure and, optionally, all used material references."""
        if not self.course or not self.term or not self.timezone:
            raise CalendarError("calendar course, term, and timezone are required")
        if not self.meetings:
            raise CalendarError("calendar must contain at least one meeting")
        if not set(self.textbook_used).issubset(self.textbook_planned):
            raise CalendarError("textbook_used must be a subset of textbook_planned")

        seen_dates: set[dt.date] = set()
        for meeting in self.meetings:
            if meeting.date in seen_dates:
                raise CalendarError(f"duplicate meeting date: {meeting.date}")
            seen_dates.add(meeting.date)
            if meeting.week < 1:
                raise CalendarError(f"invalid week for {meeting.date}: {meeting.week}")
            if meeting.day != meeting.date.strftime("%a"):
                raise CalendarError(
                    f"day mismatch for {meeting.date}: {meeting.day!r}; "
                    f"expected {meeting.date.strftime('%a')!r}"
                )
            if meeting.status not in ALLOWED_STATUSES:
                raise CalendarError(f"invalid status for {meeting.date}: {meeting.status}")
            seen_materials: set[tuple[str, str]] = set()
            for material in meeting.materials:
                key = material.kind, material.identifier
                if key in seen_materials:
                    raise CalendarError(f"duplicate material on {meeting.date}: {key}")
                seen_materials.add(key)
                if material.kind not in ALLOWED_MATERIAL_KINDS:
                    raise CalendarError(f"invalid material kind: {material.kind}")
                if not material.identifier:
                    raise CalendarError(f"material identifier is empty on {meeting.date}")
                if not material.planned and material.used:
                    raise CalendarError(
                        f"material marked used but not planned on {meeting.date}: {key}"
                    )
                unknown = set(material.includes) - ALLOWED_INCLUDES
                if unknown:
                    raise CalendarError(f"unknown include(s) for {key}: {sorted(unknown)}")
                if material.used and not material.includes and material.kind != "textbook":
                    raise CalendarError(f"used material has no includes on {meeting.date}: {key}")

        if course_root is not None:
            for meeting in self.meetings:
                for material in meeting.materials:
                    if material.used and material.kind != "textbook":
                        paths = resolve_material_paths(course_root, material)
                        if not paths:
                            raise CalendarError(
                                f"used material has no source files on {meeting.date}: "
                                f"{material.kind}/{material.identifier} ({material.includes})"
                            )


def _string(value: Any, field: str, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CalendarError(f"{context}: {field} must be a non-empty string")
    return value.strip()


def _bool(value: Any, field: str, context: str) -> bool:
    if not isinstance(value, bool):
        raise CalendarError(f"{context}: {field} must be boolean")
    return value


def load_calendar(path: Path | str) -> CourseCalendar:
    """Load and structurally validate a TOML calendar."""
    calendar_path = Path(path)
    try:
        with calendar_path.open("rb") as handle:
            raw = tomllib.load(handle)
    except FileNotFoundError as exc:
        raise CalendarError(f"calendar not found: {calendar_path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise CalendarError(f"malformed calendar {calendar_path}: {exc}") from exc

    metadata = raw.get("calendar")
    meetings_raw = raw.get("meetings")
    if not isinstance(metadata, dict) or not isinstance(meetings_raw, list):
        raise CalendarError("calendar requires [calendar] and one or more [[meetings]] tables")

    meetings: list[Meeting] = []
    for index, raw_meeting in enumerate(meetings_raw, start=1):
        context = f"meeting {index}"
        if not isinstance(raw_meeting, dict):
            raise CalendarError(f"{context} must be a table")
        date_text = _string(raw_meeting.get("date"), "date", context)
        try:
            meeting_date = dt.date.fromisoformat(date_text)
        except ValueError as exc:
            raise CalendarError(f"{context}: invalid ISO date {date_text!r}") from exc
        raw_materials = raw_meeting.get("materials", [])
        if not isinstance(raw_materials, list):
            raise CalendarError(f"{context}: materials must be an array of tables")
        materials: list[MaterialSpec] = []
        for material_index, raw_material in enumerate(raw_materials, start=1):
            material_context = f"{context} material {material_index}"
            if not isinstance(raw_material, dict):
                raise CalendarError(f"{material_context} must be a table")
            includes = raw_material.get("include", [])
            if not isinstance(includes, list) or not all(
                isinstance(item, str) for item in includes
            ):
                raise CalendarError(f"{material_context}: include must be an array of strings")
            materials.append(
                MaterialSpec(
                    kind=_string(raw_material.get("kind"), "kind", material_context),
                    identifier=_string(raw_material.get("id"), "id", material_context),
                    planned=_bool(raw_material.get("planned"), "planned", material_context),
                    used=_bool(raw_material.get("used"), "used", material_context),
                    includes=tuple(str(item).strip() for item in includes),
                    notes=str(raw_material.get("notes", "")).strip(),
                )
            )
        meetings.append(
            Meeting(
                date=meeting_date,
                week=int(raw_meeting.get("week", 0)),
                day=_string(raw_meeting.get("day"), "day", context),
                status=_string(raw_meeting.get("status"), "status", context),
                title=_string(raw_meeting.get("title"), "title", context),
                notes=str(raw_meeting.get("notes", "")).strip(),
                materials=tuple(materials),
            )
        )

    textbook = metadata.get("textbook", {})
    if not isinstance(textbook, dict):
        raise CalendarError("calendar.textbook must be a table")
    planned_chapters = textbook.get("planned_chapters", [])
    used_chapters = textbook.get("used_chapters", [])
    if not isinstance(planned_chapters, list) or not isinstance(used_chapters, list):
        raise CalendarError("calendar.textbook chapter lists must be arrays")
    if not all(isinstance(item, str) for item in [*planned_chapters, *used_chapters]):
        raise CalendarError("calendar.textbook chapter lists must contain strings")
    calendar = CourseCalendar(
        course=_string(metadata.get("course"), "course", "calendar"),
        term=_string(metadata.get("term"), "term", "calendar"),
        timezone=_string(metadata.get("timezone"), "timezone", "calendar"),
        source_schedule=_string(metadata.get("source_schedule"), "source_schedule", "calendar"),
        meetings=tuple(meetings),
        textbook_title=str(textbook.get("title", "")).strip(),
        textbook_planned=tuple(planned_chapters),
        textbook_used=tuple(used_chapters),
    )
    calendar.validate()
    return calendar


def _module_dir(course_root: Path, identifier: str) -> Path:
    return course_root / "course" / identifier


def resolve_material_paths(course_root: Path, material: MaterialSpec) -> list[tuple[str, Path]]:
    """Resolve a material spec to labeled source files."""
    if material.kind == "textbook":
        return []
    course_dir = course_root / "course"
    if material.kind == "module":
        module_dir = _module_dir(course_root, material.identifier)
        number = material.identifier.split("-", 2)[1]
        candidates: list[tuple[str, Path]] = []
        for include in material.includes:
            if include == "source":
                for name in ("README.md", "questions.md", "key-points.md", "practice-quiz.md"):
                    candidates.append((include, module_dir / name))
            elif include == "generated":
                candidates.extend((include, path) for path in (module_dir / "output").rglob("*"))
            elif include == "slides":
                slides_dir = course_root / "resources" / "slides"
                candidates.extend(
                    (include, path) for path in slides_dir.glob(f"module-{int(number)}-slides-*")
                )
                candidates.extend(
                    (include, path)
                    for path in (slides_dir / "generated").glob(f"module-{int(number)}-slides-*")
                )
            elif include == "lecture":
                lecture_dir = (
                    course_root.parent.parent / "output" / "lectures" / material.identifier
                )
                # A date folder is a teaching handoff, not a second build
                # cache. Keep the playable lecture; JSON manifests, captions,
                # frames, WAVs, hashes, and render
                # logs remain in the canonical LectureCreate output tree.
                delivery_names = {"lecture.mp4"}
                candidates.extend(
                    (include, path)
                    for path in lecture_dir.rglob("*")
                    if path.is_file() and path.name in delivery_names
                )
                candidates.extend(
                    (include, path) for path in lecture_dir.glob("*.yaml") if path.is_file()
                )
        return [(label, path) for label, path in candidates if path.is_file()]

    if material.kind == "lab":
        lab_path = course_dir / "labs" / material.identifier
        candidates = [("source", lab_path)]
        dashboard = (
            course_dir / "labs" / "dashboards" / f"{Path(material.identifier).stem}-dashboard.html"
        )
        if "dashboard" in material.includes:
            candidates.append(("dashboard", dashboard))
        return [(label, path) for label, path in candidates if path.is_file()]

    base_dirs = {
        "practice_test": course_dir / "practice_tests",
        "exam": course_dir / "exams",
        "review": course_dir / "review_materials",
    }
    base_dir = base_dirs[material.kind]
    extension = ".md"
    path = base_dir / f"{material.identifier}{extension}"
    return [("source", path)] if path.is_file() else []
