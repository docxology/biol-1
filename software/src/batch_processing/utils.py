"""Utility functions for batch processing."""

from pathlib import Path
from typing import List


def find_markdown_files(directory: Path) -> List[Path]:
    """Find all Markdown files in a directory recursively.

    Args:
        directory: Directory to search

    Returns:
        List of Markdown file paths
    """
    markdown_files = []
    for pattern in ["*.md", "*.markdown"]:
        markdown_files.extend(directory.rglob(pattern))
    return sorted(markdown_files)


def find_audio_files(directory: Path) -> List[Path]:
    """Find all audio files in a directory recursively.

    Args:
        directory: Directory to search

    Returns:
        List of audio file paths
    """
    audio_files = []
    for pattern in ["*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg"]:
        audio_files.extend(directory.rglob(pattern))
    return sorted(audio_files)


def should_process_file(file_path: Path, skip_dirs: List[str]) -> bool:
    """Check if a file should be processed (not in skip directories).

    Args:
        file_path: Path to file
        skip_dirs: List of directory names to skip

    Returns:
        True if file should be processed, False otherwise
    """
    for part in file_path.parts:
        if part in skip_dirs:
            return False
    return True


def ensure_output_directory(output_dir: Path) -> None:
    """Ensure output directory exists.

    Args:
        output_dir: Path to output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)


def get_relative_output_path(source_file: Path, source_dir: Path, output_dir: Path) -> Path:
    """Get output path maintaining relative structure.

    Args:
        source_file: Source file path
        source_dir: Source directory path
        output_dir: Output directory path

    Returns:
        Output file path maintaining relative structure
    """
    relative_path = source_file.relative_to(source_dir)
    output_file = output_dir / relative_path
    return output_file
