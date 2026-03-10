"""Shared file utility functions used across multiple modules."""

from pathlib import Path
from typing import List


def ensure_output_directory(output_path: Path) -> None:
    """Ensure output directory exists, creating it if necessary.

    Handles both file paths (creates parent dir) and directory paths.

    Args:
        output_path: Path to output file or directory
    """
    if output_path.suffix:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path.mkdir(parents=True, exist_ok=True)


def read_markdown_file(file_path: Path) -> str:
    """Read markdown file content.

    Args:
        file_path: Path to markdown file

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


def find_files(directory: Path, patterns: List[str]) -> List[Path]:
    """Find files matching any of the given glob patterns recursively.

    Args:
        directory: Directory to search
        patterns: List of glob patterns (e.g. ["*.md", "*.markdown"])

    Returns:
        Sorted list of matching file paths
    """
    found: List[Path] = []
    for pattern in patterns:
        found.extend(directory.rglob(pattern))
    return sorted(found)
