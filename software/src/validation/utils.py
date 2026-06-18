"""Utility functions for validation module."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import config
from src.shared.file_utils import is_within_directory

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
        if (
            file_path.is_file()
            and not file_path.name.startswith(".")
            and is_within_directory(file_path, directory)
        ):
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
        
    def sort_key(path: Path) -> tuple[int, str]:
        import re

        match = re.match(r"module-(\d+)", path.name)
        return (int(match.group(1)) if match else 9999, path.name)

    return sorted(
        [
            d for d in modules_path.iterdir()
            if d.is_dir() and d.name.startswith("module-")
        ],
        key=sort_key,
    )


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


def check_study_guide_files(module_path: Path, formats: Optional[List[str]] = None) -> Dict[str, bool]:
    """Check which study guide files exist for a module.

    Study guide files are named with module prefix, e.g.:
    module-01-study-of-life-keys-to-success.pdf
    
    This function checks for files ending with expected base names.

    Args:
        module_path: Path to module directory
        formats: Optional list of formats to check (e.g., ["pdf", "docx"]).
                 If None, uses EXPECTED_STUDY_GUIDE_FILES from config.

    Returns:
        Dictionary mapping expected base suffix to existence
    """
    study_guides_path = module_path / "output" / config.OUTPUT_DIRS["study_guides"]
    
    # Get expected files based on formats
    expected_files = config.get_expected_study_guide_files(formats)
    
    if not study_guides_path.exists():
        return {f: False for f in expected_files}
    
    # Get all files in study guides directory
    existing_files = [f.name for f in study_guides_path.iterdir() if f.is_file()]
    
    result = {}
    for expected_suffix in expected_files:
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

    if not website_path.exists():
        return {f: False for f in config.EXPECTED_WEBSITE_FILES}

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


def _classify_lab_file(lab_path: Path) -> Tuple[Optional[int], bool]:
    """Classify a lab markdown file as numbered/supplemental.

    A "numbered" lab matches ``lab-NN_*.md`` and has no supplemental marker
    (``followup``, ``follow-up``) in its stem. A supplemental lab is any other
    ``lab-*.md`` file (e.g. ``lab-14_microbiology-followup.md``).

    Args:
        lab_path: Path to the lab markdown file.

    Returns:
        Tuple of ``(lab_number, is_numbered)``. ``lab_number`` is the integer
        portion of ``lab-NN`` when present (``None`` for files like
        ``lab-overview.md``). ``is_numbered`` is True only when the file is
        a primary numbered protocol — supplemental files always return False.
    """
    import re

    stem = lab_path.stem
    match = re.match(r"lab-(\d+)", stem)
    lab_number = int(match.group(1)) if match else None

    supplemental_markers = ("followup", "follow-up")
    lower_stem = stem.lower()
    is_supplemental = any(marker in lower_stem for marker in supplemental_markers)

    is_numbered = lab_number is not None and not is_supplemental
    return lab_number, is_numbered


def check_lab_files(
    course_path: Path,
    max_lab: Optional[int] = None,
    formats: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Check lab output files and dashboards for a course.

    Args:
        course_path: Path to course directory.
        max_lab: Optional max lab number to check (e.g., 4 means only labs 1-4).
        formats: Optional list of output formats requested by the publish
                 pipeline (e.g. ``["pdf", "docx", "md"]``). When provided,
                 only formats that labs can render are counted; otherwise
                 falls back to :data:`config.LAB_OUTPUT_FORMATS` for
                 backward compatibility.

    Returns:
        Dictionary with lab validation results:

        - ``source_labs``: Number of source lab markdown files in scope.
        - ``source_labs_numbered``: Source labs that match ``lab-NN_*.md``
          and are not marked as follow-ups.
        - ``source_labs_supplemental``: Source labs that exist alongside a
          numbered protocol (e.g. ``lab-14_microbiology-followup.md``).
        - ``formats_checked``: Formats that were tallied for lab outputs.
        - ``output_files``: Dict mapping format to count of rendered files.
        - ``dashboards``: Number of dashboard HTML files.
        - ``missing_outputs``: List of lab stems missing any rendered output.
        - ``issues``: List of issues found.
    """
    result: Dict[str, Any] = {
        "source_labs": 0,
        "source_labs_numbered": 0,
        "source_labs_supplemental": 0,
        "formats_checked": [],
        "formats_skipped": [],
        "output_files": {},
        "dashboards": 0,
        "missing_outputs": [],
        "issues": [],
    }

    labs_dir = course_path / "course" / "labs"
    if not labs_dir.exists():
        return result

    lab_formats = config.get_lab_output_formats(formats)
    result["formats_checked"] = lab_formats
    if formats is not None:
        result["formats_skipped"] = [fmt for fmt in formats if fmt not in lab_formats]

    all_source_labs = sorted(labs_dir.glob("lab-*.md"))

    if max_lab is not None:
        in_scope: List[Path] = []
        for lab in all_source_labs:
            lab_number, _ = _classify_lab_file(lab)
            # Supplemental files (no number, or number ≤ max_lab) are kept
            # alongside their numbered parent within scope.
            if lab_number is None or lab_number <= max_lab:
                in_scope.append(lab)
        source_labs = in_scope
    else:
        source_labs = all_source_labs

    numbered = 0
    supplemental = 0
    for lab in source_labs:
        _, is_numbered = _classify_lab_file(lab)
        if is_numbered:
            numbered += 1
        else:
            supplemental += 1

    result["source_labs"] = len(source_labs)
    result["source_labs_numbered"] = numbered
    result["source_labs_supplemental"] = supplemental

    output_dir = labs_dir / "output"
    if output_dir.exists():
        for fmt in lab_formats:
            count = 0
            fmt_dir = output_dir / fmt
            if fmt_dir.exists():
                count += len(list(fmt_dir.glob(f"*.{fmt}")))
            count += len(list(output_dir.glob(f"*.{fmt}")))
            result["output_files"][fmt] = count
    else:
        for fmt in lab_formats:
            result["output_files"][fmt] = 0
        if source_labs:
            result["issues"].append("Lab output directory not found")

    for lab_file in source_labs:
        lab_stem = lab_file.stem
        has_output = False
        if output_dir.exists():
            for fmt in lab_formats:
                fmt_dir = output_dir / fmt
                if fmt_dir.exists():
                    rendered = fmt_dir / f"{lab_stem}.{fmt}"
                    if rendered.exists() and rendered.stat().st_size > 0:
                        has_output = True
                        break
                flat_rendered = output_dir / f"{lab_stem}.{fmt}"
                if flat_rendered.exists() and flat_rendered.stat().st_size > 0:
                    has_output = True
                    break
        if not has_output:
            result["missing_outputs"].append(lab_stem)

    dashboards_dir = labs_dir / "dashboards"
    if dashboards_dir.exists():
        dashboard_files = list(dashboards_dir.glob("*.html"))
        result["dashboards"] = len(dashboard_files)
    elif source_labs:
        result["issues"].append("Dashboards directory not found")

    return result


