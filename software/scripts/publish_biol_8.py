#!/usr/bin/env python3
"""
Publish BIOL-8 Course Materials

Exports the fully published BIOL-8 course to the PUBLISHED/biol-8 subfolder.
Outputs include:
- Syllabus and Schedule (PDF, MD, DOCX, MP3)
- Each module's Keys-to-Success and Questions (PDF, MD, DOCX, MP3)
- Slide PDFs from module resources folders
- Exams and Quizzes (PDF, MD, DOCX)

Usage:
    python publish_biol_8.py
    python publish_biol_8.py --dry-run
    python publish_biol_8.py --modules 01 02 03
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(software_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Define repository structure
REPO_ROOT = software_dir.parent
BIOL8_COURSE = REPO_ROOT / "course_development" / "biol-8"
BIOL8_COURSE_DIR = BIOL8_COURSE / "course"
BIOL8_SYLLABUS_DIR = BIOL8_COURSE / "syllabus"
PUBLISHED_DIR = REPO_ROOT / "PUBLISHED" / "biol-8"

# Module list
MODULES = [
    ("01", "exploring-life-science"),
    ("02", "chemistry-of-life"),
    ("03", "biomolecules"),
    ("04", "cellular-function"),
    ("05", "membranes"),
    ("06", "metabolism"),
    ("07", "mitosis"),
    ("08", "meiosis"),
    ("09", "inheritance"),
    ("10", "tissues"),
    ("11", "skeletal-system"),
    ("12", "muscular-system"),
    ("13", "pathogens"),
    ("14", "cardiovascular-system"),
    ("15", "respiratory-system"),
]


def ensure_directory(path: Path) -> None:
    """Ensure a directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> bool:
    """Copy a file if source exists."""
    if src.exists():
        ensure_directory(dst.parent)
        shutil.copy2(src, dst)
        logger.debug(f"Copied: {src.name} -> {dst}")
        return True
    else:
        logger.warning(f"Source not found: {src}")
        return False


