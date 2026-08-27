"""Utility functions for Markdown to PDF conversion."""

import ctypes
import ctypes.util
import os
from pathlib import Path

import markdown

# WeasyPrint's macOS wheels require the GTK/Pango shared libraries. Homebrew
# installs them under /opt/homebrew/lib (Apple Silicon) or /usr/local/lib
# (Intel); add those locations before importing the CFFI bindings.
for _library_dir in ("/opt/homebrew/lib", "/usr/local/lib"):
    if os.path.isdir(_library_dir):
        _existing = os.environ.get("DYLD_LIBRARY_PATH", "")
        if _library_dir not in _existing.split(":"):
            os.environ["DYLD_LIBRARY_PATH"] = ":".join(
                part for part in (_library_dir, _existing) if part
            )
        break

# CFFI does not consult DYLD_LIBRARY_PATH for these macOS names reliably;
# preload the Homebrew dylibs globally so their transitive dependencies resolve.
for _library_name in (
    "libgobject-2.0.dylib",
    "libpango-1.0.dylib",
    "libpangocairo-1.0.dylib",
    "libcairo.2.dylib",
    "libgdk_pixbuf-2.0.dylib",
    "libpangoft2-1.0.dylib",
    "libharfbuzz.dylib",
    "libfontconfig.1.dylib",
    "libfreetype.6.dylib",
):
    for _library_dir in ("/opt/homebrew/lib", "/usr/local/lib"):
        _library_path = Path(_library_dir) / _library_name
        if _library_path.exists():
            ctypes.CDLL(str(_library_path), mode=ctypes.RTLD_GLOBAL)
            break

from weasyprint import CSS, HTML  # noqa: E402

from src.shared.pdf_font_config import FONT_CONFIG  # noqa: E402


def markdown_to_html(markdown_text: str, extensions: list[str] | None = None) -> str:
    """Convert Markdown text to HTML.

    Args:
        markdown_text: Markdown content
        extensions: List of Markdown extensions to use

    Returns:
        HTML content
    """
    if extensions is None:
        extensions = [
            "extra",
            "codehilite",
            "tables",
            "fenced_code",
        ]

    md = markdown.Markdown(extensions=extensions)
    html_content = md.convert(markdown_text)

    return html_content


def html_to_pdf(html_content: str, css_content: str, output_path: Path) -> None:
    """Convert HTML content to PDF.

    Args:
        html_content: HTML content
        css_content: CSS styling
        output_path: Path for output PDF file

    Raises:
        OSError: If PDF generation fails
    """
    try:
        html_doc = HTML(string=html_content)
        css_doc = CSS(string=css_content)
        html_doc.write_pdf(output_path, stylesheets=[css_doc], font_config=FONT_CONFIG)
    except Exception as e:
        raise OSError(f"Failed to generate PDF: {e}") from e


def get_output_path(input_path: Path, output_dir: Path | None = None) -> Path:
    """Get output PDF path from input Markdown path.

    Args:
        input_path: Path to input Markdown file
        output_dir: Optional output directory (if None, uses input directory)

    Returns:
        Path to output PDF file
    """
    if output_dir is None:
        output_dir = input_path.parent

    output_filename = input_path.stem + ".pdf"
    return output_dir / output_filename
