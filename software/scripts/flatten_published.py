#!/usr/bin/env python3
"""Script to flatten the PUBLISHED directory structure.

Moves all files from subfolders (study-guides/, website/) directly into
the module folder root.

Usage:
    uv run python scripts/flatten_published.py
    uv run python scripts/flatten_published.py --path /custom/PUBLISHED
    uv run python scripts/flatten_published.py --dry-run --verbose
"""

import argparse
import shutil
from pathlib import Path


def flatten_module(module_dir: Path, dry_run: bool = False, verbose: bool = False) -> int:
    """Flatten a single module directory.

    Moves all files from subdirectories to the module root.
    Returns the count of files moved.
    """
    moved = 0

    # Get all subdirectories
    subdirs = [d for d in module_dir.iterdir() if d.is_dir()]

    for subdir in subdirs:
        # Move all files from subdirectory to module root
        for file in subdir.rglob('*'):
            if file.is_file():
                dest = module_dir / file.name
                # Handle potential name conflicts
                if dest.exists():
                    # Prefix with subdirectory name
                    dest = module_dir / f"{subdir.name}_{file.name}"
                if verbose:
                    print(f"    {file} -> {dest}")
                if not dry_run:
                    shutil.move(str(file), str(dest))
                moved += 1

        # Remove empty subdirectory
        if not dry_run:
            shutil.rmtree(subdir)

    return moved


def main():
    """Flatten all module directories in PUBLISHED."""
    parser = argparse.ArgumentParser(
        description="Flatten the PUBLISHED directory structure."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to PUBLISHED directory (default: auto-detect relative to repo root)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be flattened without doing it"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed file-level operations"
    )

    args = parser.parse_args()

    if args.path:
        published_dir = Path(args.path)
    else:
        published_dir = Path(__file__).parent.parent.parent / 'PUBLISHED'

    if not published_dir.exists():
        print(f"ERROR: PUBLISHED directory not found: {published_dir}")
        return 1

    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Flattening PUBLISHED directory: {published_dir}")
    print("=" * 60)

    for course_dir in sorted(published_dir.iterdir()):
        if not course_dir.is_dir() or course_dir.name.startswith('.'):
            continue

        print(f"\n{course_dir.name.upper()}")
        print("-" * 40)

        for module_dir in sorted(course_dir.iterdir()):
            if not module_dir.is_dir():
                continue

            # Skip special directories like labs, dashboards, syllabus
            if module_dir.name in ['labs', 'dashboards', 'syllabus']:
                print(f"  ○ Skipping {module_dir.name}")
                continue

            # Check if this is a module directory with subdirectories
            subdirs = [d for d in module_dir.iterdir() if d.is_dir()]
            if not subdirs:
                print(f"  ○ Already flat: {module_dir.name}")
                continue

            moved = flatten_module(module_dir, dry_run=args.dry_run, verbose=args.verbose)
            action = "Would flatten" if args.dry_run else "Flattened"
            print(f"  ✓ {action} {module_dir.name}: {moved} files moved")

    print("\n" + "=" * 60)
    print(f"{prefix}Flattening complete!")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
