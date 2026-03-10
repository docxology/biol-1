"""Flattening functions for the publish module.

Handles flattening module directory structures by moving files from
subdirectories to the module root, and cleaning published directories.
"""

import shutil
import logging
from pathlib import Path
from typing import List, Optional


logger = logging.getLogger(__name__)


def flatten_module(module_dir: Path, dry_run: bool = False, verbose: bool = False) -> int:
    """Flatten a single module directory by moving files from subdirs to root.

    Args:
        module_dir: Path to the module directory
        dry_run: If True, show what would be done without modifying files
        verbose: If True, log individual file operations

    Returns:
        Number of files moved
    """
    moved = 0
    subdirs = [d for d in module_dir.iterdir() if d.is_dir()]

    for subdir in subdirs:
        for file in subdir.rglob('*'):
            if file.is_file():
                dest = module_dir / file.name
                # Handle potential name conflicts
                if dest.exists():
                    dest = module_dir / f"{subdir.name}_{file.name}"
                if verbose:
                    logger.debug(f"    {file} -> {dest}")
                if not dry_run:
                    shutil.move(str(file), str(dest))
                moved += 1

        # Remove empty subdirectory
        if not dry_run:
            shutil.rmtree(subdir)

    return moved


def flatten_published(
    published_dir: Path,
    skip_dirs: Optional[List[str]] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> int:
    """Flatten all module directories in PUBLISHED.

    Args:
        published_dir: Path to the PUBLISHED directory
        skip_dirs: List of directory names to skip (default: labs, dashboards, syllabus, slides, exams)
        dry_run: If True, show what would be done without modifying files
        verbose: If True, log individual file operations

    Returns:
        Total number of files moved
    """
    if skip_dirs is None:
        skip_dirs = ['labs', 'dashboards', 'syllabus', 'slides', 'exams', 'practice_tests']

    total_moved = 0

    for course_dir in published_dir.iterdir():
        if not course_dir.is_dir() or course_dir.name.startswith('.'):
            continue

        for module_dir in course_dir.iterdir():
            if not module_dir.is_dir():
                continue
            if module_dir.name in skip_dirs:
                continue

            subdirs = [d for d in module_dir.iterdir() if d.is_dir()]
            if subdirs:
                moved = flatten_module(module_dir, dry_run=dry_run, verbose=verbose)
                total_moved += moved

    return total_moved


def clean_published(published_dir: Path) -> None:
    """Remove all content from PUBLISHED directory.

    Args:
        published_dir: Path to the PUBLISHED directory
    """
    if published_dir.exists():
        for item in published_dir.iterdir():
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    logger.info("Cleaned PUBLISHED directory")
