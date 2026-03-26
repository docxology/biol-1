"""Main functions for format conversion."""

import logging
from pathlib import Path
from typing import Dict, List

from . import config

logger = logging.getLogger(__name__)
from .utils import (
    convert_html_to_pdf,
    convert_markdown_to_html,
    convert_markdown_to_pdf,
    convert_text_to_html,
    convert_text_to_pdf,
    get_conversion_path,
    get_file_extension,
    get_output_path,
)
from src.shared.file_utils import ensure_output_directory


def convert_file(input_path: str, output_format: str, output_path: str) -> None:
    """Convert a file from one format to another.

    Args:
        input_path: Path to input file
        output_format: Target format (e.g., "pdf", "docx")
        output_path: Path for output file

    Raises:
        ValueError: If conversion is not supported
        FileNotFoundError: If input file doesn't exist
        OSError: If conversion fails
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    input_ext = get_file_extension(input_file)
    output_format_lower = output_format.lower()

    # Check if conversion is supported
    if input_ext not in config.SUPPORTED_CONVERSIONS:
        raise ValueError(f"Unsupported input format: {input_ext}")

    if output_format_lower not in config.SUPPORTED_CONVERSIONS[input_ext]:
        raise ValueError(
            f"Conversion from {input_ext} to {output_format_lower} is not supported"
        )

    ensure_output_directory(output_file)

    # Perform conversion based on formats
    conversion_key = f"{input_ext}->{output_format_lower}"

    if conversion_key == "md->pdf" or conversion_key == "markdown->pdf":
        convert_markdown_to_pdf(input_file, output_file)
    elif conversion_key == "md->html" or conversion_key == "markdown->html":
        convert_markdown_to_html(input_file, output_file)
    elif conversion_key == "md->docx" or conversion_key == "markdown->docx":
        from .utils import convert_markdown_to_docx
        convert_markdown_to_docx(input_file, output_file)
    elif conversion_key == "html->pdf":
        convert_html_to_pdf(input_file, output_file)
    elif conversion_key == "txt->pdf":
        convert_text_to_pdf(input_file, output_file)
    elif conversion_key == "txt->html":
        convert_text_to_html(input_file, output_file)
    elif conversion_key == "pdf->txt":
        from .utils import convert_pdf_to_text
        convert_pdf_to_text(input_file, output_file)
    elif conversion_key in ["mp3->txt", "wav->txt", "m4a->txt"]:
        from .utils import convert_audio_to_text
        convert_audio_to_text(input_file, output_file)
    else:
        raise ValueError(f"Conversion handler not implemented: {conversion_key}")


def batch_convert(
    directory: str, input_format: str, output_format: str
) -> List[str]:
    """Batch convert files in a directory.

    Args:
        directory: Directory containing files to convert
        input_format: Source file format
        output_format: Target file format

    Returns:
        List of output file paths

    Raises:
        ValueError: If directory doesn't exist or conversion is not supported
        OSError: If conversion fails for any file
    """
    source_dir = Path(directory)
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Directory does not exist: {directory}")

    input_format_lower = input_format.lower()
    output_format_lower = output_format.lower()

    # Check if conversion is supported
    if input_format_lower not in config.SUPPORTED_CONVERSIONS:
        raise ValueError(f"Unsupported input format: {input_format_lower}")

    if output_format_lower not in config.SUPPORTED_CONVERSIONS[input_format_lower]:
        raise ValueError(
            f"Conversion from {input_format_lower} to {output_format_lower} is not supported"
        )

    output_files = []

    # Find all files with matching extension
    pattern = f"*.{input_format_lower}"
    if input_format_lower == "md":
        # Also match .markdown
        files = list(source_dir.glob("*.md")) + list(source_dir.glob("*.markdown"))
    else:
        files = list(source_dir.glob(pattern))

    for input_file in files:
        try:
            output_path = get_output_path(input_file, output_format_lower, source_dir)
            convert_file(str(input_file), output_format_lower, str(output_path))
            output_files.append(str(output_path))
        except Exception as e:
            # Log error but continue with other files
            logger.error("Error converting %s: %s", input_file, e, exc_info=True)
            continue

    return output_files


def get_supported_formats() -> Dict[str, list]:
    """Get list of supported file formats.

    Returns:
        Dictionary mapping input formats to supported output formats
    """
    return config.SUPPORTED_CONVERSIONS.copy()


