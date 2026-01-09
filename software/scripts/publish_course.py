#!/usr/bin/env python3
"""Script to publish course materials."""

import argparse
import sys
import logging
from pathlib import Path

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(software_dir))

from src.publish.main import publish_course

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Publish course materials.")
    parser.add_argument(
        "--course", 
        type=str, 
        choices=["biol-1", "biol-8", "all"],
        required=True, 
        help="Course to publish"
    )
    
    args = parser.parse_args()
    
    repo_root = software_dir.parent
    
    courses_to_process = []
    if args.course == "all":
        courses_to_process = ["biol-1", "biol-8"]
    else:
        courses_to_process = [args.course]
        
    for course_name in courses_to_process:
        course_path = repo_root / "course_development" / course_name
        
        if not course_path.exists():
            # Fallback for checking if it's already a full path or in root
            course_path = repo_root / course_name
            
        if not course_path.exists():
            logger.error(f"Course directory not found: {course_path}")
            continue
            
        try:
            results = publish_course(str(course_path))
            
            logger.info("=" * 60)
            logger.info(f"Publishing Results for {results['course']}")
            logger.info("=" * 60)
            logger.info(f"Modules processed: {results['modules_published']}")
            logger.info(f"Syllabus files: {results['syllabus_files']}")
            logger.info(f"Total files published: {results['total_files']}")
            
            if results["modules"]:
                logger.info("\nModule Details:")
                for mod in results["modules"]:
                    logger.info(f"  - {mod['name']}: {mod['files']} files")
            
        except Exception as e:
            logger.error(f"Failed to publish {course_name}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
