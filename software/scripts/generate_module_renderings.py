#!/usr/bin/env python3
"""Script to generate all renderings for a specific module.

Usage:
    uv run python scripts/generate_module_renderings.py [OPTIONS]

Options:
    --course COURSE    Course: biol-1 or biol-8 (default: biol-1)
    --module MODULE    Module number to process (default: 1)
    --help             Show this help message

Examples:
    # Generate renderings for biol-1 module-1 (default)
    uv run python scripts/generate_module_renderings.py

    # Generate renderings for biol-8 module-2
    uv run python scripts/generate_module_renderings.py --course biol-8 --module 2
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.main import process_module_by_type


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all renderings for a specific module.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Generate for biol-1/module-1 (default)
  %(prog)s --course biol-8         Generate for biol-8/module-1
  %(prog)s --module 2              Generate for biol-1/module-2
  %(prog)s --course biol-8 --module 3   Generate for biol-8/module-3
        """,
    )

    parser.add_argument(
        "--course",
        choices=["biol-1", "biol-8"],
        default="biol-1",
        help="Course to process (default: biol-1)",
    )

    parser.add_argument(
        "--module",
        type=int,
        default=1,
        help="Module number to process (default: 1)",
    )

    return parser.parse_args()


def main() -> int:
    """Generate all renderings for a module."""
    args = parse_args()

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    module_path = repo_root / "course_development" / args.course / "course" / f"module-{args.module}"
    output_dir = module_path / "output"

    if not module_path.exists():
        print(f"Error: Module path does not exist: {module_path}")
        print(f"  Available modules in {args.course}:")
        course_dir = repo_root / "course_development" / args.course / "course"
        if course_dir.exists():
            modules = sorted([d.name for d in course_dir.iterdir() 
                             if d.is_dir() and d.name.startswith("module-")])
            for m in modules:
                print(f"    - {m}")
        return 1

    print(f"Processing: {args.course}/course/module-{args.module}")
    print(f"Output directory: {output_dir}")

    try:
        results = process_module_by_type(str(module_path), str(output_dir))

        # Print summary
        print("\n=== Generation Summary ===")
        print(f"PDF files: {results['summary']['pdf']}")
        print(f"Audio files (MP3): {results['summary']['mp3']}")
        print(f"DOCX files: {results['summary']['docx']}")
        print(f"HTML files: {results['summary']['html']}")
        print(f"TXT files: {results['summary']['txt']}")

        print("\n=== Files by Type ===")
        for file_type, files in results["by_type"].items():
            if files:
                print(f"\n{file_type}/ ({len(files)} files):")
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

