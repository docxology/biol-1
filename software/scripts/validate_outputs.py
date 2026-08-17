#!/usr/bin/env python3
"""Script to validate course outputs.

Usage:
    uv run python scripts/validate_outputs.py --course {biol-1|all}
    uv run python scripts/validate_outputs.py --course all --formats pdf,docx,md

Options:
    --course    Active course to validate (biol-1 or all)
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

# Add software directory to path
software_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(software_dir))

from src.shared.runtime import configure_runtime_environment

configure_runtime_environment()

from src.course_by_date import CalendarError, load_calendar, validate_generated_course_by_date
from src.lecture_create.validation import validate_module_lecture
from src.shared.course_config import CourseSelectionError, resolve_course_selection
from src.validation import (
    generate_validation_report,
    get_output_summary,
)
from src.validation.config import ALL_SUPPORTED_FORMATS, DEFAULT_REQUIRED_FORMATS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_formats(formats_str: str | None) -> list[str] | None:
    """Parse comma-separated formats string into list."""
    if not formats_str:
        return None
    formats = [f.strip().lower() for f in formats_str.split(",")]
    # Validate formats
    for fmt in formats:
        if fmt not in ALL_SUPPORTED_FORMATS:
            logger.warning(
                f"Unknown format '{fmt}' - valid formats: {', '.join(ALL_SUPPORTED_FORMATS)}"
            )
    return formats


def main():
    parser = argparse.ArgumentParser(description="Validate course outputs.")
    parser.add_argument(
        "--course", type=str, required=True, help="Active course to validate, or all"
    )
    parser.add_argument(
        "--formats",
        type=str,
        default=None,
        help=f"Comma-separated list of formats to validate (default: {','.join(DEFAULT_REQUIRED_FORMATS)}). "
        f"Valid formats: {','.join(ALL_SUPPORTED_FORMATS)}",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show detailed module-level results")
    parser.add_argument(
        "--validate-lectures",
        action="store_true",
        help="Validate lecture artifacts (video, captions, audio) in output/lectures/",
    )
    parser.add_argument(
        "--validate-course-by-date",
        action="store_true",
        help="Validate the generated BIOL-1 course/course_by_date projection",
    )
    parser.add_argument(
        "--max-module",
        type=str,
        action="append",
        default=[],
        help="Max module per course (format: course:number, e.g., biol-1:6)",
    )
    parser.add_argument(
        "--max-lab",
        type=str,
        action="append",
        default=[],
        help="Max lab per course (format: course:number, e.g., biol-1:4)",
    )
    parser.add_argument(
        "--strict-dashboards",
        action="store_true",
        help="Enforce per-numbered-lab dashboard invariant from COURSE_CONFIG "
        "(default 1 dashboard per numbered lab; per-course overrides when configured).",
    )

    args = parser.parse_args()

    repo_root = software_dir.parent
    formats = parse_formats(args.formats)

    # Parse module/lab limits into dicts
    module_limits = {}
    for limit in args.max_module:
        if ":" in limit:
            course, num = limit.split(":", 1)
            module_limits[course.lower()] = int(num)

    lab_limits = {}
    for limit in args.max_lab:
        if ":" in limit:
            course, num = limit.split(":", 1)
            lab_limits[course.lower()] = int(num)

    try:
        courses_to_validate = resolve_course_selection(args.course, repo_root)
    except CourseSelectionError as exc:
        parser.error(str(exc))

    # Log validation scope
    logger.info(f"\n{'=' * 60}")
    logger.info("VALIDATION SCOPE")
    logger.info(f"{'=' * 60}")
    logger.info(f"Courses: {', '.join(courses_to_validate)}")
    logger.info(
        f"Formats: {', '.join(formats) if formats else ', '.join(DEFAULT_REQUIRED_FORMATS) + ' (default)'}"
    )

    all_results = {}
    all_valid = True

    for course_name in courses_to_validate:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Validating {course_name.upper()}")
        logger.info(f"{'=' * 60}")

        # Generate full report with format filter and limits
        report = generate_validation_report(
            course_name,
            str(repo_root),
            formats=formats,
            max_module=module_limits.get(course_name),
            max_lab=lab_limits.get(course_name),
            strict_dashboards=args.strict_dashboards,
        )
        all_results[course_name] = report

        if not report["source_validation"].get("valid", False):
            all_valid = False

        # Display results
        if args.json:
            continue  # Will output all at end

        src = report["source_validation"]
        pub = report.get("published_validation", {})

        logger.info("\nSource Outputs:")
        logger.info(
            f"  Modules: {src.get('modules_valid', 0)}/{src.get('modules_checked', 0)} valid"
        )
        logger.info(f"  Syllabus: {'✓' if src.get('syllabus_valid') else '✗'}")

        invariant = src.get("dashboard_invariant")
        if invariant:
            checked = len(invariant.get("checked_labs", []))
            issues = len(invariant.get("issues", []))
            status = "✓" if invariant.get("valid") else "✗"
            logger.info(
                f"  Dashboard invariant (strict): {status} {checked} numbered labs, {issues} issue(s)"
            )

        if args.verbose and src.get("modules"):
            logger.info("\n  Module Details:")
            for mod in src["modules"]:
                status = "✓" if mod["valid"] else "✗"
                logger.info(f"    {status} {mod['name']}")
                if not mod["valid"] and mod.get("missing_files"):
                    for f in mod["missing_files"][:3]:  # Show first 3
                        logger.info(f"      - Missing: {f}")

        if src.get("issues"):
            logger.info("\n  Issues:")
            for issue in src["issues"]:
                logger.info(f"    ⚠ {issue}")

        # Published validation — reuse the result from generate_validation_report
        # (which already called validate_published internally) to avoid a redundant scan
        pub = report.get("published_validation", {})
        if pub and pub.get("courses", {}).get(course_name):
            course_pub = pub["courses"][course_name]
            n_modules = len(course_pub.get("modules", []))
            n_files = course_pub.get("total_files", 0)
            logger.info(
                f"\nPublished Outputs (PUBLISHED/{course_name}/, recursive, pre-ALL_FILES flatten):"
            )
            logger.info(f"  Total files: {n_files}  ({n_modules} module subdirs)")

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

    all_results["published"] = {
        "total_files": total_pub_files,
        "issues": all_pub_issues,
        "valid": all_pub_valid,
    }

    logger.info(f"\n{'=' * 60}")
    logger.info("PUBLISHED DIRECTORY SUMMARY (pre-ALL_FILES flatten)")
    logger.info(f"{'=' * 60}")
    logger.info(f"Total files across all courses (recursive): {total_pub_files}")
    for cname, count in sorted(per_course_pub.items()):
        logger.info(f"  {cname}: {count} files (recursive)")
    for issue in all_pub_issues:
        logger.info(f"  ⚠ {issue}")

    # JSON output
    if args.json:
        print(json.dumps(all_results, indent=2))

    # Opt-in: validate lecture artifacts
    lecture_valid = True
    if args.validate_lectures:
        lecture_valid = _validate_lectures(repo_root, courses_to_validate)
        all_valid = all_valid and lecture_valid

    date_map_valid = True
    if args.validate_course_by_date:
        date_map_valid = _validate_course_by_date(repo_root, courses_to_validate)
        all_valid = all_valid and date_map_valid

    # Final status
    logger.info(f"\n{'=' * 60}")
    if all_valid and all_pub_valid:
        logger.info("✓ All validations PASSED")
        return 0
    else:
        logger.info("✗ Some validations FAILED")
        return 1


def _validate_course_by_date(repo_root: Path, courses: list[str]) -> bool:
    """Validate generated date folders for courses that define a date map."""
    all_ok = True
    for course in courses:
        calendar_path = repo_root / "course_development" / course / "course_calendar.toml"
        if not calendar_path.exists():
            continue
        try:
            calendar = load_calendar(calendar_path)
            report = validate_generated_course_by_date(
                repo_root / "course_development" / course, calendar
            )
        except (CalendarError, OSError) as exc:
            logger.error("Course-by-date validation failed for %s: %s", course, exc)
            all_ok = False
        else:
            logger.info(
                "Course-by-date validation passed for %s: %s meetings, %s copied outputs",
                course,
                report["meetings"],
                report["copied_outputs"],
            )
    return all_ok


def _validate_lectures(repo_root: Path, courses: list[str]) -> bool:
    """Validate lecture artifacts in output/lectures/."""
    lectures_dir = repo_root / "output" / "lectures"
    if not lectures_dir.exists():
        logger.info("\nNo lecture output directory found — skipping lecture validation")
        return True

    module_dirs = sorted(d for d in lectures_dir.glob("module-*") if d.is_dir())
    if not module_dirs:
        logger.info("\nNo module lecture directories found — skipping lecture validation")
        return True

    logger.info(f"\n{'=' * 60}")
    logger.info("LECTURE VALIDATION")
    logger.info(f"Found {len(module_dirs)} module lecture directories")

    all_ok = True
    for mod_dir in module_dirs:
        name = mod_dir.name
        issues = []

        # Check for video
        video_dir = mod_dir / name / "video"
        video_file = video_dir / "lecture.mp4"
        if not video_file.exists():
            issues.append("missing lecture.mp4")
        elif video_file.stat().st_size == 0:
            issues.append("lecture.mp4 is empty")

        # Check for captions
        captions_dir = mod_dir / name / "captions"
        captions_file = captions_dir / "captions.srt"
        if not captions_file.exists():
            issues.append("missing captions.srt")

        # Check for audio
        audio_dir = mod_dir / name / "audio"
        if audio_dir.exists():
            wavs = sorted(audio_dir.glob("*.wav"))
            if not wavs:
                issues.append("no audio WAV files")
        else:
            issues.append("missing audio directory")

        # Check for PNGs
        png_dir = mod_dir / "png"
        if png_dir.exists():
            pngs = sorted(png_dir.glob("*.png"))
            if len(pngs) < 3:
                issues.append(f"only {len(pngs)} PNG(s), expected ≥3")
        else:
            issues.append("missing png directory")

        # Compare rendered lecture content with the authoritative module.toml.
        module_dir = repo_root / "course_development" / "biol-1" / "course" / name
        if module_dir.is_dir():
            issues.extend(
                f"semantic: {issue}" for issue in validate_module_lecture(module_dir, mod_dir)
            )
        else:
            issues.append(f"missing source module directory: {module_dir}")

        if issues:
            all_ok = False
            logger.info(f"  ✗ {name}: {', '.join(issues)}")
        else:
            logger.info(f"  ✓ {name}")

    if all_ok:
        logger.info("✓ All lecture validations PASSED")
    else:
        logger.info("✗ Some lecture validations FAILED")
    return all_ok


if __name__ == "__main__":
    sys.exit(main())
