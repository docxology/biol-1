"""Configuration for batch processing."""

from src.shared.course_config import SUPPORTED_OUTPUT_FORMATS

# File patterns to process
MARKDOWN_PATTERNS: list[str] = ["*.md", "*.markdown"]
AUDIO_PATTERNS: list[str] = ["*.mp3", "*.wav", "*.m4a"]

# Directories to skip
SKIP_DIRECTORIES: list[str] = [".git", "__pycache__", ".pytest_cache", ".venv"]

# Output directory names
OUTPUT_DIRECTORIES: dict[str, str] = {
    "pdf": "pdf_output",
    "audio": "audio_output",
    "text": "text_output",
    "media": "media_output",
}

# Compatibility constants for older callers. Runtime course selection and the
# default "all" format set are resolved from publish.toml.
SUPPORTED_COURSES: list[str] = ["biol-1"]
AVAILABLE_COURSES: list[str] = ["biol-1"]
# Direct library calls must be deterministic and offline by default. Audio
# narration invokes external/local speech tooling and is opt-in through an
# explicit ``formats=[..., "mp3"]`` request or publish.toml.
AVAILABLE_FORMATS: list[str] = [fmt for fmt in SUPPORTED_OUTPUT_FORMATS if fmt != "mp3"]

# File selection patterns for batch processing
SAMPLE_FILE_PREFIX: str = "sample_"

# Content type patterns that map filenames to study-guide output subdirectory
CONTENT_TYPE_PATTERNS: list[str] = ["key-points", "practice-quiz", "comprehension-questions"]
QUESTIONS_FILENAME: str = "questions.md"
