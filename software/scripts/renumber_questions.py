#!/usr/bin/env python3
"""Script to renumber questions.md files to use continuous numbering.

Thin orchestrator - delegates to src.content_processing.

Usage:
    uv run python scripts/renumber_questions.py --course all
    uv run python scripts/renumber_questions.py --course biol-1
    uv run python scripts/renumber_questions.py --course biol-1 --module module-03
    uv run python scripts/renumber_questions.py --course all --dry-run --verbose
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.content_processing import renumber_questions_in_course
from src.shared.course_config import CourseSelectionError, resolve_course_selection


def main():
    """Process questions.md files in specified courses."""
    parser = argparse.ArgumentParser(
        description="Renumber questions.md files to use continuous numbering."
    )
    parser.add_argument(
        "--course",
        type=str,
        default="all",
        help="Active course to process, or all (default: all)"
    )
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Process a single module (e.g., module-03)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent

    try:
        courses = resolve_course_selection(args.course, repo_root)
    except CourseSelectionError as exc:
        parser.error(str(exc))

    prefix = "[DRY RUN] " if args.dry_run else ""

    # Delegate to module function
    results = renumber_questions_in_course(
        repo_root=repo_root,
        courses=courses,
        module_filter=args.module,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    # Display results
    for course_result in results["courses_processed"]:
        print(f"\n{'='*60}")
        print(f"{prefix}Processing {course_result['name'].upper()}")
        print('='*60)

        for module_info in course_result["modules"]:
            if module_info["converted"]:
                action = "WOULD CONVERT" if args.dry_run else "CONVERTED"
                status = f"✓ {action}"
            else:
                status = "○ OK"
            print(f"  {status} {module_info['name']}: {module_info['question_count']} questions")

    # Print summary
    print(f"\nTotal files converted: {results['files_converted']}")
    print(f"Total questions: {results['total_questions']}")

    if results["errors"]:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results["errors"]:
            print(f"  - {error}")
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
