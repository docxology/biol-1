"""Copy and reorganization functions for the publish module.

Handles copying labs, dashboards, slides, exams, practice tests, and
reorganizing the published directory from module-based to category-based
structure.
"""

import logging
import re
import shutil
from pathlib import Path

from src.shared.course_config import active_course_names

from . import config

logger = logging.getLogger(__name__)


def _active_courses(repo_root: Path) -> list[str]:
    """Return active course ids for publish helpers."""
    return active_course_names(repo_root) or ["biol-1"]


def copy_labs_and_dashboards(
    repo_root: Path, courses: list[str] | None = None, verbose: bool = False
) -> int:
    """Copy labs and dashboards to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = _active_courses(repo_root)

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        course_dev = repo_root / "course_development" / course / "course" / "labs"
        course_pub = published_dir / course

        if not course_dev.exists():
            logger.warning(f"Labs directory not found: {course_dev}")
            continue

        # Create directories
        labs_pub = course_pub / "labs"
        dashboards_pub = course_pub / "dashboards"
        labs_pub.mkdir(parents=True, exist_ok=True)
        dashboards_pub.mkdir(parents=True, exist_ok=True)

        # Copy lab files
        for lab_file in course_dev.glob("lab-*.md"):
            dest = labs_pub / lab_file.name
            shutil.copy2(lab_file, dest)
            total_copied += 1

        # Copy lab outputs (both flat files and format subdirectories)
        output_dir = course_dev / "output"
        if output_dir.exists():
            for output_file in output_dir.rglob("*"):
                if output_file.is_file():
                    dest = labs_pub / output_file.name
                    shutil.copy2(output_file, dest)
                    total_copied += 1

        # Copy dashboards
        dashboards_dir = course_dev / "dashboards"
        if dashboards_dir.exists():
            for dashboard_file in dashboards_dir.glob("*.html"):
                dest = dashboards_pub / dashboard_file.name
                shutil.copy2(dashboard_file, dest)
                total_copied += 1

        logger.info(f"  {course}: Copied labs and dashboards")

    return total_copied


def copy_slides(repo_root: Path, courses: list[str] | None = None, verbose: bool = False) -> int:
    """Copy slide PDFs from resources/slides to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = _active_courses(repo_root)

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        slides_src = repo_root / "course_development" / course / "resources" / "slides"
        slides_dest = published_dir / course / "slides"

        if not slides_src.exists():
            continue

        slides_dest.mkdir(parents=True, exist_ok=True)
        course_copied = 0

        for slide_file in slides_src.glob("*.pdf"):
            dest = slides_dest / slide_file.name
            shutil.copy2(slide_file, dest)
            course_copied += 1

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slide PDFs")
            total_copied += course_copied

    return total_copied


