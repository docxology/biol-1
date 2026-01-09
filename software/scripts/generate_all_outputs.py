#!/usr/bin/env python3
"""Comprehensive script to generate all outputs for all modules and courses.

Usage:
    uv run python scripts/generate_all_outputs.py [OPTIONS]

Options:
    --course COURSE    Course to process: biol-1, biol-8, or all (default: all)
    --module MODULE    Specific module number to process (default: all)
    --formats FORMATS  Comma-separated list of formats: pdf,mp3,docx,html,txt (default: all)
    --dry-run          Show what would be generated without actually generating
    --skip-clear       Skip clearing existing outputs before generation
    --no-website       Skip website generation
    --help             Show this help message

Examples:
    # Generate all outputs for all courses
    uv run python scripts/generate_all_outputs.py

    # Generate only for BIOL-1
    uv run python scripts/generate_all_outputs.py --course biol-1

    # Generate only module 1 for BIOL-8
    uv run python scripts/generate_all_outputs.py --course biol-8 --module 1

    # Generate only MP3 and TXT formats (works without system dependencies)
    uv run python scripts/generate_all_outputs.py --formats mp3,txt

    # Dry run to see what would be generated
    uv run python scripts/generate_all_outputs.py --dry-run
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.logging_config import setup_logging
from src.batch_processing.main import (
    clear_all_outputs,
    process_module_by_type,
    process_module_website,
    process_syllabus,
)

# Setup logging
logger = setup_logging()

# Available options
AVAILABLE_COURSES = ["biol-1", "biol-8"]
AVAILABLE_FORMATS = ["pdf", "mp3", "docx", "html", "txt"]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all outputs for course modules and syllabi.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Generate all outputs for all courses
  %(prog)s --course biol-1          Generate only for BIOL-1
  %(prog)s --course biol-8 --module 1   Generate only module 1 for BIOL-8
  %(prog)s --formats mp3,txt        Generate only MP3 and TXT formats
  %(prog)s --dry-run                Show what would be generated
        """,
    )

    parser.add_argument(
        "--course",
        choices=AVAILABLE_COURSES + ["all"],
        default="all",
        help="Course to process (default: all)",
    )

    parser.add_argument(
        "--module",
        type=int,
        help="Specific module number to process (default: all modules)",
    )

    parser.add_argument(
        "--formats",
        type=str,
        default="all",
        help="Comma-separated list of formats: pdf,mp3,docx,html,txt (default: all)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without actually generating",
    )

    parser.add_argument(
        "--skip-clear",
        action="store_true",
        help="Skip clearing existing outputs before generation",
    )

    parser.add_argument(
        "--no-website",
        action="store_true",
        help="Skip website generation",
    )

    return parser.parse_args()


def get_courses_to_process(course_arg: str) -> List[tuple]:
    """Get list of courses to process based on argument."""
    all_courses = [
        ("course_development/biol-1", "BIOL-1"),
        ("course_development/biol-8", "BIOL-8"),
    ]

    if course_arg == "all":
        return all_courses

    return [(c, n) for c, n in all_courses if c.endswith(course_arg)]


def get_formats_to_process(formats_arg: str) -> List[str]:
    """Parse formats argument into list of formats."""
    if formats_arg == "all":
        return AVAILABLE_FORMATS

    formats = [f.strip().lower() for f in formats_arg.split(",")]
    invalid = [f for f in formats if f not in AVAILABLE_FORMATS]
    if invalid:
        logger.warning(f"Unknown formats will be ignored: {invalid}")

    return [f for f in formats if f in AVAILABLE_FORMATS]


