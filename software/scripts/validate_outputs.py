#!/usr/bin/env python3
"""Script to validate course outputs.

Usage:
    uv run python scripts/validate_outputs.py --course {biol-1|biol-8|all}
    
Options:
    --course    Course to validate (biol-1, biol-8, or all)
    --json      Output results as JSON
    --verbose   Show detailed module-level results
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(software_dir))

from src.validation import (
    generate_validation_report,
    get_output_summary,
    validate_outputs,
    validate_published,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Validate course outputs.")
    parser.add_argument(
        "--course",
        type=str,
        choices=["biol-1", "biol-8", "all"],
        required=True,
        help="Course to validate"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed module-level results"
    )
    
    args = parser.parse_args()
    
    repo_root = software_dir.parent
    
    courses_to_validate = []
    if args.course == "all":
        courses_to_validate = ["biol-1", "biol-8"]
    else:
        courses_to_validate = [args.course]
        
    all_results = {}
    all_valid = True
    
    for course_name in courses_to_validate:
        logger.info(f"\n{'='*60}")
        logger.info(f"Validating {course_name.upper()}")
        logger.info(f"{'='*60}")
        
        # Generate full report
        report = generate_validation_report(course_name, str(repo_root))
        all_results[course_name] = report
        
        if not report["source_validation"].get("valid", False):
            all_valid = False
            
        # Display results
        if args.json:
            continue  # Will output all at end
            
        src = report["source_validation"]
        pub = report.get("published_validation", {})
        
        logger.info(f"\nSource Outputs:")
        logger.info(f"  Modules: {src.get('modules_valid', 0)}/{src.get('modules_checked', 0)} valid")
        logger.info(f"  Syllabus: {'✓' if src.get('syllabus_valid') else '✗'}")
        
        if args.verbose and src.get("modules"):
            logger.info(f"\n  Module Details:")
            for mod in src["modules"]:
                status = "✓" if mod["valid"] else "✗"
                logger.info(f"    {status} {mod['name']}")
                if not mod["valid"] and mod.get("missing_files"):
                    for f in mod["missing_files"][:3]:  # Show first 3
                        logger.info(f"      - Missing: {f}")
                        
        if src.get("issues"):
            logger.info(f"\n  Issues:")
            for issue in src["issues"]:
                logger.info(f"    ⚠ {issue}")
                
        # Published validation  
        if pub and pub.get("courses", {}).get(course_name):
            course_pub = pub["courses"][course_name]
            logger.info(f"\nPublished Outputs:")
            logger.info(f"  Total files: {course_pub.get('total_files', 0)}")
            logger.info(f"  Modules: {len(course_pub.get('modules', []))}")
            
        # Output summary
        course_path = repo_root / "course_development" / course_name
        if course_path.exists():
            summary = get_output_summary(str(course_path))
            logger.info(f"\nOutput Summary:")
            for fmt, count in sorted(summary.get("by_format", {}).items()):
                logger.info(f"  {fmt}: {count} files")
                
    # Validate published directory overall
    published_path = repo_root / "PUBLISHED"
    pub_results = validate_published(str(published_path))
    all_results["published"] = pub_results
    
    logger.info(f"\n{'='*60}")
    logger.info("PUBLISHED DIRECTORY SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total files: {pub_results.get('total_files', 0)}")
    
    for course_name, course_data in pub_results.get("courses", {}).items():
        logger.info(f"  {course_name}: {course_data.get('total_files', 0)} files")
        
    if pub_results.get("issues"):
        for issue in pub_results["issues"]:
            logger.info(f"  ⚠ {issue}")
            
    # JSON output
    if args.json:
        print(json.dumps(all_results, indent=2))
        
    # Final status
    logger.info(f"\n{'='*60}")
    if all_valid and pub_results.get("valid", False):
        logger.info("✓ All validations PASSED")
        return 0
    else:
        logger.info("✗ Some validations FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
