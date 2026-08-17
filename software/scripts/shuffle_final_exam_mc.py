#!/usr/bin/env python3
"""Shuffle BIOL-1 final exam Part A MC options with a reproducible balanced-letter layout.

Thin CLI orchestrator over `src.exam_tools`. All parsing, shuffling, rendering, and
crosswalk verification logic lives in the package; this script only handles argument
parsing, file I/O, and logging.

Usage:
    uv run python scripts/shuffle_final_exam_mc.py [--dry-run]
    uv run python scripts/shuffle_final_exam_mc.py --spacing-only

Paths default to course_development/biol-1/course/exams/final-exam*.md under repo root.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.exam_tools import (
    FINAL_MC_SEED,
    crosswalk_verify,
    histogram_report,
    part_a_keyed_letters_from_key,
    reshape_part_a_spacing,
    shuffle_exam_markdown,
    update_key_part_a_answers,
)

logger = logging.getLogger(__name__)


def repo_root_from_scripts() -> Path:
    """Resolve the project root from this script's location (scripts/ → ../../)."""
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        stream=sys.stdout,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute shuffle only; do not write files.",
    )
    parser.add_argument(
        "--spacing-only",
        action="store_true",
        help=(
            "Re-render Part A with blank lines after stems and between options only "
            "(keep current option order and key untouched)."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=FINAL_MC_SEED,
        help="RNG seed (default FINAL_MC_SEED).",
    )
    args = parser.parse_args(argv)

    root = repo_root_from_scripts()
    exam_path = root / "course_development/biol-1/course/exams/final-exam.md"
    key_path = root / "course_development/biol-1/course/exams/final-exam_key.md"
    exam_text = exam_path.read_text(encoding="utf-8")
    key_text = key_path.read_text(encoding="utf-8")

    if args.spacing_only:
        keyed = part_a_keyed_letters_from_key(key_text)
        new_exam = reshape_part_a_spacing(exam_text, keyed)
        logger.info("Part A: reformatted spacing only (stem gap + blank lines between options).")
        if args.dry_run:
            return 0
        exam_path.write_text(new_exam, encoding="utf-8")
        logger.info("Wrote %s.", exam_path.relative_to(root))
        return 0

    new_exam, keyed = shuffle_exam_markdown(exam_text, seed=args.seed)
    crosswalk_verify(new_exam, keyed)
    logger.info("FINAL_MC_SEED=%s Part A histogram: %s", args.seed, histogram_report(keyed))

    if args.dry_run:
        return 0

    key_updated = update_key_part_a_answers(key_text, keyed)
    exam_path.write_text(new_exam, encoding="utf-8")
    key_path.write_text(key_updated, encoding="utf-8")
    logger.info("Wrote %s and %s.", exam_path.relative_to(root), key_path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
