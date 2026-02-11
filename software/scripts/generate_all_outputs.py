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
    --skip-labs        Skip lab manual rendering
    --help             Show this help message

Examples:
    uv run python scripts/generate_all_outputs.py
    uv run python scripts/generate_all_outputs.py --course biol-1
    uv run python scripts/generate_all_outputs.py --course biol-8 --module 1
    uv run python scripts/generate_all_outputs.py --formats mp3,txt
    uv run python scripts/generate_all_outputs.py --dry-run
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.config import AVAILABLE_COURSES, AVAILABLE_FORMATS
from src.batch_processing.logging_config import setup_logging
from src.batch_processing.main import (
    clear_all_outputs,
    process_course_exams,
    process_course_labs,
    process_course_modules,
    process_course_practice_tests,
    process_course_syllabus,
)
from src.batch_processing.utils import (
    generate_dry_run_report,
    get_courses_to_process,
    get_formats_to_process,
)

logger = setup_logging()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all outputs for course modules and syllabi.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--course", choices=AVAILABLE_COURSES + ["all"], default="all")
    parser.add_argument("--module", type=int)
    parser.add_argument("--formats", type=str, default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-clear", action="store_true")
    parser.add_argument("--no-website", action="store_true")
    parser.add_argument("--skip-labs", action="store_true")
    parser.add_argument("--max-module", type=str, action="append", default=[],
                        help="Max module per course (course:number, e.g., biol-8:6)")
    parser.add_argument("--max-lab", type=str, action="append", default=[],
                        help="Max lab per course (course:number, e.g., biol-8:5)")
    return parser.parse_args()


def parse_limits(limit_args: list) -> dict:
    """Parse course:number limits into {course: number} dict."""
    limits = {}
    for limit in limit_args:
        if ":" in limit:
            course, num = limit.split(":", 1)
            try:
                limits[course] = int(num)
            except ValueError:
                logger.warning(f"Invalid limit format: {limit}")
    return limits


def main() -> int:
    """Generate all outputs for all courses."""
    args = parse_args()
    start_time = time.time()
    repo_root = Path(__file__).parent.parent.parent

    courses = get_courses_to_process(args.course)
    formats = get_formats_to_process(args.formats)

    logger.info("=" * 60)
    logger.info("Starting comprehensive output generation")
    logger.info(f"Courses: {', '.join(c[1] for c in courses)} | Formats: {', '.join(formats)}")
    # Parse module/lab limits
    max_module_limits = parse_limits(args.max_module)
    max_lab_limits = parse_limits(args.max_lab)

    if args.module:
        logger.info(f"Module filter: module-{args.module}")
    if max_module_limits:
        logger.info(f"Max module limits: {max_module_limits}")
    if max_lab_limits:
        logger.info(f"Max lab limits: {max_lab_limits}")

    if args.dry_run:
        report = generate_dry_run_report(
            repo_root, courses, formats, args.module, not args.no_website, args.skip_labs
        )
        logger.info(report)
        return 0

    clear_results = {"total_files_removed": 0}
    if not args.skip_clear:
        clear_results = clear_all_outputs(repo_root)

    all_errors = []
    total_files = 0

    for course_dir, course_name in courses:
        course_path = repo_root / course_dir
        if not course_path.exists():
            continue

        # Get per-course limits (normalize course name to match config format)
        course_key = course_name.lower().replace(" ", "-")
        max_module = max_module_limits.get(course_key)
        max_lab = max_lab_limits.get(course_key)

        module_results = process_course_modules(
            course_path, course_name, args.module, not args.no_website, formats,
            max_module=max_module
        )
        all_errors.extend(module_results.get("errors", []))
        for m in module_results.get("modules", []):
            if "outputs" in m:
                total_files += sum(m["outputs"]["summary"].values())

        if not args.module:
            syl = process_course_syllabus(course_path, course_name, formats)
            all_errors.extend(syl.get("errors", []))
            if syl.get("processed"):
                total_files += sum(syl["results"]["summary"].values())

        if not args.module and not args.skip_labs:
            labs = process_course_labs(course_path, course_name, formats, max_lab=max_lab)
            all_errors.extend(labs.get("errors", []))
            if labs.get("processed"):
                total_files += len(labs.get("files", []))

        # Process practice tests (PDF generation)
        if not args.module:
            practice_tests = process_course_practice_tests(course_path, course_name, formats)
            all_errors.extend(practice_tests.get("errors", []))
            if practice_tests.get("processed"):
                total_files += len(practice_tests.get("files", []))

        # Process exams (PDF + DOCX generation, teacher-only local rendering)
        if not args.module:
            exams = process_course_exams(course_path, course_name, formats)
            all_errors.extend(exams.get("errors", []))
            if exams.get("processed"):
                total_files += len(exams.get("files", []))

    logger.info(f"\nTotal: {total_files} files generated in {time.time() - start_time:.2f}s")
    if all_errors:
        logger.warning(f"Errors: {len(all_errors)}")
        for e in all_errors[:10]:
            logger.error(f"  - {e}")
        return 1
    logger.info("All outputs generated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
