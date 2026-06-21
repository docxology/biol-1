#!/usr/bin/env python3
"""Generate BIOL-1 slide decks from structured module manifests."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.shared.course_config import CourseSelectionError, find_repo_root, resolve_course_selection  # noqa: E402
from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

from src.slide_deck.main import describe_course_slide_decks, render_course_slide_decks  # noqa: E402

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BIOL-1 slide decks.")
    parser.add_argument("--course", default="all", help="Active course id or all")
    parser.add_argument("--module", type=int, default=None, help="Optional module number")
    parser.add_argument("--dry-run", action="store_true", help="Report generated files without writing")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = parse_args()
    repo_root = find_repo_root(Path(__file__))
    try:
        courses = resolve_course_selection(args.course, repo_root)
    except CourseSelectionError as exc:
        logger.error(str(exc))
        return 2

    total_written = 0
    for course in courses:
        course_root = repo_root / "course_development" / course
        if args.dry_run:
            logger.info(describe_course_slide_decks(course_root, args.module))
            continue
        result = render_course_slide_decks(course_root, args.module)
        total_written += int(result["written"])
        logger.info("%s: rendered %s slide decks, wrote %s files", course, result["module_count"], result["written"])
    if not args.dry_run:
        logger.info("Slide deck generation complete: %s files written", total_written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