def process_course_modules(
    course_path: Path,
    course_name: str,
    module_filter: Optional[int] = None,
    generate_website: bool = True,
) -> dict:
    """Process all modules for a course.

    Args:
        course_path: Path to course directory
        course_name: Name of the course
        module_filter: If specified, only process this module number
        generate_website: Whether to generate HTML websites for modules

    Returns:
        Dictionary with processing results
    """
    course_dir = course_path / "course"
    if not course_dir.exists():
        logger.warning(f"Course directory not found: {course_dir}")
        return {"modules": [], "errors": []}

    results = {
        "course": course_name,
        "modules": [],
        "errors": [],
    }

    # Find all modules
    modules = sorted([d for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("module-")])

    # Filter by module number if specified
    if module_filter is not None:
        modules = [m for m in modules if m.name == f"module-{module_filter}"]
        if not modules:
            logger.warning(f"Module module-{module_filter} not found in {course_name}")
            return results

    for module_dir in modules:
        module_name = module_dir.name
        logger.info(f"{'='*60}")
        logger.info(f"Processing {course_name} - {module_name}")
        logger.info(f"{'='*60}")

        # Process module outputs
        output_dir = module_dir / "output"
        module_start = time.time()
        try:
            module_results = process_module_by_type(str(module_dir), str(output_dir))
            module_duration = time.time() - module_start
            results["modules"].append({
                "name": module_name,
                "outputs": module_results,
                "duration": module_duration,
            })

            logger.info(f"{module_name} outputs generated in {module_duration:.2f}s:")
            logger.info(f"  PDF: {module_results['summary']['pdf']}")
            logger.info(f"  MP3: {module_results['summary']['mp3']}")
            logger.info(f"  DOCX: {module_results['summary']['docx']}")
            logger.info(f"  HTML: {module_results['summary']['html']}")
            logger.info(f"  TXT: {module_results['summary']['txt']}")

            if module_results["errors"]:
                logger.warning(f"Errors in {module_name}: {len(module_results['errors'])} errors")
                for error in module_results["errors"]:
                    logger.error(f"  {module_name}: {error}")
                    results["errors"].append(f"{module_name}: {error}")

        except Exception as e:
            error_msg = f"Failed to process {module_name}: {e}"
            logger.error(error_msg, exc_info=True)
            results["errors"].append(error_msg)
            continue

        # Generate website (if enabled)
        if generate_website:
            website_start = time.time()
            try:
                website_file = process_module_website(str(module_dir))
                website_duration = time.time() - website_start
                logger.info(f"Website generated in {website_duration:.2f}s: {website_file}")
            except Exception as e:
                error_msg = f"Failed to generate website for {module_name}: {e}"
                logger.error(error_msg, exc_info=True)
                results["errors"].append(error_msg)

    return results


def process_course_syllabus(course_path: Path, course_name: str) -> dict:
    """Process syllabus for a course.

    Args:
        course_path: Path to course directory
        course_name: Name of the course

    Returns:
        Dictionary with processing results
    """
    syllabus_dir = course_path / "syllabus"
    if not syllabus_dir.exists():
        logger.warning(f"Syllabus directory not found: {syllabus_dir}")
        return {"processed": False, "errors": []}

    logger.info(f"{'='*60}")
    logger.info(f"Processing {course_name} Syllabus")
    logger.info(f"{'='*60}")

    output_dir = syllabus_dir / "output"
    syllabus_start = time.time()

    try:
        results = process_syllabus(str(syllabus_dir), str(output_dir))
        syllabus_duration = time.time() - syllabus_start
        logger.info(f"Syllabus outputs generated in {syllabus_duration:.2f}s:")
        logger.info(f"  PDF: {results['summary']['pdf']}")
        logger.info(f"  MP3: {results['summary']['mp3']}")
        logger.info(f"  DOCX: {results['summary']['docx']}")
        logger.info(f"  HTML: {results['summary']['html']}")
        logger.info(f"  TXT: {results['summary']['txt']}")

        if results["errors"]:
            logger.warning(f"Errors in syllabus processing: {len(results['errors'])} errors")
            for error in results["errors"]:
                logger.error(f"  {error}")

        return {
            "processed": True,
            "results": results,
            "errors": results["errors"],
            "duration": syllabus_duration,
        }

    except Exception as e:
        error_msg = f"Failed to process syllabus: {e}"
        logger.error(error_msg, exc_info=True)
        return {"processed": False, "errors": [error_msg]}


