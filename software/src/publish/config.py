"""Configuration for the publish module."""

from pathlib import Path

# Root directory name for published content (relative to repo root)
PUBLISH_ROOT_NAME = "PUBLISHED"

# Configuration for specific courses
# Key: Course directory name
# Value: Dict with 'module_source_dir' and 'syllabus_source_dir'
COURSE_CONFIGS = {
    "biol-1": {
        "module_source_dir": "for_upload",
        "syllabus_source_dir": "output",
        "include_syllabus": True,
    },
    "biol-8": {
        "module_source_dir": "output",
        "syllabus_source_dir": "output",
        "include_syllabus": True,
    },
}

# Default configuration for other courses
DEFAULT_CONFIG = {
    "module_source_dir": "output",
    "syllabus_source_dir": "output",
    "include_syllabus": True,
}

# Subdirectories to exclude during copy
EXCLUDE_PATTERNS = [
    ".DS_Store",
    "Thumbs.db",
    "__pycache__",
    ".git",
]
