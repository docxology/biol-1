#!/usr/bin/env python3
"""Script to generate HTML website for a module.

Usage:
    uv run python scripts/generate_module_website.py [OPTIONS]

Options:
    --course COURSE    Course: biol-1 or biol-8 (default: biol-1)
    --module MODULE    Module number to process (default: 1)
    --help             Show this help message

Examples:
    # Generate website for biol-1 module-1 (default)
    uv run python scripts/generate_module_website.py

    # Generate website for biol-8 module-2
    uv run python scripts/generate_module_website.py --course biol-8 --module 2
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.main import process_module_website


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate HTML website for a module.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Generate for biol-1/module-1 (default)
  %(prog)s --course biol-8         Generate for biol-8/module-1
  %(prog)s --module 2              Generate for biol-1/module-2
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
    """Generate HTML website for a module."""
    args = parse_args()

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    module_path = repo_root / "course_development" / args.course / "course" / f"module-{args.module}"

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

    print(f"Generating website for: {args.course}/course/module-{args.module}")

    try:
        html_file = process_module_website(str(module_path))
        print(f"\n✓ Website generated successfully!")
        print(f"Location: {html_file}")
        print(f"\nOpen in browser: file://{Path(html_file).absolute()}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

