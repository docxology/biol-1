#!/usr/bin/env python3
"""Comprehensive script to generate all outputs for all modules and courses."""

import sys
import time
from datetime import datetime
from pathlib import Path

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


def process_course_modules(course_path: Path, course_name: str) -> dict:
    """Process all modules for a course.

    Args:
        course_path: Path to course directory
        course_name: Name of the course

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

        # Generate website
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


def main():
    """Generate all outputs for all courses."""
    start_time = time.time()
    repo_root = Path(__file__).parent.parent.parent

    logger.info("=" * 60)
    logger.info("Starting comprehensive output generation")
    logger.info("=" * 60)
    logger.info(f"Repository root: {repo_root}")

    # Clear all outputs first
    logger.info("Clearing all existing outputs...")
    clear_start = time.time()
    clear_results = clear_all_outputs(repo_root)
    clear_duration = time.time() - clear_start
    logger.info(f"Output clearing completed in {clear_duration:.2f}s")

    courses = [
        ("biol-1", "BIOL-1"),
        ("biol-8", "BIOL-8"),
    ]

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

        # Process modules
        module_results = process_course_modules(course_path, course_name)
        all_results["courses"].append({
            "name": course_name,
            "modules": module_results,
        })

        # Process syllabus
        syllabus_results = process_course_syllabus(course_path, course_name)
        all_results["courses"][-1]["syllabus"] = syllabus_results

        # Collect errors and count files
        all_results["total_errors"].extend(module_results.get("errors", []))
        all_results["total_errors"].extend(syllabus_results.get("errors", []))

        # Count generated files
        for module_info in module_results.get("modules", []):
            if "outputs" in module_info:
                all_results["total_files_generated"] += sum(
                    module_info["outputs"]["summary"].values()
                )
        if syllabus_results.get("processed"):
            all_results["total_files_generated"] += sum(
                syllabus_results["results"]["summary"].values()
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