def copy_slides_to_modules(
    repo_root: Path, courses: list[str] | None = None, verbose: bool = False
) -> int:
    """Copy slide PDFs into each module's published folder.

    Maps module directories (e.g., module-01-exploring-life-science/) to slide files
    and copies slides into each module folder. Supports two naming conventions:
    - biol-1: module-{num}-slides-*.pdf (e.g., module-1-slides-full.pdf)
    - biol-8: Module {XX} - Topic.pdf (e.g., Module 01 - Exploring Life Science.pdf)

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = _active_courses(repo_root)

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        slides_src = repo_root / "course_development" / course / "resources" / "slides"
        course_pub = published_dir / course

        if not slides_src.exists() or not course_pub.exists():
            continue

        course_copied = 0

        for module_dir in sorted(course_pub.iterdir()):
            if not module_dir.is_dir():
                continue
            if not module_dir.name.startswith("module-"):
                continue

            # Extract module number from directory name (e.g., module-01-topic -> 1)
            try:
                module_num = int(module_dir.name.split("-")[1])
            except (IndexError, ValueError):
                continue

            # Try multiple slide naming patterns
            matching_slides: list[Path] = []

            # Pattern 1: module-{num}-slides-*.pdf (biol-1 style, no leading zeros)
            pattern1 = f"module-{module_num}-slides-*.pdf"
            matching_slides.extend(slides_src.glob(pattern1))

            # Pattern 2: Module {XX} - *.pdf (biol-8 style, with leading zeros)
            # Match files like "Module 01 - Exploring Life Science.pdf"
            module_num_padded = f"{module_num:02d}"
            pattern2 = f"Module {module_num_padded} - *.pdf"
            matching_slides.extend(slides_src.glob(pattern2))

            # Pattern 3: Module {X} - *.pdf (without leading zero, just in case)
            pattern3 = f"Module {module_num} - *.pdf"
            matching_slides.extend(slides_src.glob(pattern3))

            for slide_file in matching_slides:
                dest = module_dir / slide_file.name
                shutil.copy2(slide_file, dest)
                course_copied += 1
                if verbose:
                    logger.debug(f"    {slide_file.name} -> {module_dir.name}/")

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} slides into module folders")
            total_copied += course_copied

    return total_copied


def copy_exams(repo_root: Path, verbose: bool = False) -> int:
    """Copy exam files from course/exams to PUBLISHED directory.

    Args:
        repo_root: Path to the repository root
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    # BIOL-8 has exams in course/exams/
    exams_src = repo_root / "course_development" / "biol-8" / "course" / "exams"
    exams_dest = published_dir / "biol-8" / "exams"

    if not exams_src.exists():
        logger.warning(f"Exams directory not found: {exams_src}")
        return 0

    exams_dest.mkdir(parents=True, exist_ok=True)

    # Copy exam markdown files (exclude answer keys with _key suffix)
    for exam_file in exams_src.glob("*.md"):
        if not exam_file.stem.endswith("_key"):
            dest = exams_dest / exam_file.name
            shutil.copy2(exam_file, dest)
            total_copied += 1

    # Copy exam outputs (PDF, DOCX, etc.) if they exist
    output_dir = exams_src / "output"
    if output_dir.exists():
        for output_file in output_dir.rglob("*"):
            if output_file.is_file():
                dest = exams_dest / output_file.name
                shutil.copy2(output_file, dest)
                total_copied += 1

    if total_copied > 0:
        logger.info(f"  biol-8: Copied {total_copied} exam files")

    return total_copied


