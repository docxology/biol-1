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
