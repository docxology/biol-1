#!/usr/bin/env python3
"""Import legacy materials from bio_1_2025 to biol-1 structure.

Usage:
    uv run python scripts/import_legacy_materials.py [OPTIONS]

Options:
    --course COURSE    Course: biol-1 or biol-8 (default: biol-1)
    --dry-run          Show what would be imported without importing
    --skip-questions   Skip importing chapter questions
    --skip-slides      Skip importing slides
    --help             Show this help message

Examples:
    # Import all materials for biol-1 (default)
    uv run python scripts/import_legacy_materials.py

    # Dry run to preview what would be imported
    uv run python scripts/import_legacy_materials.py --dry-run

    # Import only slides, skip questions
    uv run python scripts/import_legacy_materials.py --skip-questions
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.logging_config import setup_logging
from src.format_conversion.utils import convert_docx_to_markdown
from src.module_organization.main import create_module_structure, initialize_module_files

# Setup logging
logger = setup_logging()


def get_chapter_to_module_mapping() -> Dict[int, int]:
    """Return mapping of chapter numbers to module numbers.

    Mapping: 17 chapters map to 17 modules (1:1 mapping)

    Returns:
        Dictionary mapping chapter numbers to module numbers
    """
    # Simple 1:1 mapping - each chapter gets its own module
    return {i: i for i in range(1, 18)}


def extract_chapter_number(filename: str) -> int:
    """Extract chapter number from filename.

    Args:
        filename: Filename like "Chapter 01 Keys to Success.docx" or
                 "General Biology Chapter 01 Slides.pdf"

    Returns:
        Chapter number as integer

    Raises:
        ValueError: If chapter number cannot be extracted
    """
    # Pattern for "Chapter NN" or "Chapter 0N"
    match = re.search(r"Chapter\s+0?(\d+)", filename, re.IGNORECASE)
    if match:
        return int(match.group(1))

    raise ValueError(f"Could not extract chapter number from filename: {filename}")


def ensure_module_exists(course_root: Path, module_num: int, dry_run: bool) -> Path:
    """Ensure module exists, creating it if necessary.

    Args:
        course_root: Course root directory (e.g., biol-1)
        module_num: Module number
        dry_run: If True, only check existence without creating

    Returns:
        Path to module directory
    """
    # get_module_path adds /course/ to the path, so we pass course_root
    from src.module_organization.utils import get_module_path
    module_path = get_module_path(course_root, module_num)

    if not module_path.exists():
        if dry_run:
            logger.info(f"[DRY RUN] Would create module-{module_num}")
        else:
            logger.info(f"Creating module-{module_num}")
            try:
                created_path = create_module_structure(str(course_root), module_num)
                logger.debug(f"Successfully created module {module_num} at {created_path}")
            except ValueError as e:
                # Module might already exist from concurrent creation
                if "already exists" in str(e):
                    logger.debug(f"Module {module_num} already exists (concurrent creation)")
                else:
                    logger.error(f"Could not create module {module_num}: {e}")
                    raise  # Re-raise to handle in caller
            except Exception as e:
                logger.error(f"Unexpected error creating module {module_num}: {e}", exc_info=True)
                raise  # Re-raise to handle in caller

    return module_path


def create_comprehension_questions(module_path: Path, module_num: int, dry_run: bool) -> None:
    """Create comprehension-questions.md file in resources directory.

    Args:
        module_path: Path to module directory
        module_num: Module number
        dry_run: If True, only show what would be created
    """
    resources_dir = module_path / "resources"
    if not dry_run:
        resources_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = resources_dir / "comprehension-questions.md"
    if not file_path.exists():
        if dry_run:
            logger.info(f"[DRY RUN] Would create resources/comprehension-questions.md")
        else:
            content = f"# Comprehension Questions - Module {module_num}\n\nComprehension questions for Module {module_num}.\n"
            file_path.write_text(content, encoding="utf-8")
            logger.debug(f"Created: {file_path}")


def create_questions_directory(module_path: Path, module_num: int, dry_run: bool) -> None:
    """Create questions directory with questions.json.

    Args:
        module_path: Path to module directory
        module_num: Module number
        dry_run: If True, only show what would be created
    """
    questions_dir = module_path / "questions"
    
    if dry_run:
        logger.info(f"[DRY RUN] Would create questions/ directory")
        return
    
    questions_dir.mkdir(parents=True, exist_ok=True)
    
    # Create questions.json if it doesn't exist
    questions_json = questions_dir / "questions.json"
    if not questions_json.exists():
        questions_json.write_text('{\n  "questions": []\n}\n', encoding="utf-8")
        logger.debug(f"Created: {questions_json}")
    
    # Create README.md if it doesn't exist
    readme = questions_dir / "README.md"
    if not readme.exists():
        readme_content = f"""# Module {module_num} Questions

