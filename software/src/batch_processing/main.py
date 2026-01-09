"""Main functions for batch processing."""

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import config
from .logging_config import get_logger
from .utils import (
    ensure_output_directory,
    find_audio_files,
    find_markdown_files,
    get_relative_output_path,
    should_process_file,
)
import time

logger = get_logger()


def process_module_to_pdf(module_path: str, output_dir: str) -> List[str]:
    """Convert all Markdown files in a module to PDF.

    Args:
        module_path: Path to module directory
        output_dir: Output directory for PDF files

    Returns:
        List of output PDF file paths

    Raises:
        ValueError: If module path doesn't exist
        OSError: If PDF conversion fails
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    output_directory = Path(output_dir)
    ensure_output_directory(output_directory)

    # Find all Markdown files
    markdown_files = find_markdown_files(module_dir)

    # Filter out files in skip directories
    markdown_files = [
        f for f in markdown_files if should_process_file(f, config.SKIP_DIRECTORIES)
    ]

    output_files = []

    for md_file in markdown_files:
        try:
            # Get output path maintaining structure
            output_file = get_relative_output_path(
                md_file, module_dir, output_directory
            )
            output_file = output_file.with_suffix(".pdf")

            # Ensure output directory exists
            ensure_output_directory(output_file.parent)

            # Convert to PDF
            from ..markdown_to_pdf.main import render_markdown_to_pdf

            render_markdown_to_pdf(str(md_file), str(output_file))
            output_files.append(str(output_file))
        except Exception as e:
            print(f"Error converting {md_file} to PDF: {e}")
            continue

    return output_files


def process_module_to_audio(module_path: str, output_dir: str) -> List[str]:
    """Convert all text/Markdown files in a module to audio.

    Args:
        module_path: Path to module directory
        output_dir: Output directory for audio files

    Returns:
        List of output audio file paths

    Raises:
        ValueError: If module path doesn't exist
        OSError: If audio generation fails
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    output_directory = Path(output_dir)
    ensure_output_directory(output_directory)

    # Find all Markdown and text files
    text_files = find_markdown_files(module_dir)
    text_files.extend(module_dir.rglob("*.txt"))

    # Filter out files in skip directories
    text_files = [
        f for f in text_files if should_process_file(f, config.SKIP_DIRECTORIES)
    ]

    output_files = []

    for text_file in text_files:
        try:
            # Get output path maintaining structure
            output_file = get_relative_output_path(
                text_file, module_dir, output_directory
            )
            output_file = output_file.with_suffix(".mp3")

            # Ensure output directory exists
            ensure_output_directory(output_file.parent)

            # Read and extract text
            from ..text_to_speech.utils import (
                extract_text_from_markdown,
                read_text_file,
            )

            content = read_text_file(text_file)
            if text_file.suffix in [".md", ".markdown"]:
                content = extract_text_from_markdown(content)

            # Generate speech
            from ..text_to_speech.main import generate_speech

            generate_speech(content, str(output_file))
            output_files.append(str(output_file))
        except Exception as e:
            print(f"Error converting {text_file} to audio: {e}")
            continue

    return output_files


