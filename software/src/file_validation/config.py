"""Configuration for file validation."""

import re
from typing import List, Pattern

# Required files in each active BIOL-1-style module
REQUIRED_FILES: List[str] = [
    "README.md",
    "AGENTS.md",
    "questions.md",
    "keys-to-success.md",
]

# Required directories in each module. BIOL-1 modules do not require an
# assignments/ directory; assignment naming checks remain opt-in when that
# legacy folder exists.
REQUIRED_DIRECTORIES: List[str] = []

# Root-level content files that use stable BIOL-1 names instead of module
# prefixes. They are rendered to standardized output names by the pipeline.
ROOT_CONTENT_FILES: List[str] = ["questions.md", "keys-to-success.md"]

# Naming convention patterns
KEBAB_CASE_PATTERN: Pattern[str] = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Module prefix pattern (e.g., "module-1-assignment-1")
MODULE_PREFIX_PATTERN: Pattern[str] = re.compile(r"^module-\d+-")

# Valid file extensions for course materials
VALID_EXTENSIONS: List[str] = [
    ".md",
    ".pdf",
    ".pptx",
    ".docx",
    ".txt",
    ".html",
]

# Assignment naming pattern
ASSIGNMENT_PATTERN: Pattern[str] = re.compile(
    r"^module-\d+-assignment-\d+(-[a-z0-9-]+)?\.(md|pdf)$"
)

# Lecture naming pattern
LECTURE_PATTERN: Pattern[str] = re.compile(
    r"^module-\d+-lecture-[a-z0-9-]+\.(pdf|pptx)$"
)

# Lab protocol naming pattern
LAB_PATTERN: Pattern[str] = re.compile(
    r"^module-\d+-lab-\d+-[a-z0-9-]+\.md$"
)

# Study guide naming pattern
STUDY_GUIDE_PATTERN: Pattern[str] = re.compile(r"^module-\d+-study-guide\.(md|pdf)$")

# Quiz naming pattern
QUIZ_PATTERN: Pattern[str] = re.compile(r"^module-\d+-quiz\.(md|pdf)$")