## Overview

This directory contains interactive questions for Module {module_num}. Questions are stored in JSON format and are displayed interactively on the module website.

## Question Files

- **`questions.json`**: Main question file containing all interactive questions for this module

## Question Types

The questions support multiple interactive formats:

- **Multiple Choice**: Select one correct answer from multiple options
- **Free Response**: Text input for open-ended answers
- **True/False**: Binary choice questions
- **Matching**: Match terms with their definitions or related concepts

## Usage

Questions are automatically processed and displayed on the module website at `output/website/index.html`. Students can interact with questions directly in the browser.

## Documentation

- **[AGENTS.md](AGENTS.md)**: Technical documentation for question format and processing
"""
        readme.write_text(readme_content, encoding="utf-8")
        logger.debug(f"Created: {readme}")
    
    # Create AGENTS.md if it doesn't exist
    agents = questions_dir / "AGENTS.md"
    if not agents.exists():
        agents_content = f"""# Module {module_num} Questions Technical Documentation

## Overview

Technical documentation for question format, structure, and processing for Module {module_num}.

## Question Format

Questions are stored in JSON format with the following structure:

```json
{{
  "questions": [
    {{
      "id": "unique-question-id",
      "type": "multiple_choice|free_response|true_false|matching",
      "question": "Question text",
      ...
    }}
  ]
}}
```

## Question Types

### Multiple Choice

```json
{{
  "id": "q1",
  "type": "multiple_choice",
  "question": "Question text",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct": 0,
  "explanation": "Explanation of correct answer"
}}
```

- `options`: Array of answer choices
- `correct`: Index (0-based) of correct answer
- `explanation`: Optional explanation shown after answer

### Free Response

```json
{{
  "id": "q2",
  "type": "free_response",
  "question": "Question text",
  "placeholder": "Optional placeholder text",
  "max_length": 500
}}
```

- `placeholder`: Optional placeholder text for textarea
- `max_length`: Optional maximum character count

### True/False

```json
{{
  "id": "q3",
  "type": "true_false",
  "question": "Question text",
  "correct": true,
  "explanation": "Explanation of answer"
}}
```

- `correct`: Boolean value (true or false)
- `explanation`: Optional explanation

### Matching

```json
{{
  "id": "q4",
  "type": "matching",
  "question": "Match the terms with definitions",
  "items": [
    {{"term": "Term 1", "definition": "Definition 1"}},
    {{"term": "Term 2", "definition": "Definition 2"}}
  ]
}}
```

- `items`: Array of term-definition pairs to match

## Processing

Questions are processed by the HTML website generation module:

- **Module**: `software/src/html_website/main.py`
- **Function**: `generate_module_website()`
- **Utility**: `parse_questions_json()` from `html_website/utils.py`

## Output

