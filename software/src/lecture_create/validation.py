"""Semantic validation for rendered BIOL-1 LectureCreate artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.module_content.main import ModuleContent, load_module_content

MIN_LECTURE_SECONDS = 240
# A frame/audio boundary can add a fraction of a second during muxing; retain
# a one-second quantization tolerance while keeping the student-facing target
# at approximately five minutes.
MAX_LECTURE_SECONDS = 301


def _plain(value: str) -> str:
    """Normalize prose for robust comparison without changing authored text."""
    return re.sub(r"\s+", " ", value).strip().rstrip(".")


def _contains(text: str, value: str) -> bool:
    return _plain(value).lower() in _plain(text).lower()


def validate_rendered_lecture(module: ModuleContent, artifact_dir: Path | str) -> list[str]:
    """Return semantic and portability issues for one rendered lecture.

    File-presence checks alone cannot detect an incomplete narration or a
    lecture that references the wrong module. This validator compares the
    measured LectureCreate JSON against the authoritative ``module.toml``.
    """
    root = Path(artifact_dir)
    lecture_root = root if (root / "lectures").is_dir() else root / module.slug
    lecture_path = lecture_root / "lectures" / "lecture.json"
    issues: list[str] = []
    if not lecture_path.is_file():
        return ["missing lectures/lecture.json"]
    try:
        payload: dict[str, Any] = json.loads(lecture_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid lectures/lecture.json: {exc}"]

    expected_title = f"BIOL-1 Module {module.number:02d}: {module.title}"
    if payload.get("title") != expected_title:
        issues.append(f"title mismatch: expected {expected_title!r}")
    sections = payload.get("sections")
    if not isinstance(sections, list) or len(sections) != 1:
        return issues + ["expected exactly one module section"]
    section = sections[0]
    if section.get("objectives") != list(module.learning_objectives):
        issues.append("section objectives do not exactly match module.toml")

    beats = section.get("beats")
    if not isinstance(beats, list):
        return issues + ["section beats are missing or not a list"]
    expected_ids = [f"{module.slug}_title", f"{module.slug}_objectives", f"{module.slug}_topics"]
    expected_ids += [
        f"{module.slug}_concept_map",
        f"{module.slug}_process_model",
        f"{module.slug}_application",
    ]
    term_page_count = (len(module.terms) + 2) // 3
    expected_ids += [f"{module.slug}_terms_{i:02d}" for i in range(1, term_page_count + 1)]
    expected_ids += [
        f"{module.slug}_lab",
        f"{module.slug}_retrieval",
        f"{module.slug}_quiz",
        f"{module.slug}_study_move",
        f"{module.slug}_synthesis",
    ]
    actual_ids = [beat.get("id") for beat in beats]
    if actual_ids != expected_ids:
        issues.append(f"beat sequence mismatch: expected {len(expected_ids)} complete beats")

    narration = " ".join(str(beat.get("narration", "")) for beat in beats)
    for label, values in (
        ("objective", module.learning_objectives),
        ("topic", module.topics),
        ("term", tuple(term.name for term in module.terms)),
    ):
        missing = [value for value in values if not _contains(narration, value)]
        if missing:
            issues.append(f"narration omits {label}(s): {', '.join(missing)}")

    term_bullets: list[str] = []
    for beat in beats:
        visual = beat.get("visual", {})
        audio_path = beat.get("audio_path")
        if audio_path and Path(str(audio_path)).is_absolute():
            issues.append(f"non-portable absolute audio path: {audio_path}")
        image_path = visual.get("image_path")
        if image_path:
            path = Path(str(image_path))
            if path.is_absolute():
                issues.append(f"non-portable absolute image path: {image_path}")
            elif not (root / path).is_file():
                issues.append(f"missing referenced image: {image_path}")
        if str(beat.get("id", "")).startswith(f"{module.slug}_terms_"):
            term_bullets.extend(str(item) for item in visual.get("bullets", []))
    expected_term_bullets = [f"{term.name}: {term.definition}" for term in module.terms]
    if term_bullets != expected_term_bullets:
        issues.append("key-term recap does not contain every term exactly once and in order")

    if "can grow into a theory" in narration.lower():
        issues.append("contains the inaccurate claim that a hypothesis can grow into a theory")

    durations = [beat.get("duration_ms") for beat in beats]
    if durations and all(isinstance(value, (int, float)) for value in durations):
        total_seconds = sum(float(value) for value in durations) / 1000
        if not MIN_LECTURE_SECONDS <= total_seconds <= MAX_LECTURE_SECONDS:
            issues.append(
                f"measured lecture duration {total_seconds:.1f}s is outside "
                f"the {MIN_LECTURE_SECONDS}-{MAX_LECTURE_SECONDS}s target"
            )
    return issues


def validate_module_lecture(module_dir: Path | str, artifact_dir: Path | str) -> list[str]:
    """Load one authoritative module and validate its rendered lecture."""
    return validate_rendered_lecture(load_module_content(module_dir), artifact_dir)
