"""Configuration for batch processing."""

from typing import Dict, List

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

# Supported course directory names
SUPPORTED_COURSES: List[str] = ["biol-1", "biol-8"]

# Available courses with their directory paths (relative to repo root)
AVAILABLE_COURSES: List[str] = ["biol-1", "biol-8"]

# Available output formats
AVAILABLE_FORMATS: List[str] = ["pdf", "mp3", "docx", "html", "txt"]

# File selection patterns for batch processing
SAMPLE_FILE_PREFIX: str = "sample_"

# Content type patterns that map filenames to study-guide output subdirectory
CONTENT_TYPE_PATTERNS: List[str] = ["keys-to-success", "comprehension-questions"]
QUESTIONS_FILENAME: str = "questions.md"
