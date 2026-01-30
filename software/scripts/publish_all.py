#!/usr/bin/env python3
"""
Publish All Courses - Complete Pipeline

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
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

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


def copy_labs_and_dashboards(verbose: bool = False) -> int:
    """Copy labs and dashboards to PUBLISHED directory."""
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    courses = ['biol-1', 'biol-8']
    total_copied = 0
    
    for course in courses:
        course_dev = repo_root / 'course_development' / course / 'course' / 'labs'
        course_pub = published_dir / course
        
        if not course_dev.exists():
            logger.warning(f"Labs directory not found: {course_dev}")
            continue
        
        # Create directories
        labs_pub = course_pub / 'labs'
        dashboards_pub = course_pub / 'dashboards'
        labs_pub.mkdir(parents=True, exist_ok=True)
        dashboards_pub.mkdir(parents=True, exist_ok=True)
        
        # Copy lab files
        for lab_file in course_dev.glob('lab-*.md'):
            dest = labs_pub / lab_file.name
            shutil.copy2(lab_file, dest)
            total_copied += 1
        
        # Copy lab outputs
        output_dir = course_dev / 'output'
        if output_dir.exists():
            for output_file in output_dir.iterdir():
                if output_file.is_file():
                    dest = labs_pub / output_file.name
                    shutil.copy2(output_file, dest)
                    total_copied += 1
        
        # Copy dashboards
        dashboards_dir = course_dev / 'dashboards'
        if dashboards_dir.exists():
            for dashboard_file in dashboards_dir.glob('*.html'):
                dest = dashboards_pub / dashboard_file.name
                shutil.copy2(dashboard_file, dest)
                total_copied += 1
        
        logger.info(f"  {course}: Copied labs and dashboards")
    
    return total_copied


def flatten_module(module_dir: Path) -> int:
    """Flatten a single module directory."""
    moved = 0
    subdirs = [d for d in module_dir.iterdir() if d.is_dir()]
    
    for subdir in subdirs:
        for file in subdir.rglob('*'):
            if file.is_file():
                dest = module_dir / file.name
                if dest.exists():
                    dest = module_dir / f"{subdir.name}_{file.name}"
                shutil.move(str(file), str(dest))
                moved += 1
        shutil.rmtree(subdir)
    
    return moved


def flatten_published() -> int:
    """Flatten all module directories in PUBLISHED."""
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    total_moved = 0
    
    for course_dir in published_dir.iterdir():
        if not course_dir.is_dir() or course_dir.name.startswith('.'):
            continue
        
        for module_dir in course_dir.iterdir():
            if not module_dir.is_dir():
                continue
            if module_dir.name in ['labs', 'dashboards', 'syllabus']:
                continue
            
            subdirs = [d for d in module_dir.iterdir() if d.is_dir()]
            if subdirs:
                moved = flatten_module(module_dir)
                total_moved += moved
    
    return total_moved


def clean_published():
    """Remove all content from PUBLISHED directory."""
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    
    if published_dir.exists():
        for item in published_dir.iterdir():
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    
    logger.info("Cleaned PUBLISHED directory")


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
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    print("\n" + "=" * 70)
    print("  PUBLISH ALL COURSES - Complete Pipeline")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70 + "\n")
    
    # Step 1: Clean if requested
    if args.clean:
        logger.info("STEP 1: Cleaning PUBLISHED directory")
        clean_published()
    else:
        logger.info("STEP 1: Skipping clean (use --clean to clean first)")
    
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
        
        if not run_script('generate_all_outputs.py', gen_args, args.verbose):
            logger.error("Generation failed!")
            return 1
        logger.info("  ✓ Generation complete")
    else:
        logger.info("\nSTEP 2: Skipping generation (--skip-generation)")
    
    # Step 3: Publish to PUBLISHED/
    logger.info("\nSTEP 3: Publishing to PUBLISHED/")
    if not run_script('publish_course.py', ['--course', 'all'], args.verbose):
        logger.error("Publishing failed!")
        return 1
    logger.info("  ✓ Publishing complete")
    
    # Step 4: Copy labs and dashboards
    logger.info("\nSTEP 4: Copying labs and dashboards")
    copied = copy_labs_and_dashboards(args.verbose)
    logger.info(f"  ✓ Copied {copied} files")
    
    # Step 5: Flatten structure
    logger.info("\nSTEP 5: Flattening module structure")
    moved = flatten_published()
    logger.info(f"  ✓ Flattened {moved} files")
    
    # Step 6: Validate
    logger.info("\nSTEP 6: Validating outputs")
    if not run_script('validate_outputs.py', ['--course', 'all'], args.verbose):
        logger.error("Validation failed!")
        return 1
    logger.info("  ✓ Validation complete")
    
    # Summary
    duration = time.time() - start_time
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    
    total_files = sum(1 for _ in published_dir.rglob('*') if _.is_file())
    
    print("\n" + "=" * 70)
    print("  PUBLISH COMPLETE")
    print("=" * 70)
    print(f"  Total files in PUBLISHED: {total_files}")
    print(f"  Duration: {duration:.1f}s")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
