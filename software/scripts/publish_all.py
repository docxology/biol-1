#!/usr/bin/env python3
"""
Publish All Courses - Complete Pipeline

Thin orchestrator - delegates to src.publish and src.batch_processing modules.

This script orchestrates the full course publishing workflow:
1. Generate all outputs (PDF, DOCX, HTML, TXT, MP3) for all courses
2. Publish outputs to PUBLISHED/ directory
3. Copy labs and dashboards
4. Flatten module structure (remove subfolders)
5. Run validation

Usage:
    uv run python scripts/publish_all.py [--clean] [--skip-generation] [--verbose]
"""

import argparse
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(software_dir))

from src.batch_processing.main import clear_all_outputs
from src.publish.utils import (
    clean_published,
    copy_exams,
    copy_labs_and_dashboards,
    copy_practice_tests,
    copy_slides,
    copy_slides_to_modules,
    flatten_published,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent.parent


def run_script(script_name: str, args: list[str] = None, verbose: bool = False) -> bool:
    """Run a Python script and return success status."""
    repo_root = get_repo_root()
    script_path = repo_root / 'software' / 'scripts' / script_name
    
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return False
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    logger.info(f"Running: {script_name} {' '.join(args or [])}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(repo_root / 'software'),
            capture_output=not verbose,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Script failed: {script_name}")
            if not verbose and result.stderr:
                logger.error(result.stderr[-500:])
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error running {script_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Publish all courses - Complete pipeline'
    )
    parser.add_argument(
        '--clean', action='store_true',
        help='Clean PUBLISHED directory before starting'
    )
    parser.add_argument(
        '--skip-generation', action='store_true',
        help='Skip output generation (use existing outputs)'
    )
    parser.add_argument(
        '--skip-mp3', action='store_true',
        help='Skip MP3 audio generation (faster iteration)'
    )
    parser.add_argument(
        '--formats', type=str, default='all',
        help='Comma-separated formats: pdf,mp3,docx,html,txt (default: all)'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show detailed output from subscripts'
    )
    parser.add_argument(
        '--skip-publish', action='store_true',
        help='Skip publishing to PUBLISHED/ directory'
    )
    parser.add_argument(
        '--skip-copy-extras', action='store_true',
        help='Skip copying labs and dashboards'
    )
    parser.add_argument(
        '--skip-flatten', action='store_true',
        help='Skip flattening module structure'
    )
    parser.add_argument(
        '--skip-validate', action='store_true',
        help='Skip output validation'
    )
    parser.add_argument(
        '--skip-labs', action='store_true',
        help='Skip lab manual rendering during generation'
    )
    parser.add_argument(
        '--clean-source-outputs', action='store_true',
        help='Clean source output/ directories before generation'
    )

    args = parser.parse_args()
    
    start_time = time.time()
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    courses = ['biol-1', 'biol-8']
    
    print("\n" + "=" * 70)
    print("  PUBLISH ALL COURSES - Complete Pipeline")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70 + "\n")
    
    # Step 1: Clean if requested
    if args.clean:
        logger.info("STEP 1: Cleaning PUBLISHED directory")
        clean_published(published_dir)
    else:
        logger.info("STEP 1: Skipping clean (use --clean to clean first)")

    # Step 1.5: Clean source outputs if requested
    if args.clean_source_outputs:
        logger.info("\nSTEP 1.5: Cleaning source output directories")
        clear_results = clear_all_outputs(repo_root / 'course_development')
        logger.info(f"  ✓ Cleared {clear_results['total_files_removed']} files from {len(clear_results['cleared_directories'])} directories")

    # Step 2: Generate outputs
    if not args.skip_generation:
        logger.info("\nSTEP 2: Generating all outputs")

        # Build generation args
        gen_args = ['--course', 'all']

        # Handle format options
        if args.skip_mp3:
            gen_args.extend(['--formats', 'pdf,docx,html,txt'])
            logger.info("  Skipping MP3 generation (--skip-mp3)")
        elif args.formats != 'all':
            gen_args.extend(['--formats', args.formats])
            logger.info(f"  Formats: {args.formats}")

        # Pass through skip-labs flag
        if args.skip_labs:
            gen_args.append('--skip-labs')
            logger.info("  Skipping lab rendering (--skip-labs)")

        if not run_script('generate_all_outputs.py', gen_args, args.verbose):
            logger.error("Generation failed!")
            return 1
        logger.info("  ✓ Generation complete")
    else:
        logger.info("\nSTEP 2: Skipping generation (--skip-generation)")

    # Step 3: Publish to PUBLISHED/
    if not args.skip_publish:
        logger.info("\nSTEP 3: Publishing to PUBLISHED/")
        if not run_script('publish_course.py', ['--course', 'all'], args.verbose):
            logger.error("Publishing failed!")
            return 1
        logger.info("  ✓ Publishing complete")
    else:
        logger.info("\nSTEP 3: Skipping publish (--skip-publish)")

    # Step 4: Copy labs and dashboards
    if not args.skip_copy_extras:
        logger.info("\nSTEP 4: Copying labs and dashboards")
        copied = copy_labs_and_dashboards(repo_root, courses, args.verbose)
        logger.info(f"  ✓ Copied {copied} files")
    else:
        logger.info("\nSTEP 4: Skipping copy extras (--skip-copy-extras)")

    # Step 4.5: Copy slides, exams, and practice tests
    if not args.skip_copy_extras:
        logger.info("\nSTEP 4.5: Copying slides, exams, and practice tests")
        slides_copied = copy_slides(repo_root, courses, args.verbose)
        module_slides_copied = copy_slides_to_modules(repo_root, courses, args.verbose)
        exams_copied = copy_exams(repo_root, args.verbose)
        practice_tests_copied = copy_practice_tests(repo_root, courses, args.verbose)
        logger.info(f"  ✓ Copied {slides_copied} slides to central dir, {module_slides_copied} to module folders, {exams_copied} exams, {practice_tests_copied} practice tests")

    # Step 5: Flatten structure
    if not args.skip_flatten:
        logger.info("\nSTEP 5: Flattening module structure")
        moved = flatten_published(published_dir)
        logger.info(f"  ✓ Flattened {moved} files")
    else:
        logger.info("\nSTEP 5: Skipping flatten (--skip-flatten)")

    # Step 6: Validate
    if not args.skip_validate:
        logger.info("\nSTEP 6: Validating outputs")
        if not run_script('validate_outputs.py', ['--course', 'all'], args.verbose):
            logger.error("Validation failed!")
            return 1
        logger.info("  ✓ Validation complete")
    else:
        logger.info("\nSTEP 6: Skipping validation (--skip-validate)")
    
    # Summary
    duration = time.time() - start_time
    
    total_files = sum(1 for _ in published_dir.rglob('*') if _.is_file())
    
    # Calculate per-course breakdown
    course_counts = {}
    for course_dir in sorted(published_dir.iterdir()):
        if course_dir.is_dir() and not course_dir.name.startswith('.'):
            course_counts[course_dir.name] = sum(1 for _ in course_dir.rglob('*') if _.is_file())
    
    print("\n" + "=" * 70)
    print("  PUBLISH COMPLETE")
    print("=" * 70)
    print(f"  Total files in PUBLISHED: {total_files}")
    for course, count in course_counts.items():
        print(f"    {course}: {count} files")
    print(f"  Duration: {duration:.1f}s")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
