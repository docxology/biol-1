"""Utility functions for validation module."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

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

    Study guide files are named with module prefix, e.g.:
    module-01-study-of-life-keys-to-success.pdf
    
    This function checks for files ending with expected base names.

    Args:
        module_path: Path to module directory

    Returns:
        Dictionary mapping expected base suffix to existence
    """
    study_guides_path = module_path / "output" / config.OUTPUT_DIRS["study_guides"]
    
    if not study_guides_path.exists():
        return {f: False for f in config.EXPECTED_STUDY_GUIDE_FILES}
    
    # Get all files in study guides directory
    existing_files = [f.name for f in study_guides_path.iterdir() if f.is_file()]
    
    result = {}
    for expected_suffix in config.EXPECTED_STUDY_GUIDE_FILES:
        # Check if any file ends with this suffix (e.g., "-keys-to-success.pdf")
        # The expected file is like "keys-to-success.pdf" and actual is "module-XX-topic-keys-to-success.pdf"
        suffix_to_check = f"-{expected_suffix}"
        found = any(f.endswith(suffix_to_check) or f == expected_suffix for f in existing_files)
        result[expected_suffix] = found
        
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


def check_lab_files(course_path: Path) -> Dict[str, Any]:
    """Check lab output files and dashboards for a course.

    Args:
        course_path: Path to course directory

    Returns:
        Dictionary with lab validation results:
        - source_labs: Number of source lab markdown files
        - output_files: Dict mapping format to count of rendered files
        - dashboards: Number of dashboard HTML files
        - missing_outputs: List of labs missing rendered output
        - issues: List of issues found
    """
    result: Dict[str, Any] = {
        "source_labs": 0,
        "output_files": {},
        "dashboards": 0,
        "missing_outputs": [],
        "issues": [],
    }

    labs_dir = course_path / "course" / "labs"
    if not labs_dir.exists():
        return result

    # Count source lab files
    source_labs = list(labs_dir.glob("lab-*.md"))
    result["source_labs"] = len(source_labs)

    # Check rendered output files (both flat output/*.fmt and subdirectory output/fmt/*.fmt)
    output_dir = labs_dir / "output"
    if output_dir.exists():
        for fmt in config.LAB_OUTPUT_FORMATS:
            count = 0
            # Check subdirectory: output/{fmt}/*.{fmt}
            fmt_dir = output_dir / fmt
            if fmt_dir.exists():
                count += len(list(fmt_dir.glob(f"*.{fmt}")))
            # Check flat: output/*.{fmt}
            count += len(list(output_dir.glob(f"*.{fmt}")))
            result["output_files"][fmt] = count
    else:
        for fmt in config.LAB_OUTPUT_FORMATS:
            result["output_files"][fmt] = 0
        if source_labs:
            result["issues"].append("Lab output directory not found")

    # Check each source lab has at least one rendered output
    for lab_file in source_labs:
        lab_stem = lab_file.stem
        has_output = False
        for fmt in config.LAB_OUTPUT_FORMATS:
            if output_dir.exists():
                # Check subdirectory: output/{fmt}/{lab_stem}.{fmt}
                fmt_dir = output_dir / fmt
                if fmt_dir.exists():
                    rendered = fmt_dir / f"{lab_stem}.{fmt}"
                    if rendered.exists() and rendered.stat().st_size > 0:
                        has_output = True
                        break
                # Check flat: output/{lab_stem}.{fmt}
                flat_rendered = output_dir / f"{lab_stem}.{fmt}"
                if flat_rendered.exists() and flat_rendered.stat().st_size > 0:
                    has_output = True
                    break
        if not has_output:
            result["missing_outputs"].append(lab_stem)

    # Check dashboards
    dashboards_dir = labs_dir / "dashboards"
    if dashboards_dir.exists():
        dashboard_files = list(dashboards_dir.glob("*.html"))
        result["dashboards"] = len(dashboard_files)
    else:
        if source_labs:
            result["issues"].append("Dashboards directory not found")

    return result
