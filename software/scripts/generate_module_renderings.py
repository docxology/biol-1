#!/usr/bin/env python3
"""Script to generate all renderings for a specific module.

Usage:
    uv run python scripts/generate_module_renderings.py [OPTIONS]

Options:
    --course COURSE    Active course (default: biol-1)
    --module MODULE    Module number to process (default: 1)
    --help             Show this help message

Examples:
    # Generate renderings for biol-1 module-1 (default)
    uv run python scripts/generate_module_renderings.py

    # Generate renderings for biol-1 module-2
    uv run python scripts/generate_module_renderings.py --course biol-1 --module 2
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

from scripts.utils import print_module_not_found  # noqa: E402
from src.batch_processing.main import process_module_by_type  # noqa: E402
from src.module_organization.utils import find_module_path  # noqa: E402
from src.shared.course_config import CourseSelectionError, active_course_names, resolve_course_selection  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all renderings for a specific module.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Generate for biol-1/module-1 (default)
  %(prog)s --course biol-1         Generate for biol-1/module-1
  %(prog)s --module 2              Generate for biol-1/module-2
  %(prog)s --course biol-1 --module 3   Generate for biol-1/module-3
        """,
    )

    active = ", ".join(active_course_names()) or "none"
    parser.add_argument(
        "--course",
        default="biol-1",
        help=f"Active course to process (active: {active}; default: biol-1)",
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
    try:
        [course_name] = resolve_course_selection(args.course)
    except CourseSelectionError as exc:
        logger.error(str(exc))
        return 2

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    course_path = repo_root / "course_development" / course_name

    # Find module path (supports both module-N and module-NN-topic patterns)
    module_path = find_module_path(course_path, args.module)

    if module_path is None:
        print_module_not_found(course_path, course_name, args.module)
        return 1

    output_dir = module_path / "output"

    logger.info(f"Processing: {course_name}/course/{module_path.name}")
    logger.info(f"Output directory: {output_dir}")

    try:
        results = process_module_by_type(str(module_path), str(output_dir))

        # Log summary
        logger.info("=== Generation Summary ===")
        logger.info(f"PDF files: {results['summary']['pdf']}")
        logger.info(f"Audio files (MP3): {results['summary']['mp3']}")
        logger.info(f"DOCX files: {results['summary']['docx']}")
        logger.info(f"HTML files: {results['summary']['html']}")
        logger.info(f"TXT files: {results['summary']['txt']}")

        logger.info("=== Files by Type ===")
        for file_type, files in results["by_type"].items():
            if files:
                logger.info(f"{file_type}/ ({len(files)} files):")
                for file_path in sorted(files):
                    logger.info(f"  - {Path(file_path).name}")

        if results["errors"]:
            logger.error("=== Errors ===")
            for error in results["errors"]:
                logger.error(f"  - {error}")
            return 1

        logger.info("All renderings generated successfully!")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
