"""Utility functions for validation module."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import config

logger = logging.getLogger(__name__)


def count_files_by_extension(directory: Path) -> Dict[str, int]:
    """Count files in directory by extension.

    Args:
        directory: Path to directory to scan

    Returns:
        Dictionary mapping extension to count
    """
    counts: Dict[str, int] = {}
    
    if not directory.exists():
        return counts
        
    for file_path in directory.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            ext = file_path.suffix.lower().lstrip(".")
            if ext:
                counts[ext] = counts.get(ext, 0) + 1
                
    return counts


def get_module_directories(course_path: Path) -> List[Path]:
    """Get list of module directories in a course.

    Args:
        course_path: Path to course directory

    Returns:
        Sorted list of module directory paths
    """
    modules_path = course_path / "course"
    
    if not modules_path.exists():
        return []
        
    return sorted([
        d for d in modules_path.iterdir()
        if d.is_dir() and d.name.startswith("module-")
    ])


def check_output_directory(module_path: Path) -> Tuple[bool, Dict[str, bool]]:
    """Check if module has expected output directory structure.

    Args:
        module_path: Path to module directory

    Returns:
        Tuple of (has_output, dict of subdirectory existence)
    """
    output_path = module_path / "output"
    
    if not output_path.exists():
        return False, {}
        
    subdirs = {
        "study_guides": (output_path / config.OUTPUT_DIRS["study_guides"]).exists(),
        "website": (output_path / config.OUTPUT_DIRS["website"]).exists(),
    }
    
    return True, subdirs


def check_study_guide_files(module_path: Path) -> Dict[str, bool]:
    """Check which study guide files exist for a module.

    Args:
        module_path: Path to module directory

    Returns:
        Dictionary mapping expected filename to existence
    """
    study_guides_path = module_path / "output" / config.OUTPUT_DIRS["study_guides"]
    
    result = {}
    for expected_file in config.EXPECTED_STUDY_GUIDE_FILES:
        file_path = study_guides_path / expected_file
        result[expected_file] = file_path.exists()
        
    return result


def check_website_files(module_path: Path) -> Dict[str, bool]:
    """Check which website files exist for a module.

    Args:
        module_path: Path to module directory

    Returns:
        Dictionary mapping expected filename to existence
    """
    website_path = module_path / "output" / config.OUTPUT_DIRS["website"]
    
    result = {}
    for expected_file in config.EXPECTED_WEBSITE_FILES:
        file_path = website_path / expected_file
        result[expected_file] = file_path.exists()
        
    return result


def format_file_counts(counts: Dict[str, int]) -> str:
    """Format file counts as readable string.

    Args:
        counts: Dictionary of extension to count

    Returns:
        Formatted string like "pdf:10, html:5, mp3:3"
    """
    if not counts:
        return "none"
        
    return ", ".join(f"{ext}:{count}" for ext, count in sorted(counts.items()))


def get_timestamp() -> str:
    """Get current timestamp for logging.

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(config.LOG_DATE_FORMAT)