def check_dashboard_invariant(
    course_path: Path,
    course_name: Optional[str] = None,
    max_lab: Optional[int] = None,
) -> Dict[str, Any]:
    """Strict per-numbered-lab dashboard check.

    For each numbered protocol ``lab-NN_*.md`` in ``course/labs/`` (with
    ``NN`` ≤ ``max_lab`` when supplied), verify that
    ``course/labs/dashboards/`` contains the expected number of
    ``lab-NN_*-dashboard.html`` files according to the course's
    ``dashboards`` config (default 1, with per-course overrides such as
    BIOL-8 Lab 15 = 2).

    This invariant is **opt-in** — call it from `validate_outputs` only
    when the caller asks for strict dashboard validation, so other course
    layouts that legitimately diverge are not broken.

    Args:
        course_path: Path to the course directory (e.g. ``course_development/biol-1``).
        course_name: Course identifier for config lookup; defaults to
            ``course_path.name``.
        max_lab: Optional cap on numbered labs to check.

    Returns:
        Dict with:

        - ``valid`` (bool): whether all in-scope labs satisfy the invariant.
        - ``per_lab`` ({int: {"expected": int, "found": int, "files": [str]}}):
            per-lab counts and discovered dashboard filenames.
        - ``issues`` (List[str]): human-readable mismatch descriptions.
        - ``checked_labs`` (List[int]): lab numbers actually evaluated.
        - ``exempt_labs`` (List[int]): lab numbers skipped via config.
    """
    import re

    name = course_name or course_path.name
    cfg = config.get_dashboard_config(name)
    default_per_lab = cfg["default_per_lab"]
    overrides = {int(k): int(v) for k, v in cfg["overrides"].items()}
    exempt = {int(n) for n in cfg["exempt"]}

    result: Dict[str, Any] = {
        "valid": True,
        "per_lab": {},
        "issues": [],
        "checked_labs": [],
        "exempt_labs": sorted(exempt),
    }

    labs_dir = course_path / "course" / "labs"
    dashboards_dir = labs_dir / "dashboards"

    if not labs_dir.exists():
        return result

    numbered_labs: Dict[int, Path] = {}
    for lab_path in sorted(labs_dir.glob("lab-*.md")):
        lab_number, is_numbered = _classify_lab_file(lab_path)
        if not is_numbered or lab_number is None:
            continue
        if max_lab is not None and lab_number > max_lab:
            continue
        # Multiple .md files for the same NN are unusual; keep the first.
        numbered_labs.setdefault(lab_number, lab_path)

    if not numbered_labs:
        return result

    if not dashboards_dir.exists():
        result["valid"] = False
        result["issues"].append(
            "Strict dashboard check: dashboards/ directory not found"
        )
        return result

    dashboard_files = sorted(dashboards_dir.glob("*-dashboard.html"))

    for lab_number in sorted(numbered_labs):
        if lab_number in exempt:
            continue

        expected = overrides.get(lab_number, default_per_lab)
        prefix = re.compile(rf"^lab-0*{lab_number}_.*-dashboard\.html$")
        matches = [f for f in dashboard_files if prefix.match(f.name)]
        found = len(matches)

        result["checked_labs"].append(lab_number)
        result["per_lab"][lab_number] = {
            "expected": expected,
            "found": found,
            "files": [m.name for m in matches],
        }

        if found != expected:
            result["valid"] = False
            if found == 0:
                msg = (
                    f"Strict dashboard check: lab-{lab_number:02d} expects "
                    f"{expected} dashboard(s), found none"
                )
            elif found < expected:
                msg = (
                    f"Strict dashboard check: lab-{lab_number:02d} expects "
                    f"{expected} dashboard(s), found {found} ({', '.join(m.name for m in matches)})"
                )
            else:
                msg = (
                    f"Strict dashboard check: lab-{lab_number:02d} expects "
                    f"{expected} dashboard(s), found {found} extras "
                    f"({', '.join(m.name for m in matches)})"
                )
            result["issues"].append(msg)

    return result
