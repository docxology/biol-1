#!/usr/bin/env python3
"""Script to publish course materials."""

import argparse
import sys
import time
import logging
from pathlib import Path

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(software_dir))

from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

from src.publish.main import publish_course  # noqa: E402
from src.shared.course_config import CourseSelectionError, resolve_course_selection  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Publish course materials.")
    parser.add_argument("--course", type=str, required=True, help="Active course to publish, or all")
    
    args = parser.parse_args()
    
    repo_root = software_dir.parent
    try:
        courses_to_process = resolve_course_selection(args.course, repo_root)
    except CourseSelectionError as exc:
        parser.error(str(exc))
        
    for course_name in courses_to_process:
        course_path = repo_root / "course_development" / course_name
        
        if not course_path.exists():
            # Fallback for checking if it's already a full path or in root
            course_path = repo_root / course_name
            
        if not course_path.exists():
            logger.error(f"Course directory not found: {course_path}")
            continue
            
        try:
            t0 = time.time()
            results = publish_course(str(course_path))
            elapsed = time.time() - t0
            course_id = results['course']
            n_mod = results['modules_published']
            n_files = results['total_files']
            n_syl = results['syllabus_files']
            msg = f"  ✅ {course_id}: {n_mod} modules, {n_files} files published"
            if n_syl:
                msg += f" ({n_syl} syllabus)"
            msg += f" in {elapsed:.2f}s"
            logger.info(msg)
            if results.get('errors'):
                for err in results['errors']:
                    logger.warning(f"    ⚠ {err}")
            
        except Exception as e:
            logger.error(f"Failed to publish {course_name}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