def copy_practice_tests(
    repo_root: Path, courses: list[str] | None = None, verbose: bool = False
) -> int:
    """Copy practice test files from course/practice_tests to PUBLISHED directory.

    Copies practice test markdown files (including answer keys) and any
    rendered outputs (PDF, DOCX). Both tests and answer keys are published
    so students can self-assess.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = _active_courses(repo_root)

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        practice_tests_src = repo_root / "course_development" / course / "course" / "practice_tests"
        practice_tests_dest = published_dir / course / "practice_tests"

        if not practice_tests_src.exists():
            if verbose:
                logger.debug(f"Practice tests directory not found: {practice_tests_src}")
            continue

        practice_tests_dest.mkdir(parents=True, exist_ok=True)
        course_copied = 0

        # Copy practice test markdown files (including answer keys)
        for test_file in practice_tests_src.glob("*.md"):
            if test_file.name in ("README.md", "AGENTS.md"):
                continue  # Skip instructor-facing docs; PUBLISHED is fully generated
            dest = practice_tests_dest / test_file.name
            shutil.copy2(test_file, dest)
            course_copied += 1

        # Copy practice test outputs (PDF, DOCX, etc.) if they exist
        output_dir = practice_tests_src / "output"
        if output_dir.exists():
            for output_file in output_dir.rglob("*"):
                if output_file.is_file():
                    dest = practice_tests_dest / output_file.name
                    shutil.copy2(output_file, dest)
                    course_copied += 1

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} practice test files")
            total_copied += course_copied

    return total_copied


def copy_module_generated_assets(
    repo_root: Path,
    courses: list[str] | None = None,
    verbose: bool = False,
) -> int:
    """Copy each module's deterministic generated SVG assets into PUBLISHED.

    Each module's ``resources/generated/*.svg`` (concept map, process model,
    retrieval card) is linked from its ``key-points.md`` via relative
    paths like ``resources/generated/module-NN-concept-map.svg``. Those links
    must resolve both from the flattened ``module_keys/`` category folder and
    from the per-module ``modules/<slug>/`` bundle, so the assets are copied
    into a ``resources/generated/`` subdirectory alongside each destination.

    Must run after ``copy_module_bundles`` (which rebuilds ``modules/`` from
    scratch on every publish), otherwise this step's output there would be
    wiped.

    Args:
        repo_root: Path to the repository root
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Number of files copied
    """
    if courses is None:
        courses = _active_courses(repo_root)

    published_dir = repo_root / config.PUBLISH_ROOT_NAME
    total_copied = 0

    for course in courses:
        course_dev = repo_root / "course_development" / course / "course"
        course_pub = published_dir / course
        modules_pub = course_pub / "modules"

        if not course_dev.exists() or not course_pub.exists():
            continue

        course_copied = 0

        for module_dir in sorted(course_dev.glob("module-*")):
            if not module_dir.is_dir():
                continue

            generated_dir = module_dir / "resources" / "generated"
            if not generated_dir.exists():
                continue

            svg_files = sorted(generated_dir.glob("*.svg"))
            if not svg_files:
                continue

            # Shared flattened destination alongside module_keys/homework
            # (filenames are module-number-prefixed, so no cross-module
            # collisions when merged into one directory per course).
            module_keys_generated = course_pub / "module_keys" / "resources" / "generated"
            module_keys_generated.mkdir(parents=True, exist_ok=True)
            for svg_file in svg_files:
                shutil.copy2(svg_file, module_keys_generated / svg_file.name)
                course_copied += 1

            # Per-module nested bundle destination.
            module_slug = module_dir.name
            module_bundle_dir = modules_pub / module_slug
            if module_bundle_dir.exists():
                bundle_generated = module_bundle_dir / "resources" / "generated"
                bundle_generated.mkdir(parents=True, exist_ok=True)
                for svg_file in svg_files:
                    shutil.copy2(svg_file, bundle_generated / svg_file.name)
                    course_copied += 1

            if verbose:
                logger.debug(f"    {module_slug}: copied {len(svg_files)} generated asset(s)")

        if course_copied > 0:
            logger.info(f"  {course}: Copied {course_copied} generated module assets")
            total_copied += course_copied

    return total_copied


def reorganize_to_categories(
    published_dir: Path, courses: list[str] | None = None, verbose: bool = False
) -> int:
    """Reorganize PUBLISHED directory from module-based to category-based structure.

    Transforms:
        module-XX-*/key-points files -> module_keys/
        module-XX-*/questions files -> homework/
        module-XX-*/website (index.html) -> removed
        module-XX-*/slides -> slides/
        syllabus/ -> course/

    Args:
        published_dir: Path to the PUBLISHED directory
        courses: List of course names (default: active courses from publish.toml)
        verbose: If True, log detailed operations

    Returns:
        Total number of files reorganized
    """
    if courses is None:
        courses = _active_courses(published_dir.parent)

    total_moved = 0

    for course in courses:
        course_dir = published_dir / course
        if not course_dir.exists():
            continue

        # Create category directories
        homework_dir = course_dir / "homework"
        module_keys_dir = course_dir / "module_keys"
        course_info_dir = course_dir / "course"

        homework_dir.mkdir(parents=True, exist_ok=True)
        module_keys_dir.mkdir(parents=True, exist_ok=True)
        course_info_dir.mkdir(parents=True, exist_ok=True)

        # Rename syllabus -> course (if syllabus exists)
        syllabus_dir = course_dir / "syllabus"
        if syllabus_dir.exists():
            for f in syllabus_dir.iterdir():
                if f.is_file():
                    dest = course_info_dir / f.name
                    shutil.move(str(f), str(dest))
                    total_moved += 1
                    if verbose:
                        logger.debug(f"  {f.name} -> course/")
            # Remove empty syllabus directory
            if syllabus_dir.exists() and not any(syllabus_dir.iterdir()):
                syllabus_dir.rmdir()

        # Process each module directory
        module_dirs = sorted(
            [d for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("module-")]
        )

        for module_dir in module_dirs:
            for f in list(module_dir.iterdir()):
                if not f.is_file():
                    continue

                fname = f.name.lower()

                # Questions files -> homework/
                if "questions" in fname:
                    dest = homework_dir / f.name
                    shutil.move(str(f), str(dest))
                    total_moved += 1
                    if verbose:
                        logger.debug(f"  {f.name} -> homework/")

                # Key-points files -> module_keys/
                elif "key-points" in fname:
                    dest = module_keys_dir / f.name
                    shutil.move(str(f), str(dest))
                    total_moved += 1
                    if verbose:
                        logger.debug(f"  {f.name} -> module_keys/")

                # Slides files -> slides/ (they might already be there, but handle duplicates)
                # Matches both: "module-X-slides-*.pdf" and "Module XX - Topic.pdf"
                elif fname.endswith(".pdf") and ("slides" in fname or fname.startswith("module ")):
                    slides_dir = course_dir / "slides"
                    slides_dir.mkdir(parents=True, exist_ok=True)
                    dest = slides_dir / f.name
                    if not dest.exists():
                        shutil.move(str(f), str(dest))
                        total_moved += 1
                        if verbose:
                            logger.debug(f"  {f.name} -> slides/")

                    else:
                        # Duplicate slide - remove from module
                        f.unlink()

                # Remove website files (index.html)
                elif fname == "index.html":
                    f.unlink()
                    if verbose:
                        logger.debug(f"  Removed {f.name}")

            # Remove empty module directory
            if module_dir.exists() and not any(module_dir.iterdir()):
                module_dir.rmdir()
                if verbose:
                    logger.debug(f"  Removed empty {module_dir.name}/")

        logger.info(f"  {course}: Reorganized to category structure")

    return total_moved


def copy_module_bundles(
    published_dir: Path, courses: list[str] | None = None, verbose: bool = False
) -> int:
    if courses is None:
        courses = _active_courses(published_dir.parent)

    total_copied = 0
    for course in courses:
        course_dir = published_dir / course
        if not course_dir.exists():
            continue
        modules_dir = course_dir / "modules"
        if modules_dir.exists():
            shutil.rmtree(modules_dir)
        modules_dir.mkdir(parents=True, exist_ok=True)

        module_slugs = _published_module_slugs(course_dir)
        course_copied = 0
        for number, slug in sorted(module_slugs.items()):
            module_dir = modules_dir / slug
            module_dir.mkdir(parents=True, exist_ok=True)
            course_copied += _copy_module_prefix_files(course_dir / "module_keys", module_dir, slug)
            course_copied += _copy_module_prefix_files(course_dir / "homework", module_dir, slug)
            course_copied += _copy_matching_files(
                course_dir / "slides",
                module_dir,
                (f"module-{number}-slides-", f"module-{number:02d}-slides-"),
            )
            course_copied += _copy_matching_files(
                course_dir / "labs",
                module_dir,
                (f"lab-{number:02d}_",),
            )
            course_copied += _copy_matching_files(
                course_dir / "dashboards",
                module_dir,
                (f"lab-{number:02d}_",),
            )
            if verbose:
                logger.debug("  %s: bundled %s", course, slug)

        if course_copied > 0:
            logger.info("  %s: Copied %s files into per-module bundles", course, course_copied)
            total_copied += course_copied

    return total_copied


def _published_module_slugs(course_dir: Path) -> dict[int, str]:
    slugs: dict[int, str] = {}
    for category_name in ("module_keys", "homework"):
        category_dir = course_dir / category_name
        if not category_dir.exists():
            continue
        for file_path in category_dir.iterdir():
            if not file_path.is_file():
                continue
            match = re.match(r"(module-(\d{2})-.+?)-(?:key-points|questions)\.", file_path.name)
            if match:
                slugs[int(match.group(2))] = match.group(1)
    return slugs


def _copy_module_prefix_files(src_dir: Path, dest_dir: Path, module_slug: str) -> int:
    return _copy_matching_files(src_dir, dest_dir, (f"{module_slug}-",))


def _copy_matching_files(src_dir: Path, dest_dir: Path, prefixes: tuple[str, ...]) -> int:
    if not src_dir.exists():
        return 0
    copied = 0
    for file_path in sorted(src_dir.iterdir()):
        if not file_path.is_file():
            continue
        if not any(file_path.name.startswith(prefix) for prefix in prefixes):
            continue
        shutil.copy2(file_path, dest_dir / file_path.name)
        copied += 1
    return copied
