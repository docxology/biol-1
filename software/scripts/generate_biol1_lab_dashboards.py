#!/usr/bin/env python3
"""Generate aligned BIOL-1 lab dashboard HTML files.

Thin CLI orchestrator for the ``src.lab_dashboard`` package.  Parses
``--dry-run`` and ``--course`` arguments, delegates all business logic
to the module, and logs results.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.lab_dashboard.config import DASHBOARD_DIR, REPO_ROOT
from src.lab_dashboard.main import render_all_dashboards

logger = logging.getLogger(__name__)


def main() -> None:
    """CLI entry point — parse args and delegate to lab_dashboard module."""
    parser = argparse.ArgumentParser(
        description="Generate aligned BIOL-1 lab dashboard HTML files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render dashboards without writing files.",
    )
    parser.add_argument(
        "--course",
        default="biol-1",
        choices=["biol-1"],
        help="Course to generate dashboards for (default: biol-1).",
    )
    args = parser.parse_args()

    dashboard_dir: Path
    if args.course == "biol-1":
        dashboard_dir = DASHBOARD_DIR
    else:
        logger.error("Unsupported course: %s", args.course)
        sys.exit(1)

    logger.info(
        "Generating BIOL-1 lab dashboards in %s (dry_run=%s)",
        dashboard_dir,
        args.dry_run,
    )

    written = render_all_dashboards(dashboard_dir, dry_run=args.dry_run)

    if args.dry_run:
        logger.info("Dry run — %d dashboards would be written:", len(written))
    else:
        logger.info("Wrote %d dashboards:", len(written))

    for path_str in written:
        path = Path(path_str)
        try:
            rel = path.relative_to(REPO_ROOT)
            logger.info("  %s", rel)
        except ValueError:
            logger.info("  %s", path)

    logger.info("Done.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    main()
