"""Shared course activation helpers.

The repository may keep archived courses on disk, but generation and publish
commands should only operate on courses enabled in ``publish.toml``.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


class CourseSelectionError(ValueError):
    """Raised when a requested course is not an active course."""


def find_repo_root(start: Path | None = None) -> Path:
    """Find the repository root by walking upward to ``publish.toml``."""
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "publish.toml").exists():
            return candidate
    return Path(__file__).resolve().parents[3]


def load_publish_config(repo_root: Path | None = None) -> dict[str, Any]:
    """Load ``publish.toml`` from the repository root."""
    root = repo_root or find_repo_root()
    config_path = root / "publish.toml"
    if not config_path.exists():
        return {"publish": {"courses": _fallback_course_config()}}
    with config_path.open("rb") as handle:
        return tomllib.load(handle)


def course_configs(repo_root: Path | None = None) -> dict[str, dict[str, Any]]:
    """Return course configuration keyed by course id."""
    publish = load_publish_config(repo_root).get("publish", {})
    courses = publish.get("courses", {})
    return {str(name): dict(cfg) for name, cfg in courses.items()}


def active_course_names(repo_root: Path | None = None) -> list[str]:
    """Return course ids enabled for active generation/publishing."""
    courses = course_configs(repo_root)
    return [name for name, cfg in courses.items() if bool(cfg.get("enabled", True))]


def active_course_paths(repo_root: Path | None = None) -> list[tuple[str, str]]:
    """Return active courses as ``(relative_path, display_name)`` tuples."""
    courses = course_configs(repo_root)
    selected: list[tuple[str, str]] = []
    for name in active_course_names(repo_root):
        cfg = courses.get(name, {})
        rel_path = str(cfg.get("path") or f"course_development/{name}")
        selected.append((rel_path, name.upper()))
    return selected


def resolve_course_selection(course_arg: str, repo_root: Path | None = None) -> list[str]:
    """Resolve a CLI course argument to active course ids.

    Args:
        course_arg: Course id or ``all``.
        repo_root: Optional repository root.

    Returns:
        Active course ids to process.

    Raises:
        CourseSelectionError: If the course is archived, inactive, or unknown.
    """
    root = repo_root or find_repo_root()
    courses = course_configs(root)
    active = active_course_names(root)

    if course_arg == "all":
        if not active:
            raise CourseSelectionError("No active courses are enabled in publish.toml")
        return active

    if course_arg in active:
        return [course_arg]

    if course_arg in courses:
        cfg = courses[course_arg]
        archive_path = cfg.get("archive_path") or cfg.get("archived_path")
        if archive_path:
            raise CourseSelectionError(
                f"{course_arg} is archived/inactive; archived source: {archive_path}"
            )
        raise CourseSelectionError(f"{course_arg} is disabled in publish.toml")

    active_text = ", ".join(active) if active else "none"
    raise CourseSelectionError(f"Unknown course '{course_arg}'. Active courses: {active_text}")


def archived_course_paths(repo_root: Path | None = None) -> dict[str, str]:
    """Return disabled courses with configured archive paths."""
    archived: dict[str, str] = {}
    for name, cfg in course_configs(repo_root).items():
        if bool(cfg.get("enabled", True)):
            continue
        archive_path = cfg.get("archive_path") or cfg.get("archived_path")
        if archive_path:
            archived[name] = str(archive_path)
    return archived


def _fallback_course_config() -> dict[str, dict[str, Any]]:
    return {
        "biol-1": {
            "enabled": True,
            "path": "course_development/biol-1",
        }
    }
