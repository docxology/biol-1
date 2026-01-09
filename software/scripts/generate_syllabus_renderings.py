#!/usr/bin/env python3
"""Script to generate all renderings for syllabus files.

Usage:
    uv run python scripts/generate_syllabus_renderings.py [OPTIONS]

Options:
    --course COURSE    Course: biol-1 or biol-8 (default: biol-1)
    --help             Show this help message

Examples:
    # Generate syllabus renderings for biol-1 (default)
    uv run python scripts/generate_syllabus_renderings.py

    # Generate syllabus renderings for biol-8
    uv run python scripts/generate_syllabus_renderings.py --course biol-8
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.main import process_syllabus


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all renderings for syllabus files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Generate for biol-1 syllabus (default)
  %(prog)s --course biol-8         Generate for biol-8 syllabus
        """,
    )

    parser.add_argument(
        "--course",
        choices=["biol-1", "biol-8"],
        default="biol-1",
        help="Course to process (default: biol-1)",
    )

    return parser.parse_args()


def main() -> int:
    """Generate all renderings for syllabus files."""
    args = parse_args()

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    syllabus_path = repo_root / "course_development" / args.course / "syllabus"
    output_dir = syllabus_path / "output"

    if not syllabus_path.exists():
        print(f"Error: Syllabus path does not exist: {syllabus_path}")
        return 1

    print(f"Processing: {args.course}/syllabus")
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

