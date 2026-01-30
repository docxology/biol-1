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
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.logging_config import setup_logging
from src.legacy_import import (
    process_chapter_questions,
    process_slides,
    process_for_upload_all_modules,
)

# Setup logging
logger = setup_logging()


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