def main() -> int:
    """Generate all outputs for all courses.
    
    Returns:
        Exit code (0 for success, 1 for errors)
    """
    # Parse command-line arguments
    args = parse_args()
    
    start_time = time.time()
    repo_root = Path(__file__).parent.parent.parent

    # Get courses and formats to process
    courses = get_courses_to_process(args.course)
    formats = get_formats_to_process(args.formats)

    logger.info("=" * 60)
    logger.info("Starting comprehensive output generation")
    logger.info("=" * 60)
    logger.info(f"Repository root: {repo_root}")
    logger.info(f"Courses: {', '.join(c[1] for c in courses)}")
    logger.info(f"Formats: {', '.join(formats)}")
    if args.module:
        logger.info(f"Module filter: module-{args.module}")
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be generated")
    if args.skip_clear:
        logger.info("Skipping output clearing")
    if args.no_website:
        logger.info("Website generation disabled")

    # Dry run mode - just show what would be processed
    if args.dry_run:
        logger.info("")
        logger.info("=" * 60)
        logger.info("DRY RUN - Files that would be processed:")
        logger.info("=" * 60)
        
        for course_dir, course_name in courses:
            course_path = repo_root / course_dir
            if not course_path.exists():
                continue
            
            logger.info(f"\n{course_name}:")
            course_dir_path = course_path / "course"
            if course_dir_path.exists():
                modules = sorted([d for d in course_dir_path.iterdir() 
                                  if d.is_dir() and d.name.startswith("module-")])
                
                # Filter by module number if specified
                if args.module:
                    modules = [m for m in modules if m.name == f"module-{args.module}"]
                
                for module_dir in modules:
                    md_files = list(module_dir.glob("*.md"))
                    assignment_files = list((module_dir / "assignments").glob("*.md")) if (module_dir / "assignments").exists() else []
                    logger.info(f"  {module_dir.name}: {len(md_files)} root files, {len(assignment_files)} assignments")
                    logger.info(f"    Would generate: {', '.join(formats)}")
                    if not args.no_website:
                        logger.info(f"    Would generate: website/index.html")
            
            syllabus_dir = course_path / "syllabus"
            if syllabus_dir.exists():
                syllabus_files = list(syllabus_dir.glob("*.md"))
                logger.info(f"  Syllabus: {len(syllabus_files)} files")
                logger.info(f"    Would generate: {', '.join(formats)}")
        
        logger.info("\nDry run complete. No files were generated.")
        return 0

    # Clear all outputs first (unless --skip-clear is set)
    clear_results = {"total_files_removed": 0}
    if not args.skip_clear:
        logger.info("Clearing all existing outputs...")
        clear_start = time.time()
        clear_results = clear_all_outputs(repo_root)
        clear_duration = time.time() - clear_start
        logger.info(f"Output clearing completed in {clear_duration:.2f}s")
    else:
        logger.info("Skipping output clearing (--skip-clear)")

    all_results = {
        "courses": [],
        "total_errors": [],
        "total_files_generated": 0,
    }

    for course_dir, course_name in courses:
        course_path = repo_root / course_dir

        if not course_path.exists():
            logger.warning(f"Course directory not found: {course_path}")
            continue

        logger.info("")
        logger.info("#" * 60)
        logger.info(f"# Processing {course_name}")
        logger.info("#" * 60)

        course_start = time.time()

        # Process modules (with optional module filter)
        module_results = process_course_modules(
            course_path, 
            course_name,
            module_filter=args.module,
            generate_website=not args.no_website,
        )
        all_results["courses"].append({
            "name": course_name,
            "modules": module_results,
        })

        # Process syllabus (only if not filtering by specific module)
        if not args.module:
            syllabus_results = process_course_syllabus(course_path, course_name)
            all_results["courses"][-1]["syllabus"] = syllabus_results
            all_results["total_errors"].extend(syllabus_results.get("errors", []))
            if syllabus_results.get("processed"):
                all_results["total_files_generated"] += sum(
                    syllabus_results["results"]["summary"].values()
                )

        # Collect errors and count files
        all_results["total_errors"].extend(module_results.get("errors", []))

        # Count generated files
        for module_info in module_results.get("modules", []):
            if "outputs" in module_info:
                all_results["total_files_generated"] += sum(
                    module_info["outputs"]["summary"].values()
                )

        course_duration = time.time() - course_start
        logger.info(f"Completed {course_name} in {course_duration:.2f}s")

    total_duration = time.time() - start_time

    # Print summary
    logger.info("")
    logger.info("#" * 60)
    logger.info("# Generation Summary")
    logger.info("#" * 60)

    for course_info in all_results["courses"]:
        logger.info(f"\n{course_info['name']}:")
        if "modules" in course_info:
            modules_processed = len(course_info["modules"].get("modules", []))
            logger.info(f"  Modules processed: {modules_processed}")
            # Log module durations
            for module_info in course_info["modules"].get("modules", []):
                if "duration" in module_info:
                    logger.debug(f"    {module_info['name']}: {module_info['duration']:.2f}s")
        if "syllabus" in course_info:
            if course_info["syllabus"].get("processed"):
                logger.info(f"  Syllabus: ✓ Processed")
                if "duration" in course_info["syllabus"]:
                    logger.debug(f"    Duration: {course_info['syllabus']['duration']:.2f}s")
            else:
                logger.warning(f"  Syllabus: ✗ Not processed")

    logger.info(f"\nTotal files generated: {all_results['total_files_generated']}")
    logger.info(f"Total duration: {total_duration:.2f}s")
    logger.info(f"Files cleared: {clear_results['total_files_removed']}")

    if all_results["total_errors"]:
        logger.warning(f"Total Errors: {len(all_results['total_errors'])}")
        for error in all_results["total_errors"][:10]:  # Show first 10
            logger.error(f"  - {error}")
        if len(all_results["total_errors"]) > 10:
            logger.warning(f"  ... and {len(all_results['total_errors']) - 10} more")
        return 1
    else:
        logger.info("All outputs generated successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())

