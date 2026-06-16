#!/usr/bin/env python3
"""Script to generate all renderings for syllabus files.

Usage:
    uv run python scripts/generate_syllabus_renderings.py [OPTIONS]

Options:
    --course COURSE    Active course (default: biol-1)
    --help             Show this help message

Examples:
    # Generate syllabus renderings for biol-1 (default)
    uv run python scripts/generate_syllabus_renderings.py

    # Generate syllabus renderings for biol-1
    uv run python scripts/generate_syllabus_renderings.py --course biol-1
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

from src.batch_processing.main import process_syllabus  # noqa: E402
from src.shared.course_config import CourseSelectionError, active_course_names, resolve_course_selection  # noqa: E402


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all renderings for syllabus files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Generate for biol-1 syllabus (default)
  %(prog)s --course biol-1         Generate for biol-1 syllabus
        """,
    )

    active = ", ".join(active_course_names()) or "none"
    parser.add_argument(
        "--course",
        default="biol-1",
        help=f"Active course to process (active: {active}; default: biol-1)",
    )

    return parser.parse_args()


def main() -> int:
    """Generate all renderings for syllabus files."""
    args = parse_args()
    try:
        [course_name] = resolve_course_selection(args.course)
    except CourseSelectionError as exc:
        print(f"Error: {exc}")
        return 2

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    syllabus_path = repo_root / "course_development" / course_name / "syllabus"
    output_dir = syllabus_path / "output"

    if not syllabus_path.exists():
        print(f"Error: Syllabus path does not exist: {syllabus_path}")
        return 1

    print(f"Processing: {course_name}/syllabus")
    print(f"Output directory: {output_dir}")

    try:
        results = process_syllabus(str(syllabus_path), str(output_dir))

        # Print summary
        print("\n=== Generation Summary ===")
        print(f"PDF files: {results['summary']['pdf']}")
        print(f"Audio files (MP3): {results['summary']['mp3']}")
        print(f"DOCX files: {results['summary']['docx']}")
        print(f"HTML files: {results['summary']['html']}")
        print(f"TXT files: {results['summary']['txt']}")

        print("\n=== Files by Format ===")
        for format_type, files in results["by_format"].items():
            if files:
                print(f"\n{format_type}/ ({len(files)} files):")
                for file_path in sorted(files):
                    print(f"  - {Path(file_path).name}")

        if results["errors"]:
            print("\n=== Errors ===")
            for error in results["errors"]:
                print(f"  - {error}")
            return 1

        print("\n✓ All renderings generated successfully!")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
