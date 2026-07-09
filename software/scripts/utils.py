"""Shared utility functions for CLI scripts."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def print_module_not_found(course_path: Path, course_id: str, module_num: int) -> None:
    """Log diagnostic information when a module is not found.

    Lists available modules in the course directory to help the user
    identify valid module numbers.

    Args:
        course_path: Path to the course root (e.g., repo/course_development/biol-1)
        course_id: Course identifier string (e.g., "biol-1")
        module_num: The module number that was not found
    """
    logger.error("Module %d not found in %s", module_num, course_id)
    logger.error("Available modules in %s:", course_id)
    course_dir = course_path / "course"
    if course_dir.exists():
        modules: list[str] = sorted(
            [d.name for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("module-")]
        )
        for m in modules:
            logger.error("  - %s", m)
