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
        
        # Copy lab outputs (both flat files and format subdirectories like output/pdf/, output/html/)
        output_dir = course_dev / 'output'
        if output_dir.exists():
            for output_file in output_dir.rglob('*'):
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


def copy_slides(verbose: bool = False) -> int:
    """Copy slide PDFs from resources/slides to PUBLISHED directory."""
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    total_copied = 0
    courses = ['biol-1', 'biol-8']
    
    for course in courses:
        slides_src = repo_root / 'course_development' / course / 'resources' / 'slides'
        slides_dest = published_dir / course / 'slides'
        
        if not slides_src.exists():
            continue
        
        slides_dest.mkdir(parents=True, exist_ok=True)
        course_copied = 0
        
        for slide_file in slides_src.glob('*.pdf'):
            dest = slides_dest / slide_file.name
            shutil.copy2(slide_file, dest)
            course_copied += 1
        
        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slide PDFs")
            total_copied += course_copied
    
    return total_copied


def copy_slides_to_modules(verbose: bool = False) -> int:
    """Copy slide PDFs into each module's published folder.
    
    Maps module directories (e.g., module-01-study-of-life/) to slide files
    (e.g., module-1-slides-full.pdf, module-1-slides-notes.pdf) and copies
    the slides into each module folder.
    """
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    total_copied = 0
    courses = ['biol-1', 'biol-8']
    
    for course in courses:
        slides_src = repo_root / 'course_development' / course / 'resources' / 'slides'
        course_pub = published_dir / course
        
        if not slides_src.exists() or not course_pub.exists():
            continue
        
        course_copied = 0
        
        # Find all module directories in published folder
        for module_dir in sorted(course_pub.iterdir()):
            if not module_dir.is_dir():
                continue
            # Skip non-module directories
            if not module_dir.name.startswith('module-'):
                continue
            
            # Extract module number from directory name (e.g., "module-01-study-of-life" -> 1)
            try:
                module_num = int(module_dir.name.split('-')[1])
            except (IndexError, ValueError):
                continue
            
            # Find matching slides (slides use single-digit pattern: module-1-slides-*.pdf)
            slide_pattern = f"module-{module_num}-slides-*.pdf"
            matching_slides = list(slides_src.glob(slide_pattern))
            
            for slide_file in matching_slides:
                dest = module_dir / slide_file.name
                shutil.copy2(slide_file, dest)
                course_copied += 1
        
        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slides into module folders")
            total_copied += course_copied
    
    return total_copied


def copy_exams(verbose: bool = False) -> int:
    """Copy exam files from course/exams to PUBLISHED directory."""
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    total_copied = 0
    
    # BIOL-8 has exams in course/exams/
    exams_src = repo_root / 'course_development' / 'biol-8' / 'course' / 'exams'
    exams_dest = published_dir / 'biol-8' / 'exams'
    
    if not exams_src.exists():
        logger.warning(f"Exams directory not found: {exams_src}")
        return 0
    
    exams_dest.mkdir(parents=True, exist_ok=True)
    
    # Copy exam markdown files (exclude answer keys with _key suffix)
    for exam_file in exams_src.glob('*.md'):
        if not exam_file.stem.endswith('_key'):
            dest = exams_dest / exam_file.name
            shutil.copy2(exam_file, dest)
            total_copied += 1
    
    # Copy exam outputs (PDF, DOCX, etc.) if they exist
    output_dir = exams_src / 'output'
    if output_dir.exists():
        for output_file in output_dir.rglob('*'):
            if output_file.is_file():
                dest = exams_dest / output_file.name
                shutil.copy2(output_file, dest)
                total_copied += 1
    
    if total_copied > 0:
        logger.info(f"  biol-8: Copied {total_copied} exam files")
    
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
            if module_dir.name in ['labs', 'dashboards', 'syllabus', 'slides', 'exams']:
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

    # Step 1.5: Clean source outputs if requested
    if args.clean_source_outputs:
        logger.info("\nSTEP 1.5: Cleaning source output directories")
        repo_root = get_repo_root()
        sys.path.insert(0, str(repo_root / 'software'))
        from src.batch_processing.main import clear_all_outputs
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
        copied = copy_labs_and_dashboards(args.verbose)
        logger.info(f"  ✓ Copied {copied} files")
    else:
        logger.info("\nSTEP 4: Skipping copy extras (--skip-copy-extras)")

    # Step 4.5: Copy slides and exams
    if not args.skip_copy_extras:
        logger.info("\nSTEP 4.5: Copying slides and exams")
        slides_copied = copy_slides(args.verbose)
        module_slides_copied = copy_slides_to_modules(args.verbose)
        exams_copied = copy_exams(args.verbose)
        logger.info(f"  ✓ Copied {slides_copied} slides to central dir, {module_slides_copied} to module folders, {exams_copied} exams")

    # Step 5: Flatten structure
    if not args.skip_flatten:
        logger.info("\nSTEP 5: Flattening module structure")
        moved = flatten_published()
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
    repo_root = get_repo_root()
    published_dir = repo_root / 'PUBLISHED'
    
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
