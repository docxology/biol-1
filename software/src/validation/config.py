"""Configuration for validation module."""

from pathlib import Path
from typing import Dict, List

# Expected output formats
EXPECTED_FORMATS = ["pdf", "docx", "html", "txt", "mp3"]

# Required study guide files per module (MP3 is optional)
EXPECTED_STUDY_GUIDE_FILES = [
    "keys-to-success.pdf",
    "keys-to-success.docx",
    "keys-to-success.html",
    "keys-to-success.txt",
    "questions.pdf",
    "questions.docx",
    "questions.html",
    "questions.txt",
]

# Optional study guide files (not counted toward validity)
OPTIONAL_STUDY_GUIDE_FILES = [
    "keys-to-success.mp3",
    "questions.mp3",
]

# Expected website files
EXPECTED_WEBSITE_FILES = ["index.html"]

# Output directories
OUTPUT_DIRS = {
    "study_guides": "study-guides",
    "website": "website",
    "labs": "labs",
    "dashboards": "dashboards",
}

# Lab output formats (labs support PDF and HTML rendering)
LAB_OUTPUT_FORMATS = ["pdf", "html"]

# Course configurations
COURSE_CONFIG: Dict[str, Dict] = {
    "biol-1": {
        "expected_modules": 17,
        "module_prefix": "module-",
    },
    "biol-8": {
        "expected_modules": 15,
        "module_prefix": "module-",
    },
}

# Syllabus expected outputs
SYLLABUS_EXPECTED_FORMATS = ["pdf", "docx", "html", "txt", "mp3"]

# Published directory name
PUBLISHED_DIR_NAME = "PUBLISHED"

# Logging configuration
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