def process_module_to_text(module_path: str, output_dir: str) -> List[str]:
    """Transcribe all audio files in a module to text.

    Args:
        module_path: Path to module directory
        output_dir: Output directory for text files

    Returns:
        List of output text file paths

    Raises:
        ValueError: If module path doesn't exist
        OSError: If transcription fails
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    output_directory = Path(output_dir)
    ensure_output_directory(output_directory)

    # Find all audio files
    audio_files = find_audio_files(module_dir)

    # Filter out files in skip directories
    audio_files = [
        f for f in audio_files if should_process_file(f, config.SKIP_DIRECTORIES)
    ]

    output_files = []

    for audio_file in audio_files:
        try:
            # Get output path maintaining structure
            output_file = get_relative_output_path(
                audio_file, module_dir, output_directory
            )
            output_file = output_file.with_suffix(".txt")

            # Ensure output directory exists
            ensure_output_directory(output_file.parent)

            # Transcribe audio
            from ..speech_to_text.main import transcribe_audio

            transcribe_audio(str(audio_file), str(output_file))
            output_files.append(str(output_file))
        except Exception as e:
            print(f"Error transcribing {audio_file}: {e}")
            continue

    return output_files


def generate_module_media(module_path: str, output_dir: str) -> Dict[str, Any]:
    """Generate all media formats for a module (PDF, audio, text transcriptions).

    Args:
        module_path: Path to module directory
        output_dir: Base output directory for all media

    Returns:
        Dictionary with results for each media type:
        - pdf_files: List of generated PDF files
        - audio_files: List of generated audio files
        - text_files: List of generated text transcriptions
        - errors: List of errors encountered

    Raises:
        ValueError: If module path doesn't exist
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    base_output = Path(output_dir)
    ensure_output_directory(base_output)

    results = {
        "pdf_files": [],
        "audio_files": [],
        "text_files": [],
        "errors": [],
    }

    # Generate PDFs
    try:
        pdf_output = base_output / config.OUTPUT_DIRECTORIES["pdf"]
        results["pdf_files"] = process_module_to_pdf(module_path, str(pdf_output))
    except Exception as e:
        results["errors"].append(f"PDF generation error: {e}")

    # Generate audio
    try:
        audio_output = base_output / config.OUTPUT_DIRECTORIES["audio"]
        results["audio_files"] = process_module_to_audio(module_path, str(audio_output))
    except Exception as e:
        results["errors"].append(f"Audio generation error: {e}")

    # Transcribe audio to text
    try:
        text_output = base_output / config.OUTPUT_DIRECTORIES["text"]
        # First generate audio if not already done
        if not results["audio_files"]:
            audio_output = base_output / config.OUTPUT_DIRECTORIES["audio"]
            results["audio_files"] = process_module_to_audio(
                module_path, str(audio_output)
            )
        # Then transcribe the generated audio
        if results["audio_files"]:
            results["text_files"] = process_module_to_text(
                str(audio_output), str(text_output)
            )
    except Exception as e:
        results["errors"].append(f"Text transcription error: {e}")

    return results