def convert_markdown_to_pdf(input_path: Path, output_path: Path) -> bool:
    """Convert markdown to PDF using the markdown_to_pdf module."""
    try:
        from src.markdown_to_pdf.main import render_markdown_to_pdf
        render_markdown_to_pdf(str(input_path), str(output_path))
        logger.debug(f"PDF: {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"PDF conversion failed for {input_path.name}: {e}")
        return False


def convert_markdown_to_docx(input_path: Path, output_path: Path) -> bool:
    """Convert markdown to DOCX using the format_conversion module."""
    try:
        from src.format_conversion.main import convert_file
        convert_file(str(input_path), "docx", str(output_path))
        logger.debug(f"DOCX: {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"DOCX conversion failed for {input_path.name}: {e}")
        return False


def convert_markdown_to_mp3(input_path: Path, output_path: Path) -> bool:
    """Convert markdown to MP3 using the text_to_speech module."""
    try:
        from src.text_to_speech.main import generate_speech
        from src.text_to_speech.utils import extract_text_from_markdown, read_text_file
        
        content = read_text_file(input_path)
        text = extract_text_from_markdown(content)
        
        # Only generate if there's substantial text
        if len(text.strip()) < 50:
            logger.warning(f"Skipping MP3 (too short): {input_path.name}")
            return False
            
        generate_speech(text, str(output_path))
        logger.debug(f"MP3: {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"MP3 conversion failed for {input_path.name}: {e}")
        return False


def process_markdown_file(
    input_path: Path, 
    output_dir: Path, 
    basename: str,
    formats: List[str] = ["pdf", "md", "docx", "mp3"]
) -> Dict[str, bool]:
    """Process a markdown file to multiple output formats."""
    results = {}
    
    ensure_directory(output_dir)
    
    # Copy original markdown
    if "md" in formats:
        md_out = output_dir / f"{basename}.md"
        results["md"] = copy_file(input_path, md_out)
    
    # Convert to PDF
    if "pdf" in formats:
        pdf_out = output_dir / f"{basename}.pdf"
        results["pdf"] = convert_markdown_to_pdf(input_path, pdf_out)
    
    # Convert to DOCX
    if "docx" in formats:
        docx_out = output_dir / f"{basename}.docx"
        results["docx"] = convert_markdown_to_docx(input_path, docx_out)
    
    # Convert to MP3
    if "mp3" in formats:
        mp3_out = output_dir / f"{basename}.mp3"
        results["mp3"] = convert_markdown_to_mp3(input_path, mp3_out)
    
    return results


def publish_syllabus(output_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Publish syllabus and schedule documents."""
    logger.info("📄 Publishing Syllabus and Schedule...")
    
    syllabus_output = output_dir / "syllabus"
    results = {"files": 0, "errors": []}
    
    if dry_run:
        logger.info("  [DRY RUN] Would publish syllabus files")
        return results
    
    files_to_process = [
        (BIOL8_SYLLABUS_DIR / "BIOL-8_Spring-2026_Syllabus.md", "BIOL-8_Syllabus"),
        (BIOL8_SYLLABUS_DIR / "Schedule.md", "BIOL-8_Schedule"),
    ]
    
    for src_path, basename in files_to_process:
        if src_path.exists():
            result = process_markdown_file(src_path, syllabus_output, basename)
            results["files"] += sum(1 for v in result.values() if v)
        else:
            results["errors"].append(f"Not found: {src_path}")
    
    logger.info(f"  ✓ Syllabus: {results['files']} files")
    return results


def publish_module(
    module_num: str, 
    module_topic: str, 
    output_dir: Path, 
    dry_run: bool = False
) -> Dict[str, Any]:
    """Publish a single module's materials."""
    module_dir_name = f"module-{module_num}-{module_topic}"
    module_src = BIOL8_COURSE_DIR / module_dir_name
    module_output = output_dir / "modules" / module_dir_name
    
    results = {"files": 0, "errors": [], "slides": 0}
    
    if not module_src.exists():
        results["errors"].append(f"Module not found: {module_dir_name}")
        return results
    
    if dry_run:
        logger.info(f"  [DRY RUN] Would publish module {module_num}")
        return results
    
    # Process keys-to-success.md
    keys_src = module_src / "keys-to-success.md"
    if keys_src.exists():
        result = process_markdown_file(
            keys_src, 
            module_output, 
            f"module-{module_num}_keys-to-success"
        )
        results["files"] += sum(1 for v in result.values() if v)
    
    # Process questions.md
    questions_src = module_src / "questions.md"
    if questions_src.exists():
        result = process_markdown_file(
            questions_src, 
            module_output, 
            f"module-{module_num}_questions"
        )
        results["files"] += sum(1 for v in result.values() if v)
    
    # Copy slide PDFs from resources folder
    resources_dir = module_src / "resources"
    if resources_dir.exists():
        slides_output = module_output / "slides"
        for pdf_file in resources_dir.glob("*.pdf"):
            ensure_directory(slides_output)
            dst = slides_output / pdf_file.name
            if copy_file(pdf_file, dst):
                results["slides"] += 1
                results["files"] += 1
        
        # Also copy any PPT/PPTX files
        for ppt_file in list(resources_dir.glob("*.ppt")) + list(resources_dir.glob("*.pptx")):
            ensure_directory(slides_output)
            dst = slides_output / ppt_file.name
            if copy_file(ppt_file, dst):
                results["slides"] += 1
                results["files"] += 1
    
    return results


def publish_exams(output_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Publish exam files (student versions only, not keys)."""
    logger.info("📝 Publishing Exams...")
    
    exams_output = output_dir / "exams"
    exams_src = BIOL8_COURSE_DIR / "exams"
    results = {"files": 0, "errors": []}
    
    if dry_run:
        logger.info("  [DRY RUN] Would publish exam files")
        return results
    
    if not exams_src.exists():
        results["errors"].append("Exams directory not found")
        return results
    
    # Process only student-facing exams (not keys)
    for exam_file in exams_src.glob("*.md"):
        if "_key" in exam_file.name:
            continue  # Skip answer keys for student publication
        
        basename = exam_file.stem
        result = process_markdown_file(
            exam_file, 
            exams_output, 
            basename,
            formats=["pdf", "md", "docx"]  # No audio for exams
        )
        results["files"] += sum(1 for v in result.values() if v)
    
    logger.info(f"  ✓ Exams: {results['files']} files")
    return results


def publish_quizzes(output_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Publish quiz files (student versions only, not keys)."""
    logger.info("📋 Publishing Quizzes...")
    
    quizzes_output = output_dir / "quizzes"
    quizzes_src = BIOL8_COURSE_DIR / "quizzes"
    results = {"files": 0, "errors": []}
    
    if dry_run:
        logger.info("  [DRY RUN] Would publish quiz files")
        return results
    
    if not quizzes_src.exists():
        results["errors"].append("Quizzes directory not found")
        return results
    
    # Process only student-facing quizzes (not keys)
    for quiz_file in quizzes_src.glob("*.md"):
        if "_key" in quiz_file.name:
            continue  # Skip answer keys for student publication
        
        basename = quiz_file.stem
        result = process_markdown_file(
            quiz_file, 
            quizzes_output, 
            basename,
            formats=["pdf", "md", "docx"]  # No audio for quizzes
        )
        results["files"] += sum(1 for v in result.values() if v)
    
    logger.info(f"  ✓ Quizzes: {results['files']} files")
    return results


def publish_labs(output_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Publish lab protocol files."""
    logger.info("🔬 Publishing Labs...")
    
    labs_output = output_dir / "labs"
    labs_src = BIOL8_COURSE_DIR / "labs"
    results = {"files": 0, "errors": []}
    
    if dry_run:
        logger.info("  [DRY RUN] Would publish lab files")
        return results
    
    if not labs_src.exists():
        results["errors"].append("Labs directory not found")
        return results
    
    for lab_file in labs_src.glob("*.md"):
        basename = lab_file.stem
        result = process_markdown_file(
            lab_file, 
            labs_output, 
            basename,
            formats=["pdf", "md", "docx"]  # No audio for lab protocols
        )
        results["files"] += sum(1 for v in result.values() if v)
    
    logger.info(f"  ✓ Labs: {results['files']} files")
    return results


def create_index(output_dir: Path, stats: Dict[str, Any]) -> None:
    """Create an index file for the published course."""
    index_content = f"""# BIOL-8: Human Biology — Published Course Materials
## Spring 2026 | College of the Redwoods, Del Norte Campus

---

## Contents

### Syllabus
- [BIOL-8_Syllabus.pdf](syllabus/BIOL-8_Syllabus.pdf)
- [BIOL-8_Schedule.pdf](syllabus/BIOL-8_Schedule.pdf)

### Modules ({len(MODULES)} total)

| Module | Topic | Materials |
|--------|-------|-----------|
"""
    
    for num, topic in MODULES:
        module_name = f"module-{num}-{topic}"
        title = topic.replace("-", " ").title()
        index_content += f"| {num} | {title} | [Keys](modules/{module_name}/module-{num}_keys-to-success.pdf) · [Questions](modules/{module_name}/module-{num}_questions.pdf) |\n"
    
    index_content += """
### Assessments

- **Exams**: [exams/](exams/) — 4 exams (PDF, MD, DOCX)
- **Quizzes**: [quizzes/](quizzes/) — 15 module quizzes (PDF, MD, DOCX)
- **Labs**: [labs/](labs/) — 15 lab protocols (PDF, MD, DOCX)

---

## Publication Statistics

"""
    index_content += f"- **Modules processed**: {stats.get('modules', 0)}\n"
    index_content += f"- **Total files**: {stats.get('total_files', 0)}\n"
    index_content += f"- **Slide PDFs copied**: {stats.get('slides', 0)}\n"
    
    if stats.get('errors'):
        index_content += f"\n### Errors ({len(stats['errors'])})\n"
        for err in stats['errors']:
            index_content += f"- {err}\n"
    
    index_content += f"""
---

*Generated by publish_biol_8.py*
"""
    
    index_path = output_dir / "README.md"
    index_path.write_text(index_content)
    logger.info(f"📑 Created index: {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Publish BIOL-8 course materials to PUBLISHED/biol-8/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python publish_biol_8.py                    # Publish all materials
    python publish_biol_8.py --dry-run          # Preview without writing
    python publish_biol_8.py --modules 01 02    # Publish specific modules
    python publish_biol_8.py --clean            # Clean output before publishing
        """
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview what would be published without making changes"
    )
    parser.add_argument(
        "--modules", 
        nargs="+", 
        help="Specific module numbers to publish (e.g., 01 02 03)"
    )
    parser.add_argument(
        "--clean", 
        action="store_true", 
        help="Clean output directory before publishing"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("BIOL-8 Course Publisher")
    logger.info("=" * 60)
    logger.info(f"Source: {BIOL8_COURSE}")
    logger.info(f"Output: {PUBLISHED_DIR}")
    
    if args.dry_run:
        logger.info("MODE: Dry run (no files will be written)")
    
    # Clean output if requested
    if args.clean and PUBLISHED_DIR.exists() and not args.dry_run:
        logger.info("🧹 Cleaning output directory...")
        shutil.rmtree(PUBLISHED_DIR)
    
    # Ensure output directory exists
    if not args.dry_run:
        ensure_directory(PUBLISHED_DIR)
    
    # Track statistics
    stats = {
        "modules": 0,
        "total_files": 0,
        "slides": 0,
        "errors": []
    }
    
    # Publish syllabus
    syllabus_result = publish_syllabus(PUBLISHED_DIR, args.dry_run)
    stats["total_files"] += syllabus_result["files"]
    stats["errors"].extend(syllabus_result.get("errors", []))
    
    # Determine which modules to process
    if args.modules:
        modules_to_process = [
            (num, topic) for num, topic in MODULES 
            if num in args.modules
        ]
    else:
        modules_to_process = MODULES
    
    # Publish modules
    logger.info(f"📚 Publishing {len(modules_to_process)} Modules...")
    for module_num, module_topic in modules_to_process:
        result = publish_module(module_num, module_topic, PUBLISHED_DIR, args.dry_run)
        stats["modules"] += 1
        stats["total_files"] += result["files"]
        stats["slides"] += result.get("slides", 0)
        stats["errors"].extend(result.get("errors", []))
        
        if not args.dry_run:
            logger.info(f"  ✓ Module {module_num}: {result['files']} files" + 
                       (f" ({result['slides']} slides)" if result['slides'] else ""))
    
    # Publish exams
    exams_result = publish_exams(PUBLISHED_DIR, args.dry_run)
    stats["total_files"] += exams_result["files"]
    stats["errors"].extend(exams_result.get("errors", []))
    
    # Publish quizzes
    quizzes_result = publish_quizzes(PUBLISHED_DIR, args.dry_run)
    stats["total_files"] += quizzes_result["files"]
    stats["errors"].extend(quizzes_result.get("errors", []))
    
    # Publish labs
    labs_result = publish_labs(PUBLISHED_DIR, args.dry_run)
    stats["total_files"] += labs_result["files"]
    stats["errors"].extend(labs_result.get("errors", []))
    
    # Create index
    if not args.dry_run:
        create_index(PUBLISHED_DIR, stats)
    
    # Summary
    logger.info("=" * 60)
    logger.info("PUBLICATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"📊 Modules processed: {stats['modules']}")
    logger.info(f"📊 Total files published: {stats['total_files']}")
    logger.info(f"📊 Slide PDFs copied: {stats['slides']}")
    
    if stats["errors"]:
        logger.warning(f"⚠️  Errors encountered: {len(stats['errors'])}")
        for err in stats["errors"]:
            logger.warning(f"   - {err}")
    else:
        logger.info("✅ No errors")
    
    logger.info(f"\n📁 Output: {PUBLISHED_DIR}")


if __name__ == "__main__":
    main()
