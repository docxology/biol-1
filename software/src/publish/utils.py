"""Utility functions for the publish module."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging

from . import config

logger = logging.getLogger(__name__)


def get_course_config(course_name: str) -> Dict[str, str]:
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


def copy_directory_contents(src: Path, dst: Path, exclude_patterns: Optional[List[str]] = None) -> int:
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


# =============================================================================
# Flattening Functions (migrated from scripts/flatten_published.py)
# =============================================================================

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


# =============================================================================
# Copy Functions (migrated from scripts/publish_all.py)
# =============================================================================

def copy_labs_and_dashboards(
    repo_root: Path,
    courses: Optional[List[str]] = None,
    verbose: bool = False
) -> int:
    """Copy labs and dashboards to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: ['biol-1', 'biol-8'])
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = ['biol-1', 'biol-8']

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        course_dev = repo_root / 'course_development' / course / 'course' / 'labs'
        course_pub = published_dir / course

        if not course_dev.exists():
            logger.warning(f"Labs directory not found: {course_dev}")
            continue

        # Create directories
        labs_pub = course_pub / 'labs'
        dashboards_pub = course_pub / 'dashboards'
        labs_pub.mkdir(parents=True, exist_ok=True)
        dashboards_pub.mkdir(parents=True, exist_ok=True)

        # Copy lab files
        for lab_file in course_dev.glob('lab-*.md'):
            dest = labs_pub / lab_file.name
            shutil.copy2(lab_file, dest)
            total_copied += 1

        # Copy lab outputs (both flat files and format subdirectories)
        output_dir = course_dev / 'output'
        if output_dir.exists():
            for output_file in output_dir.rglob('*'):
                if output_file.is_file():
                    dest = labs_pub / output_file.name
                    shutil.copy2(output_file, dest)
                    total_copied += 1

        # Copy dashboards
        dashboards_dir = course_dev / 'dashboards'
        if dashboards_dir.exists():
            for dashboard_file in dashboards_dir.glob('*.html'):
                dest = dashboards_pub / dashboard_file.name
                shutil.copy2(dashboard_file, dest)
                total_copied += 1

        logger.info(f"  {course}: Copied labs and dashboards")

    return total_copied


def copy_slides(
    repo_root: Path,
    courses: Optional[List[str]] = None,
    verbose: bool = False
) -> int:
    """Copy slide PDFs from resources/slides to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: ['biol-1', 'biol-8'])
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = ['biol-1', 'biol-8']

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        slides_src = repo_root / 'course_development' / course / 'resources' / 'slides'
        slides_dest = published_dir / course / 'slides'

        if not slides_src.exists():
            continue

        slides_dest.mkdir(parents=True, exist_ok=True)
        course_copied = 0

        for slide_file in slides_src.glob('*.pdf'):
            dest = slides_dest / slide_file.name
            shutil.copy2(slide_file, dest)
            course_copied += 1

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slide PDFs")
            total_copied += course_copied

    return total_copied


def copy_slides_to_modules(
    repo_root: Path,
    courses: Optional[List[str]] = None,
    verbose: bool = False
) -> int:
    """Copy slide PDFs into each module's published folder.

    Maps module directories (e.g., module-01-study-of-life/) to slide files
    (e.g., module-1-slides-full.pdf) and copies slides into each module folder.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: ['biol-1', 'biol-8'])
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = ['biol-1', 'biol-8']

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        slides_src = repo_root / 'course_development' / course / 'resources' / 'slides'
        course_pub = published_dir / course

        if not slides_src.exists() or not course_pub.exists():
            continue

        course_copied = 0

        for module_dir in sorted(course_pub.iterdir()):
            if not module_dir.is_dir():
                continue
            if not module_dir.name.startswith('module-'):
                continue

            # Extract module number from directory name
            try:
                module_num = int(module_dir.name.split('-')[1])
            except (IndexError, ValueError):
                continue

            # Find matching slides
            slide_pattern = f"module-{module_num}-slides-*.pdf"
            matching_slides = list(slides_src.glob(slide_pattern))

            for slide_file in matching_slides:
                dest = module_dir / slide_file.name
                shutil.copy2(slide_file, dest)
                course_copied += 1

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slides into module folders")
            total_copied += course_copied

    return total_copied


def copy_exams(repo_root: Path, verbose: bool = False) -> int:
    """Copy exam files from course/exams to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    # BIOL-8 has exams in course/exams/
    exams_src = repo_root / 'course_development' / 'biol-8' / 'course' / 'exams'
    exams_dest = published_dir / 'biol-8' / 'exams'

    if not exams_src.exists():
        logger.warning(f"Exams directory not found: {exams_src}")
        return 0

    exams_dest.mkdir(parents=True, exist_ok=True)

    # Copy exam markdown files (exclude answer keys with _key suffix)
    for exam_file in exams_src.glob('*.md'):
        if not exam_file.stem.endswith('_key'):
            dest = exams_dest / exam_file.name
            shutil.copy2(exam_file, dest)
            total_copied += 1

    # Copy exam outputs (PDF, DOCX, etc.) if they exist
    output_dir = exams_src / 'output'
    if output_dir.exists():
        for output_file in output_dir.rglob('*'):
            if output_file.is_file():
                dest = exams_dest / output_file.name
                shutil.copy2(output_file, dest)
                total_copied += 1

    if total_copied > 0:
        logger.info(f"  biol-8: Copied {total_copied} exam files")

    return total_copied


def copy_practice_tests(
    repo_root: Path,
    courses: Optional[List[str]] = None,
    verbose: bool = False
) -> int:
    """Copy practice test files from course/practice_tests to PUBLISHED directory.

    Copies practice test markdown files (including answer keys) and any
    rendered outputs (PDF, DOCX). Both tests and answer keys are published
    so students can self-assess.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: ['biol-1', 'biol-8'])
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = ['biol-1', 'biol-8']

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        practice_tests_src = repo_root / 'course_development' / course / 'course' / 'practice_tests'
        practice_tests_dest = published_dir / course / 'practice_tests'

        if not practice_tests_src.exists():
            if verbose:
                logger.debug(f"Practice tests directory not found: {practice_tests_src}")
            continue

        practice_tests_dest.mkdir(parents=True, exist_ok=True)
        course_copied = 0

        # Copy practice test markdown files (including answer keys)
        for test_file in practice_tests_src.glob('*.md'):
            if test_file.name == 'README.md':
                continue  # Skip README
            dest = practice_tests_dest / test_file.name
            shutil.copy2(test_file, dest)
            course_copied += 1

        # Copy practice test outputs (PDF, DOCX, etc.) if they exist
        output_dir = practice_tests_src / 'output'
        if output_dir.exists():
            for output_file in output_dir.rglob('*'):
                if output_file.is_file():
                    dest = practice_tests_dest / output_file.name
                    shutil.copy2(output_file, dest)
                    course_copied += 1

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} practice test files")
            total_copied += course_copied

    return total_copied

