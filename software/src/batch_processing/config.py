"""Configuration for batch processing."""

from typing import Dict, List

from src.shared.course_config import SUPPORTED_OUTPUT_FORMATS

# File patterns to process
MARKDOWN_PATTERNS: List[str] = ["*.md", "*.markdown"]
AUDIO_PATTERNS: List[str] = ["*.mp3", "*.wav", "*.m4a"]

# Directories to skip
SKIP_DIRECTORIES: List[str] = [".git", "__pycache__", ".pytest_cache", ".venv"]

# Output directory names
OUTPUT_DIRECTORIES: Dict[str, str] = {
    "pdf": "pdf_output",
    "audio": "audio_output",
    "text": "text_output",
    "media": "media_output",
}

# Compatibility constants for older callers. Runtime course selection and the
# default "all" format set are resolved from publish.toml.
SUPPORTED_COURSES: List[str] = ["biol-1"]
AVAILABLE_COURSES: List[str] = ["biol-1"]
AVAILABLE_FORMATS: List[str] = list(SUPPORTED_OUTPUT_FORMATS)

# File selection patterns for batch processing
SAMPLE_FILE_PREFIX: str = "sample_"

# Content type patterns that map filenames to study-guide output subdirectory
CONTENT_TYPE_PATTERNS: List[str] = ["keys-to-success", "comprehension-questions"]
QUESTIONS_FILENAME: str = "questions.md"
