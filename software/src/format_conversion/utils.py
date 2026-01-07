"""Utility functions for format conversion."""

from pathlib import Path
from typing import Optional

from ..markdown_to_pdf.main import render_markdown_to_pdf


def get_file_extension(file_path: Path) -> str:
    """Get file extension (lowercase, without dot).

    Args:
        file_path: Path to file

    Returns:
        File extension without dot
    """
    return file_path.suffix.lower().lstrip(".")


def ensure_output_directory(output_path: Path) -> None:
    """Ensure output directory exists.

    Args:
        output_path: Path to output file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)


def get_output_path(
    input_path: Path, output_format: str, output_dir: Optional[Path] = None
) -> Path:
    """Get output file path from input path and format.

    Args:
        input_path: Path to input file
        output_format: Target format (without dot)
        output_dir: Optional output directory (if None, uses input directory)

    Returns:
        Path to output file
    """
    if output_dir is None:
        output_dir = input_path.parent

    output_filename = input_path.stem + "." + output_format
    return output_dir / output_filename


def convert_markdown_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert Markdown file to PDF.

    Args:
        input_path: Path to input Markdown file
        output_path: Path to output PDF file
    """
    render_markdown_to_pdf(str(input_path), str(output_path))


def convert_markdown_to_html(input_path: Path, output_path: Path) -> None:
    """Convert Markdown file to HTML.

    Args:
        input_path: Path to input Markdown file
        output_path: Path to output HTML file
    """
    from ..markdown_to_pdf.utils import markdown_to_html, read_markdown_file

    markdown_content = read_markdown_file(input_path)
    html_content = markdown_to_html(markdown_content)

    # Add basic HTML structure
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{input_path.stem}</title>
</head>
<body>
{html_content}
</body>
</html>"""

    output_path.write_text(full_html, encoding="utf-8")


def convert_html_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert HTML file to PDF.

    Args:
        input_path: Path to input HTML file
        output_path: Path to output PDF file
    """
    from weasyprint import HTML

    html_content = input_path.read_text(encoding="utf-8")
    HTML(string=html_content).write_pdf(output_path)


def convert_text_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert text file to PDF.

    Args:
        input_path: Path to input text file
        output_path: Path to output PDF file
    """
    from weasyprint import HTML

    text_content = input_path.read_text(encoding="utf-8")
    # Escape HTML and wrap in pre tag
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        pre {{ font-family: monospace; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <pre>{text_content}</pre>
</body>
</html>"""
    HTML(string=html_content).write_pdf(output_path)


def convert_text_to_html(input_path: Path, output_path: Path) -> None:
    """Convert text file to HTML.

    Args:
        input_path: Path to input text file
        output_path: Path to output HTML file
    """
    text_content = input_path.read_text(encoding="utf-8")
    # Escape HTML and wrap in pre tag
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{input_path.stem}</title>
</head>
<body>
    <pre>{text_content}</pre>
</body>
</html>"""
    output_path.write_text(html_content, encoding="utf-8")


def convert_markdown_to_docx(input_path: Path, output_path: Path) -> None:
    """Convert Markdown file to DOCX.

    Args:
        input_path: Path to input Markdown file
        output_path: Path to output DOCX file
    """
    from docx import Document
    from docx.shared import Inches

    from ..markdown_to_pdf.utils import markdown_to_html, read_markdown_file

    # Read and convert Markdown to HTML first
    markdown_content = read_markdown_file(input_path)
    html_content = markdown_to_html(markdown_content)

    # Create DOCX document
    doc = Document()

    # Parse HTML and add to document
    # For simplicity, we'll extract text from HTML
    from html.parser import HTMLParser

    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self.current_para = []

        def handle_data(self, data):
            self.current_para.append(data.strip())

        def handle_endtag(self, tag):
            if tag in ["p", "h1", "h2", "h3", "h4", "h5", "h6"]:
                text = " ".join(self.current_para).strip()
                if text:
                    self.text.append(text)
                self.current_para = []

    parser = TextExtractor()
    parser.feed(html_content)

    # Add paragraphs to document
    for text in parser.text:
        if text:
            doc.add_paragraph(text)

    doc.save(str(output_path))


def convert_pdf_to_text(input_path: Path, output_path: Path) -> None:
    """Convert PDF file to text.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output text file
    """
    from pypdf import PdfReader

    reader = PdfReader(str(input_path))
    text_content = []

    for page in reader.pages:
        text_content.append(page.extract_text())

    full_text = "\n\n".join(text_content)
    output_path.write_text(full_text, encoding="utf-8")


def convert_audio_to_text(input_path: Path, output_path: Path) -> None:
    """Convert audio file to text using speech-to-text.

    Args:
        input_path: Path to input audio file
        output_path: Path to output text file
    """
    from ..speech_to_text.main import transcribe_audio

    transcribe_audio(str(input_path), str(output_path))


def get_conversion_path(input_path: str, output_format: str) -> str:
    """Generate output path for file conversion.

    Args:
        input_path: Path to input file
        output_format: Target format (without dot)

    Returns:
        Output file path with new extension
    """
    input_file = Path(input_path)
    output_file = input_file.with_suffix(f".{output_format}")
    return str(output_file)
