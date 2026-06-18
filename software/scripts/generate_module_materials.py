#!/usr/bin/env python3
"""Generate BIOL-1 module Markdown and assets from structured module.toml files."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.module_content.main import (  # noqa: E402
    describe_course_module_materials,
    render_course_module_materials,
)
from src.shared.course_config import CourseSelectionError, find_repo_root, resolve_course_selection  # noqa: E402
from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate structured module materials.")
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
            logger.info(describe_course_module_materials(course_root, args.module))
            continue
        result = render_course_module_materials(course_root, args.module)
        total_written += int(result["written"])
        logger.info("%s: rendered %s modules, wrote %s files", course, result["module_count"], result["written"])
    if not args.dry_run:
        logger.info("Structured module material generation complete: %s files written", total_written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
