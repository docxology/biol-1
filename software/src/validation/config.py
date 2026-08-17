"""Configuration for validation module."""

from typing import Any

from src.shared.course_config import SUPPORTED_OUTPUT_FORMATS, validate_supported_formats

# All supported output formats
ALL_SUPPORTED_FORMATS = list(SUPPORTED_OUTPUT_FORMATS)

# Default required formats when no --formats specified (minimum viable output)
DEFAULT_REQUIRED_FORMATS = ["pdf", "docx"]

# Format-aware validation: These are the base file types (without extension)
STUDY_GUIDE_BASE_TYPES = ["key-points", "practice-quiz", "questions"]

# Optional study guide files (not counted toward validity)
OPTIONAL_STUDY_GUIDE_FILES = [
    "key-points.mp3",
    "questions.mp3",
]


def get_expected_study_guide_files(formats: list[str] | None = None) -> list[str]:
    """Get expected study guide files based on requested formats.

    Args:
        formats: List of format extensions to validate (e.g., ["pdf", "docx", "md"])
                 If None, uses DEFAULT_REQUIRED_FORMATS

    Returns:
        List of expected file suffixes like ["key-points.pdf", "practice-quiz.pdf", ...]
    """
    if formats is None:
        formats = DEFAULT_REQUIRED_FORMATS
    else:
        formats = validate_supported_formats(formats)

    # Filter to only formats that produce study guide files (not md which is just a copy)
    renderable_formats = [f for f in formats if f in ["pdf", "docx", "html", "txt"]]

    files = []
    for base_type in STUDY_GUIDE_BASE_TYPES:
        for fmt in renderable_formats:
            files.append(f"{base_type}.{fmt}")

    return files


# Syllabus format configuration
SYLLABUS_REQUIRED_FORMATS = ["pdf", "docx"]  # Minimum for syllabus
SYLLABUS_OPTIONAL_FORMATS = ["html", "txt", "mp3", "md"]  # Nice to have


def get_syllabus_required_formats(formats: list[str] | None = None) -> list[str]:
    """Get required syllabus formats based on requested formats.

    Args:
        formats: List of format extensions requested (e.g., ["pdf", "docx", "md"])
                 If None, uses SYLLABUS_REQUIRED_FORMATS

    Returns:
        List of formats to require for syllabus validation
    """
    if formats is None:
        return SYLLABUS_REQUIRED_FORMATS
    formats = validate_supported_formats(formats)

    # Only require formats that were actually requested AND are renderable
    renderable = ["pdf", "docx", "html", "txt"]
    return [f for f in formats if f in renderable]


# Expected website files
EXPECTED_WEBSITE_FILES = ["index.html"]

# Output directories
OUTPUT_DIRS = {
    "study_guides": "study-guides",
    "website": "website",
    "labs": "labs",
    "dashboards": "dashboards",
}

# Lab output formats: the canonical course export is a printable PDF only.
LAB_OUTPUT_FORMATS = ["pdf"]

# The lab pipeline deliberately does not publish HTML. The low-level lab
# renderer may still use HTML internally to construct the PDF.
LAB_RENDERABLE_FORMATS = ["pdf"]


def get_lab_output_formats(formats: list[str] | None = None) -> list[str]:
    """Resolve the lab output formats to validate.

    Args:
        formats: List of requested formats (e.g. ["pdf", "docx", "md"]).
                 If None, falls back to LAB_OUTPUT_FORMATS for backward
                 compatibility with callers that pre-date format threading.

    Returns:
        List of formats that are both requested and renderable for labs.
        Order is preserved from the input list.
    """
    if formats is None:
        return list(LAB_OUTPUT_FORMATS)
    renderable = set(LAB_RENDERABLE_FORMATS)
    return [f for f in formats if f in renderable]


# Course configurations
#
# `dashboards` describes the **strict** per-numbered-lab invariant that
# `check_dashboard_invariant` enforces when `strict_dashboards=True`:
#   - default_per_lab: required dashboards for each numbered protocol unless
#     listed in `overrides` or `exempt`.
#   - overrides: {lab_number: required_count} for labs that ship more (or
#     fewer) than the default. BIOL-8's Lab 15 ships two — one for the
#     cardiovascular and one for the respiratory portion of the lab.
#   - exempt: lab numbers that are intentionally undocumented in the
#     dashboard set (typically because the only `lab-NN_*.md` is a
#     supplemental/follow-up page).
COURSE_CONFIG: dict[str, dict[str, Any]] = {
    "biol-1": {
        "expected_modules": 16,
        "module_prefix": "module-",
        "dashboards": {
            "default_per_lab": 1,
            "overrides": {},
            "exempt": [],
        },
    },
    "biol-8": {
        "expected_modules": 17,
        "module_prefix": "module-",
        "dashboards": {
            "default_per_lab": 1,
            "overrides": {15: 2},
            "exempt": [],
        },
    },
}


def get_dashboard_config(course_name: str) -> dict[str, Any]:
    """Return the per-course dashboard invariant config (defaults if missing).

    Args:
        course_name: Course directory name (e.g. ``biol-8``).

    Returns:
        Dict with ``default_per_lab`` (int), ``overrides`` ({int: int}),
        and ``exempt`` (List[int]). Returns sensible defaults for unknown
        courses so the strict check degrades gracefully.
    """
    course_cfg = COURSE_CONFIG.get(course_name, {})
    raw = course_cfg.get("dashboards", {}) or {}
    return {
        "default_per_lab": int(raw.get("default_per_lab", 1)),
        "overrides": dict(raw.get("overrides", {}) or {}),
        "exempt": list(raw.get("exempt", []) or []),
    }


# Published directory name
PUBLISHED_DIR_NAME = "PUBLISHED"

# Logging configuration
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