def process_module_by_type(module_path: str, output_dir: str) -> Dict[str, Any]:
    """Process module files by curriculum element type and generate all format renderings.

    Organizes outputs by curriculum element type (assignments, lab-protocols,
    lecture-content, study-guides) with all formats (PDF, MP3, DOCX, HTML, TXT).

    Args:
        module_path: Path to module directory
        output_dir: Base output directory for all renderings

    Returns:
        Dictionary with results:
        - by_type: Dict mapping curriculum type to list of generated files
        - summary: Dict with counts of generated files by format
        - errors: List of errors encountered

    Raises:
        ValueError: If module path doesn't exist
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    logger.info(f"Processing module: {module_dir.name}")
    base_output = Path(output_dir)
    ensure_output_directory(base_output)

    # Curriculum element type mapping
    type_mapping = {
        "assignment": "assignments",
        "lab-protocol": "lab-protocols",
        "lecture-content": "lecture-content",
        "study-guide": "study-guides",
    }

    # Find all sample markdown files
    markdown_files = find_markdown_files(module_dir)
    files_to_process = [f for f in markdown_files if f.name.startswith("sample_")]
    
    # Process assignment files
    assignments_dir = module_dir / "assignments"
    if assignments_dir.exists():
        assignment_files = list(assignments_dir.glob("*.md"))
        files_to_process.extend(assignment_files)

    # Process resource files
    resources_dir = module_dir / "resources"
    if resources_dir.exists():
        resource_files = list(resources_dir.glob("*.md"))
        files_to_process.extend(resource_files)

    logger.debug(f"Found {len(files_to_process)} markdown files to process")

    results = {
        "by_type": {t: [] for t in type_mapping.values()},
        "summary": {"pdf": 0, "mp3": 0, "docx": 0, "html": 0, "txt": 0},
        "errors": [],
    }

    for md_file in files_to_process:
        try:
            # Detect curriculum element type from filename
            file_type = None
            output_subdir = None

            if "assignment" in md_file.name:
                file_type = "assignment"
                output_subdir = "assignments"
            elif "lab-protocol" in md_file.name:
                file_type = "lab-protocol"
                output_subdir = "lab-protocols"
            elif "lecture-content" in md_file.name:
                file_type = "lecture-content"
                output_subdir = "lecture-content"
            elif "study-guide" in md_file.name:
                file_type = "study-guide"
                output_subdir = "study-guides"
            elif "keys-to-success" in md_file.name:
                file_type = "study-guide"
                output_subdir = "study-guides"
            elif "comprehension-questions" in md_file.name:
                file_type = "study-guide"
                output_subdir = "study-guides"
            elif "assignment" in md_file.name or md_file.parent.name == "assignments":
                file_type = "assignment"
                output_subdir = "assignments"

            if not output_subdir:
                logger.debug(f"Skipping file (no type match): {md_file.name}")
                continue  # Skip files that don't match known types

            # Create output subdirectory for this type
            type_output_dir = base_output / output_subdir
            ensure_output_directory(type_output_dir)
            logger.debug(f"Processing {file_type}: {md_file.name} -> {output_subdir}/")

            # Base filename without extension
            base_name = md_file.stem

            # Generate PDF
            try:
                pdf_file = type_output_dir / f"{base_name}.pdf"
                from ..markdown_to_pdf.main import render_markdown_to_pdf

                logger.debug(f"Generating PDF: {pdf_file.name}")
                render_markdown_to_pdf(str(md_file), str(pdf_file))
                results["by_type"][output_subdir].append(str(pdf_file))
                results["summary"]["pdf"] += 1
            except Exception as e:
                error_msg = f"PDF generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate Audio (MP3)
            try:
                audio_file = type_output_dir / f"{base_name}.mp3"
                from ..text_to_speech.utils import (
                    extract_text_from_markdown,
                    read_text_file,
                )
                from ..text_to_speech.main import generate_speech
            
                logger.debug(f"Generating MP3: {audio_file.name}")
                content = read_text_file(md_file)
                text_content = extract_text_from_markdown(content)
                generate_speech(text_content, str(audio_file))
                time.sleep(2)  # Add delay to avoid 429 errors
                results["by_type"][output_subdir].append(str(audio_file))
                results["summary"]["mp3"] += 1
            except Exception as e:
                error_msg = f"Audio generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate DOCX
            try:
                docx_file = type_output_dir / f"{base_name}.docx"
                from ..format_conversion.main import convert_file

                logger.debug(f"Generating DOCX: {docx_file.name}")
                convert_file(str(md_file), "docx", str(docx_file))
                results["by_type"][output_subdir].append(str(docx_file))
                results["summary"]["docx"] += 1
            except Exception as e:
                error_msg = f"DOCX generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate HTML
            try:
                html_file = type_output_dir / f"{base_name}.html"
                from ..format_conversion.main import convert_file as convert_file_func
                logger.debug(f"Generating HTML: {html_file.name}")
                convert_file_func(str(md_file), "html", str(html_file))
                results["by_type"][output_subdir].append(str(html_file))
                results["summary"]["html"] += 1
            except Exception as e:
                error_msg = f"HTML generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate TXT (extracted text)
            try:
                txt_file = type_output_dir / f"{base_name}.txt"
                from ..text_to_speech.utils import (
                    extract_text_from_markdown,
                    read_text_file,
                )

                logger.debug(f"Generating TXT: {txt_file.name}")
                content = read_text_file(md_file)
                text_content = extract_text_from_markdown(content)
                txt_file.write_text(text_content, encoding="utf-8")
                results["by_type"][output_subdir].append(str(txt_file))
                results["summary"]["txt"] += 1
            except Exception as e:
                error_msg = f"TXT generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

        except Exception as e:
            logger.error(f"Processing failed for {md_file.name}: {e}", exc_info=True)
            results["errors"].append(f"Processing failed for {md_file.name}: {e}")

    total_outputs = sum(results["summary"].values())
    logger.info(f"Processed module {module_dir.name}: {len(files_to_process)} files, {total_outputs} outputs generated")
    if results["errors"]:
        logger.warning(f"Module processing completed with {len(results['errors'])} errors")

    return results


def process_syllabus(syllabus_path: str, output_dir: str) -> Dict[str, Any]:
    """Process syllabus files and generate all format renderings.

    Organizes outputs flat in the output directory (same structure as module assignments),
    with all formats (PDF, MP3, DOCX, HTML, TXT) in the same directory.

    Args:
        syllabus_path: Path to syllabus directory
        output_dir: Base output directory for all renderings

    Returns:
        Dictionary with results:
        - by_format: Dict mapping format type to list of generated files
        - summary: Dict with counts of generated files by format
        - errors: List of errors encountered

    Raises:
        ValueError: If syllabus path doesn't exist
    """
    syllabus_dir = Path(syllabus_path)
    if not syllabus_dir.exists():
        raise ValueError(f"Syllabus path does not exist: {syllabus_path}")

    logger.info(f"Processing syllabus: {syllabus_dir.name}")
    base_output = Path(output_dir)
    ensure_output_directory(base_output)

    # Find all markdown files in syllabus directory (excluding README and AGENTS)
    markdown_files = find_markdown_files(syllabus_dir)
    syllabus_files = [
        f for f in markdown_files
        if not f.name.startswith("README") and not f.name.startswith("AGENTS")
    ]

    results = {
        "by_format": {"pdf": [], "mp3": [], "docx": [], "html": [], "txt": []},
        "summary": {"pdf": 0, "mp3": 0, "docx": 0, "html": 0, "txt": 0},
        "errors": [],
    }

    for md_file in syllabus_files:
        try:
            # Base filename without extension
            base_name = md_file.stem

            # Generate PDF
            try:
                pdf_file = base_output / f"{base_name}.pdf"
                from ..markdown_to_pdf.main import render_markdown_to_pdf

                logger.debug(f"Generating PDF: {pdf_file.name}")
                render_markdown_to_pdf(str(md_file), str(pdf_file))
                results["by_format"]["pdf"].append(str(pdf_file))
                results["summary"]["pdf"] += 1
            except Exception as e:
                error_msg = f"PDF generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate Audio (MP3)
            try:
                audio_file = base_output / f"{base_name}.mp3"
                from ..text_to_speech.utils import (
                    extract_text_from_markdown,
                    read_text_file,
                )
                from ..text_to_speech.main import generate_speech
            
                logger.debug(f"Generating MP3: {audio_file.name}")
                content = read_text_file(md_file)
                text_content = extract_text_from_markdown(content)
                generate_speech(text_content, str(audio_file))
                time.sleep(2)  # Add delay to avoid 429 errors
                results["by_format"]["mp3"].append(str(audio_file))
                results["summary"]["mp3"] += 1
            except Exception as e:
                error_msg = f"Audio generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate DOCX
            try:
                docx_file = base_output / f"{base_name}.docx"
                from ..format_conversion.main import convert_file

                logger.debug(f"Generating DOCX: {docx_file.name}")
                convert_file(str(md_file), "docx", str(docx_file))
                results["by_format"]["docx"].append(str(docx_file))
                results["summary"]["docx"] += 1
            except Exception as e:
                error_msg = f"DOCX generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate HTML
            try:
                html_file = base_output / f"{base_name}.html"
                from ..format_conversion.main import convert_file as convert_file_func
                logger.debug(f"Generating HTML: {html_file.name}")
                convert_file_func(str(md_file), "html", str(html_file))
                results["by_format"]["html"].append(str(html_file))
                results["summary"]["html"] += 1
            except Exception as e:
                error_msg = f"HTML generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

            # Generate TXT (extracted text)
            try:
                txt_file = base_output / f"{base_name}.txt"
                from ..text_to_speech.utils import (
                    extract_text_from_markdown,
                    read_text_file,
                )

                logger.debug(f"Generating TXT: {txt_file.name}")
                content = read_text_file(md_file)
                text_content = extract_text_from_markdown(content)
                txt_file.write_text(text_content, encoding="utf-8")
                results["by_format"]["txt"].append(str(txt_file))
                results["summary"]["txt"] += 1
            except Exception as e:
                error_msg = f"TXT generation failed for {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

        except Exception as e:
            logger.error(f"Processing failed for {md_file.name}: {e}", exc_info=True)
            results["errors"].append(f"Processing failed for {md_file.name}: {e}")

    logger.info(f"Processed syllabus: {len(syllabus_files)} files, {sum(results['summary'].values())} outputs generated")
    if results["errors"]:
        logger.warning(f"Syllabus processing completed with {len(results['errors'])} errors")

    return results


def clear_all_outputs(repo_root: Path) -> Dict[str, Any]:
    """Clear all output directories before regeneration.

    Removes all files and subdirectories within output directories while
    preserving the output directory structure itself.

    Args:
        repo_root: Root path of the repository

    Returns:
        Dictionary with summary:
        - cleared_directories: List of cleared directory paths
        - total_files_removed: Total count of files removed
        - errors: List of errors encountered
    """
    logger.info("Starting output clearing process")
    results = {
        "cleared_directories": [],
        "total_files_removed": 0,
        "errors": [],
    }

    # Find all output directories
    output_dirs = []
    for course_dir in ["biol-1", "biol-8"]:
        course_path = repo_root / course_dir
        if not course_path.exists():
            logger.debug(f"Course directory not found: {course_path}")
            continue

        # Module output directories
        course_modules = course_path / "course"
        if course_modules.exists():
            for module_dir in course_modules.iterdir():
                if module_dir.is_dir() and module_dir.name.startswith("module-"):
                    output_dir = module_dir / "output"
                    if output_dir.exists():
                        output_dirs.append(output_dir)

        # Syllabus output directory
        syllabus_path = course_path / "syllabus" / "output"
        if syllabus_path.exists():
            output_dirs.append(syllabus_path)

    logger.info(f"Found {len(output_dirs)} output directories to clear")

    for output_dir in output_dirs:
        try:
            # Count files before clearing
            file_count = sum(1 for _ in output_dir.rglob("*") if _.is_file())
            dir_count = sum(1 for _ in output_dir.rglob("*") if _.is_dir())

            if file_count == 0 and dir_count == 0:
                logger.debug(f"Output directory already empty: {output_dir}")
                continue

            # Remove all contents but keep the directory
            for item in output_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)

            results["cleared_directories"].append(str(output_dir))
            results["total_files_removed"] += file_count

            logger.info(f"Cleared {file_count} files and {dir_count} directories from {output_dir.relative_to(repo_root)}")

        except Exception as e:
            error_msg = f"Failed to clear {output_dir}: {e}"
            logger.error(error_msg, exc_info=True)
            results["errors"].append(error_msg)

    logger.info(f"Output clearing completed: {len(results['cleared_directories'])} directories, {results['total_files_removed']} files removed")
    if results["errors"]:
        logger.warning(f"Output clearing completed with {len(results['errors'])} errors")

    return results


def process_module_website(module_path: str, output_dir: Optional[str] = None) -> str:
    """Generate HTML website for a module.

    Args:
        module_path: Path to module directory
        output_dir: Optional output directory (defaults to module_path/output/website)

    Returns:
        Path to generated HTML file

    Raises:
        ValueError: If module path doesn't exist
        OSError: If website generation fails
    """
    from ..html_website.main import generate_module_website

    logger.info(f"Generating website for module: {Path(module_path).name}")
    website_file = generate_module_website(module_path, output_dir)
    logger.info(f"Website generated: {website_file}")
    return website_file
