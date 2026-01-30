#!/usr/bin/env python3
"""Script to renumber questions.md files to use continuous numbering.

This script converts section-based question files (with headers like "1. **Topic**")
to continuous numbered format (1. Question, 2. Question, etc.).

Usage:
    uv run python scripts/renumber_questions.py --course all
    uv run python scripts/renumber_questions.py --course biol-1
    uv run python scripts/renumber_questions.py --course biol-8 --module module-03
    uv run python scripts/renumber_questions.py --course all --dry-run --verbose
"""

import argparse
import re
from pathlib import Path


def extract_questions_from_sectioned(content: str) -> list[str]:
    """Extract all questions from a sectioned questions.md file.

    Handles format like:
    1.  **Topic Header**
        *   Question one?
        *   Question two?
    """
    questions = []

    # Find all bullet point questions (lines starting with * or -)
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        # Match lines that start with * or - and contain a question
        if stripped.startswith('*') or stripped.startswith('-'):
            # Remove the bullet point marker
            question = stripped.lstrip('*- \t')
            if question and len(question) > 5:  # Skip very short items
                questions.append(question)

    return questions


def format_as_continuous(questions: list[str], title: str) -> str:
    """Format questions as continuous numbered list."""
    lines = [f"# {title}", ""]

    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
        lines.append("")

    return '\n'.join(lines)


def process_questions_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> tuple[bool, int]:
    """Process a single questions.md file.

    Returns:
        Tuple of (was_changed, question_count)
    """
    content = filepath.read_text()

    # Check if already in continuous format (no ### sections with numbered headers)
    if not re.search(r'\n###\s+Part', content):
        # Already in continuous format
        count = len(re.findall(r'^\d+\.', content, re.MULTILINE))
        return False, count

    # Extract title from first line
    first_line = content.split('\n')[0]
    title = first_line.lstrip('# ').strip()

    # Extract questions
    questions = extract_questions_from_sectioned(content)

    if not questions:
        return False, 0

    # Generate new content
    new_content = format_as_continuous(questions, title)

    if verbose:
        print(f"    Title: {title}")
        print(f"    Questions extracted: {len(questions)}")

    # Write back
    if not dry_run:
        filepath.write_text(new_content)

    return True, len(questions)


def main():
    """Process questions.md files in specified courses."""
    parser = argparse.ArgumentParser(
        description="Renumber questions.md files to use continuous numbering."
    )
    parser.add_argument(
        "--course",
        type=str,
        choices=["biol-1", "biol-8", "all"],
        default="all",
        help="Course to process (default: all)"
    )
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Process a single module (e.g., module-03)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent

    if args.course == "all":
        courses = ['biol-1', 'biol-8']
    else:
        courses = [args.course]

    prefix = "[DRY RUN] " if args.dry_run else ""

    for course in courses:
        course_path = repo_root / 'course_development' / course / 'course'

        print(f"\n{'='*60}")
        print(f"{prefix}Processing {course.upper()}")
        print('='*60)

        if not course_path.exists():
            print(f"  ERROR: Course path not found: {course_path}")
            continue

        if args.module:
            # Process single module
            module_dirs = [course_path / args.module]
        else:
            module_dirs = sorted(course_path.glob('module-*'))

        for module_dir in module_dirs:
            if not module_dir.exists():
                print(f"  ✗ NOT FOUND {module_dir.name}")
                continue

            questions_file = module_dir / 'questions.md'

            if not questions_file.exists():
                print(f"  ✗ MISSING {module_dir.name}")
                continue

            was_changed, count = process_questions_file(
                questions_file, dry_run=args.dry_run, verbose=args.verbose
            )

            if was_changed:
                action = "WOULD CONVERT" if args.dry_run else "CONVERTED"
                status = f"✓ {action}"
            else:
                status = "○ OK"
            print(f"  {status} {module_dir.name}: {count} questions")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
