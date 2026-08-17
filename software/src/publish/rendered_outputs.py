"""Copy generated course outputs into the repository-level output projection."""

from __future__ import annotations

import shutil
from pathlib import Path

__all__ = ["copy_course_rendered_outputs"]


def copy_course_rendered_outputs(
    repo_root: Path | str,
    course_path: Path | str,
    course_name: str,
) -> dict[str, object]:
    """Rebuild ``output/<course_name>/`` from source-tree render outputs."""
    root = Path(repo_root).resolve()
    course = Path(course_path).resolve()
    if not course.is_dir():
        raise FileNotFoundError(f"course directory does not exist: {course}")

    destination = root / "output" / course_name
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for output_dir in sorted(path for path in course.rglob("output") if path.is_dir()):
        relative_parent = output_dir.parent.relative_to(course)
        for source in sorted(path for path in output_dir.rglob("*") if path.is_file()):
            target = destination / relative_parent / source.relative_to(output_dir)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(str(target.relative_to(root)))

    return {
        "course": course_name,
        "destination": str(destination),
        "files": copied,
        "count": len(copied),
    }