Questions are rendered as interactive HTML elements on the module website with:
- Answer validation
- Feedback and explanations
- Progress tracking
- State persistence
"""
        agents.write_text(agents_content, encoding="utf-8")
        logger.debug(f"Created: {agents}")


def process_chapter_questions(
    source_dir: Path, course_root: Path, course_dir: Path, dry_run: bool
) -> Dict[str, Any]:
    """Process all Chapter Questions DOCX files.

    Args:
        source_dir: Directory containing Chapter Questions DOCX files
        course_dir: Course directory (e.g., biol-1/course)
        dry_run: If True, only show what would be done without doing it

    Returns:
        Dictionary with processing results
    """
    results = {
        "processed": [],
        "skipped": [],
        "errors": [],
        "summary": {"converted": 0, "skipped": 0, "errors": 0, "modules_created": 0},
    }

    chapter_mapping = get_chapter_to_module_mapping()

    # Find all DOCX files in source directory
    docx_files = list(source_dir.glob("*.docx"))
    if not docx_files:
        logger.warning(f"No DOCX files found in {source_dir}")
        return results

    logger.info(f"Found {len(docx_files)} DOCX files to process")

    for docx_file in sorted(docx_files):
        try:
            # Extract chapter number from filename
            chapter_num = extract_chapter_number(docx_file.name)

            # Get module number from mapping (1:1 mapping)
            if chapter_num not in chapter_mapping:
                logger.warning(
                    f"Skipping {docx_file.name}: Chapter {chapter_num} not in mapping"
                )
                results["skipped"].append(
                    {
                        "file": docx_file.name,
                        "reason": f"Chapter {chapter_num} not in mapping",
                    }
                )
                results["summary"]["skipped"] += 1
                continue

            module_num = chapter_mapping[chapter_num]

            # Ensure module exists
            module_path = ensure_module_exists(course_root, module_num, dry_run)
            if not dry_run and not module_path.exists():
                # Module creation failed
                results["skipped"].append(
                    {
                        "file": docx_file.name,
                        "reason": f"Could not create module {module_num}",
                    }
                )
                results["summary"]["skipped"] += 1
                continue

            if not module_path.exists() and not dry_run:
                results["summary"]["modules_created"] += 1

            # Create comprehension questions file in resources directory
            create_comprehension_questions(module_path, module_num, dry_run)

            # Determine output path
            resources_dir = module_path / "resources"

            if not dry_run:
                resources_dir.mkdir(parents=True, exist_ok=True)

            # Output filename
            output_filename = f"module-{module_num}-keys-to-success.md"
            output_path = resources_dir / output_filename

            if dry_run:
                logger.info(
                    f"[DRY RUN] Would convert: {docx_file.name} -> {output_path}"
                )
                results["processed"].append(
                    {
                        "source": docx_file.name,
                        "destination": str(output_path),
                        "module": module_num,
                        "chapter": chapter_num,
                    }
                )
            else:
                # Convert DOCX to Markdown
                logger.info(f"Converting: {docx_file.name} -> {output_path.name}")
                markdown_content = convert_docx_to_markdown(docx_file)
                output_path.write_text(markdown_content, encoding="utf-8")
                logger.debug(f"Created: {output_path}")

                results["processed"].append(
                    {
                        "source": docx_file.name,
                        "destination": str(output_path),
                        "module": module_num,
                        "chapter": chapter_num,
                    }
                )
                results["summary"]["converted"] += 1

        except ValueError as e:
            error_msg = f"Error processing {docx_file.name}: {e}"
            logger.error(error_msg)
            results["errors"].append({"file": docx_file.name, "error": str(e)})
            results["summary"]["errors"] += 1
        except Exception as e:
            error_msg = f"Unexpected error processing {docx_file.name}: {e}"
            logger.error(error_msg, exc_info=True)
            results["errors"].append({"file": docx_file.name, "error": str(e)})
            results["summary"]["errors"] += 1

    return results


def process_slides(
    slides_full_dir: Path,
    slides_notes_dir: Path,
    course_root: Path,
    dry_run: bool,
) -> Dict[str, Any]:
    """Copy and organize PDF slides to module directories.

    Args:
        slides_full_dir: Directory containing full slides PDFs
        slides_notes_dir: Directory containing notes slides PDFs
        course_dir: Course directory (e.g., biol-1/course)
        dry_run: If True, only show what would be done without doing it

    Returns:
        Dictionary with processing results
    """
    results = {
        "processed": [],
        "skipped": [],
        "errors": [],
        "summary": {"copied": 0, "skipped": 0, "errors": 0},
    }

    chapter_mapping = get_chapter_to_module_mapping()

    # Process full slides
    if slides_full_dir.exists():
        full_slides = list(slides_full_dir.glob("*.pdf"))
        logger.info(f"Found {len(full_slides)} full slide PDFs to process")

        for pdf_file in sorted(full_slides):
            try:
                chapter_num = extract_chapter_number(pdf_file.name)

                if chapter_num not in chapter_mapping:
                    logger.warning(
                        f"Skipping {pdf_file.name}: Chapter {chapter_num} not in mapping"
                    )
                    results["skipped"].append(
                        {
                            "file": pdf_file.name,
                            "reason": f"Chapter {chapter_num} not in mapping",
                        }
                    )
                    results["summary"]["skipped"] += 1
                    continue

                module_num = chapter_mapping[chapter_num]

                # Ensure module exists
                module_path = ensure_module_exists(course_root, module_num, dry_run)
                if not module_path.exists() and not dry_run:
                    continue

                # Create slides directory in module
                slides_dir = module_path / "slides"
                if not dry_run:
                    slides_dir.mkdir(parents=True, exist_ok=True)

                output_filename = f"module-{module_num}-slides-full.pdf"
                output_path = slides_dir / output_filename

                if dry_run:
                    logger.info(
                        f"[DRY RUN] Would copy: {pdf_file.name} -> {output_path}"
                    )
                    results["processed"].append(
                        {
                            "source": pdf_file.name,
                            "destination": str(output_path),
                            "module": module_num,
                            "chapter": chapter_num,
                            "type": "full",
                        }
                    )
                else:
                    logger.info(f"Copying: {pdf_file.name} -> {output_path.name}")
                    shutil.copy2(pdf_file, output_path)
                    logger.debug(f"Copied: {output_path}")

                    results["processed"].append(
                        {
                            "source": pdf_file.name,
                            "destination": str(output_path),
                            "module": module_num,
                            "chapter": chapter_num,
                            "type": "full",
                        }
                    )
                    results["summary"]["copied"] += 1

            except ValueError as e:
                error_msg = f"Error processing {pdf_file.name}: {e}"
                logger.error(error_msg)
                results["errors"].append({"file": pdf_file.name, "error": str(e)})
                results["summary"]["errors"] += 1
            except Exception as e:
                error_msg = f"Unexpected error processing {pdf_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append({"file": pdf_file.name, "error": str(e)})
                results["summary"]["errors"] += 1
    else:
        logger.warning(f"Full slides directory does not exist: {slides_full_dir}")

    # Process notes slides
    if slides_notes_dir.exists():
        notes_slides = list(slides_notes_dir.glob("*.pdf"))
        logger.info(f"Found {len(notes_slides)} notes slide PDFs to process")

        for pdf_file in sorted(notes_slides):
            try:
                chapter_num = extract_chapter_number(pdf_file.name)

                if chapter_num not in chapter_mapping:
                    logger.warning(
                        f"Skipping {pdf_file.name}: Chapter {chapter_num} not in mapping"
                    )
                    results["skipped"].append(
                        {
                            "file": pdf_file.name,
                            "reason": f"Chapter {chapter_num} not in mapping",
                        }
                    )
                    results["summary"]["skipped"] += 1
                    continue

                module_num = chapter_mapping[chapter_num]

                # Ensure module exists
                module_path = ensure_module_exists(course_root, module_num, dry_run)
                if not module_path.exists() and not dry_run:
                    continue

                # Create slides directory in module
                slides_dir = module_path / "slides"
                if not dry_run:
                    slides_dir.mkdir(parents=True, exist_ok=True)

                output_filename = f"module-{module_num}-slides-notes.pdf"
                output_path = slides_dir / output_filename

                if dry_run:
                    logger.info(
                        f"[DRY RUN] Would copy: {pdf_file.name} -> {output_path}"
                    )
                    results["processed"].append(
                        {
                            "source": pdf_file.name,
                            "destination": str(output_path),
                            "module": module_num,
                            "chapter": chapter_num,
                            "type": "notes",
                        }
                    )
                else:
                    logger.info(f"Copying: {pdf_file.name} -> {output_path.name}")
                    shutil.copy2(pdf_file, output_path)
                    logger.debug(f"Copied: {output_path}")

                    results["processed"].append(
                        {
                            "source": pdf_file.name,
                            "destination": str(output_path),
                            "module": module_num,
                            "chapter": chapter_num,
                            "type": "notes",
                        }
                    )
                    results["summary"]["copied"] += 1

            except ValueError as e:
                error_msg = f"Error processing {pdf_file.name}: {e}"
                logger.error(error_msg)
                results["errors"].append({"file": pdf_file.name, "error": str(e)})
                results["summary"]["errors"] += 1
            except Exception as e:
                error_msg = f"Unexpected error processing {pdf_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append({"file": pdf_file.name, "error": str(e)})
                results["summary"]["errors"] += 1
    else:
        logger.warning(f"Notes slides directory does not exist: {slides_notes_dir}")

    return results


def create_for_upload_files(module_path: Path, module_num: int, dry_run: bool) -> Dict[str, Any]:
    """Create for_upload folder with DOCX and PDF of all markdown files plus slide PDFs.

    Args:
        module_path: Path to module directory
        module_num: Module number
        dry_run: If True, only show what would be created

    Returns:
        Dictionary with processing results
    """
    results = {
        "processed": [],
        "errors": [],
        "summary": {"pdf": 0, "docx": 0, "slides_copied": 0, "errors": 0},
    }

    for_upload_dir = module_path / "for_upload"
    
    if dry_run:
        logger.info(f"[DRY RUN] Would create for_upload/ directory for module-{module_num}")
    else:
        for_upload_dir.mkdir(parents=True, exist_ok=True)

    # Find all markdown files in resources directory
    resources_dir = module_path / "resources"
    markdown_files = []
    if resources_dir.exists():
        markdown_files = [
            f for f in resources_dir.glob("*.md")
            if f.name not in ["README.md", "AGENTS.md"]
        ]

    # Process each markdown file
    for md_file in markdown_files:
        base_name = md_file.stem
        
        if dry_run:
            logger.info(f"[DRY RUN] Would process {md_file.name} -> for_upload/")
            results["processed"].append({"file": md_file.name, "type": "markdown"})
        else:
            try:
                # Generate PDF
                pdf_file = for_upload_dir / f"{base_name}.pdf"
                from src.markdown_to_pdf.main import render_markdown_to_pdf
                logger.debug(f"Generating PDF: {pdf_file.name}")
                render_markdown_to_pdf(str(md_file), str(pdf_file))
                results["summary"]["pdf"] += 1
                results["processed"].append({"file": pdf_file.name, "type": "pdf"})

                # Generate DOCX
                docx_file = for_upload_dir / f"{base_name}.docx"
                from src.format_conversion.main import convert_file
                logger.debug(f"Generating DOCX: {docx_file.name}")
                convert_file(str(md_file), "docx", str(docx_file))
                results["summary"]["docx"] += 1
                results["processed"].append({"file": docx_file.name, "type": "docx"})

            except Exception as e:
                error_msg = f"Error processing {md_file.name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append({"file": md_file.name, "error": str(e)})
                results["summary"]["errors"] += 1

    # Copy slide PDFs to for_upload
    slides_dir = module_path / "slides"
    if slides_dir.exists():
        slide_pdfs = list(slides_dir.glob("*.pdf"))
        for slide_pdf in slide_pdfs:
            if dry_run:
                logger.info(f"[DRY RUN] Would copy {slide_pdf.name} -> for_upload/")
                results["processed"].append({"file": slide_pdf.name, "type": "slide"})
            else:
                try:
                    dest_file = for_upload_dir / slide_pdf.name
                    shutil.copy2(slide_pdf, dest_file)
                    logger.debug(f"Copied slide: {dest_file.name}")
                    results["summary"]["slides_copied"] += 1
                    results["processed"].append({"file": dest_file.name, "type": "slide"})
                except Exception as e:
                    error_msg = f"Error copying {slide_pdf.name}: {e}"
                    logger.error(error_msg, exc_info=True)
                    results["errors"].append({"file": slide_pdf.name, "error": str(e)})
                    results["summary"]["errors"] += 1

    return results


def process_for_upload_all_modules(course_dir: Path, dry_run: bool) -> Dict[str, Any]:
    """Process for_upload folders for all modules.

    Args:
        course_dir: Course directory (e.g., biol-1/course)
        dry_run: If True, only show what would be created

    Returns:
        Dictionary with processing results
    """
    results = {
        "modules_processed": 0,
        "modules_errors": 0,
        "total_pdf": 0,
        "total_docx": 0,
        "total_slides": 0,
        "errors": [],
    }

    # Find all modules
    modules = sorted([d for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("module-")])
    
    logger.info(f"Processing for_upload folders for {len(modules)} modules")

    for module_path in modules:
        # Extract module number
        match = re.search(r"module-(\d+)", module_path.name)
        if not match:
            continue
        
        module_num = int(match.group(1))
        
        try:
            module_results = create_for_upload_files(module_path, module_num, dry_run)
            results["modules_processed"] += 1
            results["total_pdf"] += module_results["summary"]["pdf"]
            results["total_docx"] += module_results["summary"]["docx"]
            results["total_slides"] += module_results["summary"]["slides_copied"]
            
            if module_results["errors"]:
                results["modules_errors"] += 1
                results["errors"].extend(module_results["errors"])
        except Exception as e:
            error_msg = f"Error processing for_upload for {module_path.name}: {e}"
            logger.error(error_msg, exc_info=True)
            results["modules_errors"] += 1
            results["errors"].append({"module": module_path.name, "error": str(e)})

    return results


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Import legacy materials from bio_1_2025 to biol-1 structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Import all materials for biol-1
  %(prog)s --dry-run                Preview what would be imported
  %(prog)s --skip-questions         Import only slides
  %(prog)s --skip-slides            Import only chapter questions
  %(prog)s --course biol-8          Import for biol-8
        """,
    )

    parser.add_argument(
        "--course",
        choices=["biol-1", "biol-8"],
        default="biol-1",
        help="Course to process (default: biol-1)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without importing",
    )

    parser.add_argument(
        "--skip-questions",
        action="store_true",
        help="Skip importing chapter questions",
    )

    parser.add_argument(
        "--skip-slides",
        action="store_true",
        help="Skip importing slides",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    source_questions_dir = repo_root / "bio_1_2025" / "files" / "Chapter Questions"
    source_slides_full_dir = repo_root / "bio_1_2025" / "files" / "Slides" / "Slides_Full"
    source_slides_notes_dir = (
        repo_root / "bio_1_2025" / "files" / "Slides" / "Slides_Notes"
    )
    course_root = repo_root / args.course  # Course root (e.g., biol-1)
    course_dir = course_root / "course"  # Course directory (e.g., biol-1/course)

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 60)

    # Process chapter questions
    questions_results = None
    if not args.skip_questions:
        if not source_questions_dir.exists():
            logger.error(f"Chapter Questions directory does not exist: {source_questions_dir}")
            return 1

        print("\n" + "=" * 60)
        print("Processing Chapter Questions")
        print("=" * 60)
        questions_results = process_chapter_questions(
            source_questions_dir, course_root, course_dir, args.dry_run
        )

        print(f"\nChapter Questions Summary:")
        print(f"  Converted: {questions_results['summary']['converted']}")
        print(f"  Modules Created: {questions_results['summary']['modules_created']}")
        print(f"  Skipped: {questions_results['summary']['skipped']}")
        print(f"  Errors: {questions_results['summary']['errors']}")

        if questions_results["processed"]:
            print(f"\nProcessed files ({len(questions_results['processed'])}):")
            for item in questions_results["processed"]:
                print(f"  - {item['source']} -> module-{item['module']}")

        if questions_results["errors"]:
            print(f"\nErrors ({len(questions_results['errors'])}):")
            for error in questions_results["errors"]:
                print(f"  - {error['file']}: {error['error']}")

    # Process slides
    slides_results = None
    if not args.skip_slides:
        print("\n" + "=" * 60)
        print("Processing Slides")
        print("=" * 60)
        slides_results = process_slides(
            source_slides_full_dir,
            source_slides_notes_dir,
            course_root,
            args.dry_run,
        )

        print(f"\nSlides Summary:")
        print(f"  Copied: {slides_results['summary']['copied']}")
        print(f"  Skipped: {slides_results['summary']['skipped']}")
        print(f"  Errors: {slides_results['summary']['errors']}")

        if slides_results["processed"]:
            print(f"\nProcessed files ({len(slides_results['processed'])}):")
            for item in slides_results["processed"]:
                print(f"  - {item['source']} -> module-{item['module']} ({item['type']})")

        if slides_results["errors"]:
            print(f"\nErrors ({len(slides_results['errors'])}):")
            for error in slides_results["errors"]:
                print(f"  - {error['file']}: {error['error']}")

    # Overall summary
    print("\n" + "=" * 60)
    print("Import Summary")
    print("=" * 60)

    total_processed = 0
    total_errors = 0
    total_modules_created = 0

    if questions_results:
        total_processed += questions_results["summary"]["converted"]
        total_errors += questions_results["summary"]["errors"]
        total_modules_created += questions_results["summary"]["modules_created"]

    if slides_results:
        total_processed += slides_results["summary"]["copied"]
        total_errors += slides_results["summary"]["errors"]

    # Process for_upload folders
    print("\n" + "=" * 60)
    print("Processing For Upload Folders")
    print("=" * 60)
    for_upload_results = process_for_upload_all_modules(course_dir, args.dry_run)

    print(f"\nFor Upload Summary:")
    print(f"  Modules Processed: {for_upload_results['modules_processed']}")
    print(f"  PDF files created: {for_upload_results['total_pdf']}")
    print(f"  DOCX files created: {for_upload_results['total_docx']}")
    print(f"  Slides copied: {for_upload_results['total_slides']}")
    print(f"  Errors: {len(for_upload_results['errors'])}")

    if for_upload_results["errors"]:
        print(f"\nFor Upload Errors ({len(for_upload_results['errors'])}):")
        for error in for_upload_results["errors"][:10]:  # Show first 10
            print(f"  - {error}")

    total_errors += len(for_upload_results["errors"])

    print(f"\nTotal files processed: {total_processed}")
    print(f"Total modules created: {total_modules_created}")
    print(f"Total errors: {total_errors}")

    if args.dry_run:
        print("\n[DRY RUN] No files were actually modified.")
        print("Run without --dry-run to perform the import.")
    elif total_errors == 0:
        print("\n✓ Import completed successfully!")
    else:
        print(f"\n⚠ Import completed with {total_errors} error(s).")

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
