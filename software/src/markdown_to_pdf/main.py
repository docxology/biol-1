"""Main functions for Markdown to PDF conversion."""

import logging
from pathlib import Path
from typing import Any

from src.assessment_layout import build_tearoff_assessment
from src.shared.file_utils import ensure_output_directory, read_markdown_file

from . import config
from .utils import (
    get_output_path,
    html_to_pdf,
    markdown_to_html,
)

logger = logging.getLogger(__name__)


def render_markdown_to_pdf(
    input_path: str,
    output_path: str,
    css_content: str | None = None,
    pdf_options: dict[str, Any] | None = None,
) -> None:
    """Convert a Markdown file to PDF format.

    Args:
        input_path: Path to input Markdown file
        output_path: Path for output PDF file
        css_content: Optional custom CSS content (uses default if None)
        pdf_options: Optional PDF options (uses default if None)

    Raises:
        FileNotFoundError: If input file doesn't exist
        OSError: If PDF generation fails
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    ensure_output_directory(output_file)

    # Read Markdown file
    markdown_content = read_markdown_file(input_file)

    # Assessment sources opt into a duplex layout with a tear-off answer sheet.
    if "assessment-layout: tearoff-duplex" in markdown_content:
        html_content = build_tearoff_assessment(markdown_content)
    else:
        # Convert Markdown to HTML
        html_content = markdown_to_html(markdown_content)

    # Use default CSS if not provided
    if css_content is None:
        css_content = config.DEFAULT_CSS

    # Generate PDF
    html_to_pdf(html_content, css_content, output_file)


def batch_render_markdown(directory: str, output_dir: str) -> list[str]:
    """Batch convert all Markdown files in a directory to PDF.

    Args:
        directory: Directory containing Markdown files
        output_dir: Output directory for PDF files

    Returns:
        List of output file paths

    Raises:
        ValueError: If directory doesn't exist
        OSError: If PDF generation fails for any file
    """
    source_dir = Path(directory)
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Directory does not exist: {directory}")

    output_directory = Path(output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    output_files = []

    # Find all Markdown files
    markdown_files = list(source_dir.glob("*.md")) + list(source_dir.glob("*.markdown"))

    for md_file in markdown_files:
        try:
            output_path = get_output_path(md_file, output_directory)
            render_markdown_to_pdf(str(md_file), str(output_path))
            output_files.append(str(output_path))
        except Exception as e:
            # Log error but continue with other files
            logger.error("Error converting %s: %s", md_file, e)
            continue

    return output_files


def configure_pdf_options(template: str, options: dict[str, Any]) -> dict[str, Any]:
    """Configure PDF rendering options.

    Args:
        template: Template name (currently only "default" is supported)
        options: Dictionary of rendering options to override defaults

    Returns:
        Configured options dictionary

    Raises:
        ValueError: If template is invalid
    """
    if template != "default":
        raise ValueError(f"Unknown template: {template}")

    # Start with default options
    configured = config.DEFAULT_PDF_OPTIONS.copy()

    # Override with provided options
    configured.update(options)

    return configured
