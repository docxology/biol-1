#!/usr/bin/env python3
"""Script to validate course outputs.

Usage:
    uv run python scripts/validate_outputs.py --course {biol-1|biol-8|all}
    uv run python scripts/validate_outputs.py --course all --formats pdf,docx,md
    
Options:
    --course    Course to validate (biol-1, biol-8, or all)
    --formats   Comma-separated list of formats to validate (default: pdf,docx)
                Only validates that these formats exist, ignoring others.
    --json      Output results as JSON
    --verbose   Show detailed module-level results
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(software_dir))

from src.validation import (
    generate_validation_report,
    get_output_summary,
    validate_outputs,
    validate_published,
)
from src.validation.config import DEFAULT_REQUIRED_FORMATS, ALL_SUPPORTED_FORMATS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def parse_formats(formats_str: Optional[str]) -> Optional[List[str]]:
    """Parse comma-separated formats string into list."""
    if not formats_str:
        return None
    formats = [f.strip().lower() for f in formats_str.split(',')]
    # Validate formats
    for fmt in formats:
        if fmt not in ALL_SUPPORTED_FORMATS:
            logger.warning(f"Unknown format '{fmt}' - valid formats: {', '.join(ALL_SUPPORTED_FORMATS)}")
    return formats


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
        "--formats",
        type=str,
        default=None,
        help=f"Comma-separated list of formats to validate (default: {','.join(DEFAULT_REQUIRED_FORMATS)}). "
             f"Valid formats: {','.join(ALL_SUPPORTED_FORMATS)}"
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
    parser.add_argument(
        "--max-module",
        type=str,
        action="append",
        default=[],
        help="Max module per course (format: course:number, e.g., biol-8:6)"
    )
    parser.add_argument(
        "--max-lab",
        type=str,
        action="append",
        default=[],
        help="Max lab per course (format: course:number, e.g., biol-8:4)"
    )
    
    args = parser.parse_args()
    
    repo_root = software_dir.parent
    formats = parse_formats(args.formats)
    
    # Parse module/lab limits into dicts
    module_limits = {}
    for limit in args.max_module:
        if ':' in limit:
            course, num = limit.split(':', 1)
            module_limits[course.lower()] = int(num)
    
    lab_limits = {}
    for limit in args.max_lab:
        if ':' in limit:
            course, num = limit.split(':', 1)
            lab_limits[course.lower()] = int(num)
    
    courses_to_validate = []
    if args.course == "all":
        courses_to_validate = ["biol-1", "biol-8"]
    else:
        courses_to_validate = [args.course]
    
    # Log validation scope
    logger.info(f"\n{'='*60}")
    logger.info("VALIDATION SCOPE")
    logger.info(f"{'='*60}")
    logger.info(f"Courses: {', '.join(courses_to_validate)}")
    logger.info(f"Formats: {', '.join(formats) if formats else ', '.join(DEFAULT_REQUIRED_FORMATS) + ' (default)'}")
        
    all_results = {}
    all_valid = True
    
    for course_name in courses_to_validate:
        logger.info(f"\n{'='*60}")
        logger.info(f"Validating {course_name.upper()}")
        logger.info(f"{'='*60}")
        
        # Generate full report with format filter and limits
        report = generate_validation_report(
            course_name,
            str(repo_root),
            formats=formats,
            max_module=module_limits.get(course_name),
            max_lab=lab_limits.get(course_name),
        )
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
                
        # Published validation — reuse the result from generate_validation_report
        # (which already called validate_published internally) to avoid a redundant scan
        pub = report.get("published_validation", {})
        if pub and pub.get("courses", {}).get(course_name):
            course_pub = pub["courses"][course_name]
            n_modules = len(course_pub.get("modules", []))
            n_files = course_pub.get("total_files", 0)
            logger.info(f"\nPublished Outputs:")
            logger.info(f"  Total files: {n_files}  ({n_modules} modules)")
            
        # Output summary
        course_path = repo_root / "course_development" / course_name
        if course_path.exists():
            summary = get_output_summary(str(course_path))
            by_fmt = summary.get("by_format", {})
            if by_fmt:
                fmt_str = "  ".join(f"{fmt}:{count}" for fmt, count in sorted(by_fmt.items()))
                logger.info(f"\nOutput Summary: {fmt_str}")
                
    # Aggregate published summary from already-computed per-course report data
    # (generate_validation_report already called validate_published internally —
    # no need to scan PUBLISHED/ a third time here)
    total_pub_files = 0
    all_pub_issues = []
    all_pub_valid = True
    per_course_pub: dict = {}
    for cname, report in all_results.items():
        if cname == "published":
            continue
        pub = report.get("published_validation", {})
        if pub:
            course_data = pub.get("courses", {}).get(cname, {})
            count = course_data.get("total_files", 0)
            total_pub_files += count
            per_course_pub[cname] = count
            all_pub_issues.extend(pub.get("issues", []))
            if not pub.get("valid", True):
                all_pub_valid = False

    all_results["published"] = {"total_files": total_pub_files, "issues": all_pub_issues, "valid": all_pub_valid}

    logger.info(f"\n{'='*60}")
    logger.info("PUBLISHED DIRECTORY SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total files: {total_pub_files}")
    for cname, count in sorted(per_course_pub.items()):
        logger.info(f"  {cname}: {count} files")
    for issue in all_pub_issues:
        logger.info(f"  ⚠ {issue}")

    # JSON output
    if args.json:
        print(json.dumps(all_results, indent=2))

    # Final status
    logger.info(f"\n{'='*60}")
    if all_valid and all_pub_valid:
        logger.info("✓ All validations PASSED")
        return 0
    else:
        logger.info("✗ Some validations FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

