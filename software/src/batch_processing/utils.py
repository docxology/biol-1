"""Utility functions for batch processing."""

import logging
from pathlib import Path
from typing import List, Optional

from . import config

logger = logging.getLogger(__name__)


def find_markdown_files(directory: Path) -> List[Path]:
    """Find all Markdown files in a directory recursively.

    Args:
        directory: Directory to search

    Returns:
        List of Markdown file paths
    """
    markdown_files = []
    for pattern in ["*.md", "*.markdown"]:
        markdown_files.extend(directory.rglob(pattern))
    return sorted(markdown_files)


def find_audio_files(directory: Path) -> List[Path]:
    """Find all audio files in a directory recursively.

    Args:
        directory: Directory to search

    Returns:
        List of audio file paths
    """
    audio_files = []
    for pattern in ["*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg"]:
        audio_files.extend(directory.rglob(pattern))
    return sorted(audio_files)


def should_process_file(file_path: Path, skip_dirs: List[str]) -> bool:
    """Check if a file should be processed (not in skip directories).

    Args:
        file_path: Path to file
        skip_dirs: List of directory names to skip

    Returns:
        True if file should be processed, False otherwise
    """
    for part in file_path.parts:
        if part in skip_dirs:
            return False
    return True


def ensure_output_directory(output_dir: Path) -> None:
    """Ensure output directory exists.

    Args:
        output_dir: Path to output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)


def get_relative_output_path(source_file: Path, source_dir: Path, output_dir: Path) -> Path:
    """Get output path maintaining relative structure.

    Args:
        source_file: Source file path
        source_dir: Source directory path
        output_dir: Output directory path

    Returns:
        Output file path maintaining relative structure
    """
    relative_path = source_file.relative_to(source_dir)
    output_file = output_dir / relative_path
    return output_file


def get_courses_to_process(course_arg: str) -> List[tuple]:
    """Get list of courses to process based on argument.

    Args:
        course_arg: Course name ("biol-1", "biol-8") or "all"

    Returns:
        List of (relative_path, display_name) tuples
    """
    all_courses = [
        (f"course_development/{c}", c.upper()) for c in config.AVAILABLE_COURSES
    ]

    if course_arg == "all":
        return all_courses

    return [(c, n) for c, n in all_courses if c.endswith(course_arg)]


def get_formats_to_process(formats_arg: str) -> List[str]:
    """Parse formats argument into list of valid formats.

    Args:
        formats_arg: Comma-separated format string or "all"

    Returns:
        List of valid format strings
    """
    if formats_arg == "all":
        return list(config.AVAILABLE_FORMATS)

    formats = [f.strip().lower() for f in formats_arg.split(",")]
    invalid = [f for f in formats if f not in config.AVAILABLE_FORMATS]
    if invalid:
        logger.warning(f"Unknown formats will be ignored: {invalid}")

    return [f for f in formats if f in config.AVAILABLE_FORMATS]


def generate_dry_run_report(
    repo_root: Path,
    courses: List[tuple],
    formats: List[str],
    module_filter: Optional[int] = None,
    generate_website: bool = True,
    skip_labs: bool = False,
) -> str:
    """Generate a dry-run report of what would be processed.

    Args:
        repo_root: Path to repository root
        courses: List of (relative_path, display_name) tuples
        formats: List of format strings
        module_filter: Optional module number to filter
        generate_website: Whether website generation is enabled
        skip_labs: Whether lab rendering is skipped

    Returns:
        Report string describing what would be processed
    """
    from src.module_organization.utils import matches_module_number

    lines = [
        "",
        "=" * 60,
        "DRY RUN - Files that would be processed:",
        "=" * 60,
    ]

    for course_dir, course_name in courses:
        course_path = repo_root / course_dir
        if not course_path.exists():
            continue

        lines.append(f"\n{course_name}:")
        course_dir_path = course_path / "course"
        if course_dir_path.exists():
            modules = sorted(
                [
                    d
                    for d in course_dir_path.iterdir()
                    if d.is_dir() and d.name.startswith("module-")
                ]
            )

            if module_filter is not None:
                modules = [
                    m for m in modules if matches_module_number(m.name, module_filter)
                ]

            for module_dir in modules:
                md_files = list(module_dir.glob("*.md"))
                assignment_files = (
                    list((module_dir / "assignments").glob("*.md"))
                    if (module_dir / "assignments").exists()
                    else []
                )
                lines.append(
                    f"  {module_dir.name}: {len(md_files)} root files, "
                    f"{len(assignment_files)} assignments"
                )
                lines.append(f"    Would generate: {', '.join(formats)}")
                if generate_website:
                    lines.append("    Would generate: website/index.html")

        syllabus_dir = course_path / "syllabus"
        if syllabus_dir.exists():
            syllabus_files = list(syllabus_dir.glob("*.md"))
            lines.append(f"  Syllabus: {len(syllabus_files)} files")
            lines.append(f"    Would generate: {', '.join(formats)}")

        if not skip_labs:
            labs_dir = course_path / "course" / "labs"
            if labs_dir.exists():
                lab_files = list(labs_dir.glob("lab-*.md"))
                lab_formats = [f for f in formats if f in ("pdf", "html")]
                lines.append(f"  Labs: {len(lab_files)} files")
                lines.append(
                    f"    Would generate: "
                    f"{', '.join(lab_formats) if lab_formats else 'none (no compatible formats)'}"
                )

    lines.append("\nDry run complete. No files were generated.")
    return "\n".join(lines)
