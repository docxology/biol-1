#!/usr/bin/env python3
"""Generate the BIOL-1 course-by-date copy-only material projection."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.course_by_date import (
    CalendarError,
    generate_course_by_date,
    load_calendar,
    validate_generated_course_by_date,
)
from src.shared.course_config import find_repo_root

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course", default="biol-1", choices=("biol-1",))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-clean", action="store_true", help="Keep existing date folders")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = parse_args()
    repo_root = find_repo_root(Path(__file__))
    course_root = repo_root / "course_development" / args.course
    calendar_path = course_root / "course_calendar.toml"
    try:
        calendar = load_calendar(calendar_path)
        if args.validate_only:
            result = validate_generated_course_by_date(course_root, calendar)
        else:
            result = generate_course_by_date(
                course_root,
                calendar,
                clean=not args.no_clean,
                dry_run=args.dry_run,
            )
            if not args.dry_run:
                validate_generated_course_by_date(course_root, calendar)
    except CalendarError as exc:
        logger.error("Course-by-date generation failed: %s", exc)
        return 2
    logger.info(
        "%s: generated %s meeting folders and copied %s outputs into %s",
        args.course,
        result["meetings"],
        result.get("files", result.get("copied_outputs", 0)),
        result.get("output", course_root / "course" / "course_by_date"),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
