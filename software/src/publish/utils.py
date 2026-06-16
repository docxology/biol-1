"""Utility functions for the publish module.

Core utilities are defined here. Flattening and copy/extras functions are
defined in their own sub-modules and re-exported here for backward
compatibility so that existing callers (scripts, tests) that import from
``src.publish.utils`` continue to work without changes.
"""

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

from . import config
from .flatten import (  # noqa: F401
    clean_published,
    flatten_module,
    flatten_published,
)
from .copy_extras import (  # noqa: F401
    copy_exams,
    copy_labs_and_dashboards,
    copy_practice_tests,
    copy_slides,
    copy_slides_to_modules,
    reorganize_to_categories,
)

logger = logging.getLogger(__name__)


def get_course_config(course_name: str) -> Dict[str, Any]:
    """Get configuration for a specific course.

    Args:
        course_name: Name of the course directory (e.g., 'biol-1')

    Returns:
        Dictionary with configuration options
    """
    return config.COURSE_CONFIGS.get(course_name, config.DEFAULT_CONFIG)


def clean_directory(path: Path) -> None:
    """Clean a directory (remove all contents) or create if doesn't exist.

    Args:
        path: Path to the directory to clean
    """
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_directory_contents(
    src: Path, dst: Path, exclude_patterns: Optional[List[str]] = None
) -> int:
    """Copy contents of source directory to destination.

    Args:
        src: Source directory path
        dst: Destination directory path
        exclude_patterns: List of glob patterns to exclude

    Returns:
        Number of files copied
    """
    if not src.exists():
        logger.warning(f"Source directory does not exist: {src}")
        return 0

    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)

    if exclude_patterns is None:
        exclude_patterns = config.EXCLUDE_PATTERNS

    count = 0
    # shutil.copytree requires dst to not exist or be empty if dirs_exist_ok=True (3.8+)
    # We'll use manual walk to be safe and handle exclusions easily

    for item in src.rglob("*"):
        if not item.is_file():
            continue

        # Check exclusions
        relative_path = item.relative_to(src)
        if any(item.match(p) for p in exclude_patterns):
            continue

        # Determine destination path
        dest_file = dst / relative_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(item, dest_file)
            count += 1
        except Exception as e:
            logger.error(f"Failed to copy {item}: {e}")

    return count
