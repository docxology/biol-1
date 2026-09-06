#!/usr/bin/env python3
"""Generate BIOL-1 module lecture videos via LectureCreate.

For each module under course_development/biol-1/course/module-NN-*/:
  1. Generate a LectureCreate YAML manifest from module.toml
  2. Convert generated SVGs to PNGs for IMAGE beats
  3. Invoke lecturecreate to render the video

Usage:
    uv run python scripts/generate_module_videos.py --module 1
    uv run python scripts/generate_module_videos.py --all
    uv run python scripts/generate_module_videos.py --module 1 --dry-run
    uv run python scripts/generate_module_videos.py --module 1 --render
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lecture_create.main import (
    build_combined_lecture_yaml,
    build_module_lecture_yaml,
    enrich_narrations_with_llm,
    render_module_video,
)

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
COURSE_ROOT = REPO_ROOT / "course_development" / "biol-1"
MODULES_DIR = COURSE_ROOT / "course"
LECTURE_OUTPUT_ROOT = REPO_ROOT / "output" / "lectures"

#: Subprocess binary for lecturecreate; override with LECTURECREATE_BIN env var.
LECTURECREATE_BIN = os.environ.get("LECTURECREATE_BIN", "lecturecreate")

#: Canonical BIOL-1 render contract; override only for an intentional experiment.
LECTURECREATE_CONFIG = os.environ.get(
    "LECTURECREATE_CONFIG",
    str(REPO_ROOT / "software" / "src" / "lecture_create" / "biol-1.yaml"),
)

#: Default TTS backend — ``edge`` when available, else ``system``.
_DEFAULT_BACKEND = os.environ.get(
    "LECTURECREATE_BACKEND",
    "",
)


def _resolve_backend(requested: str) -> str:
    """Resolve the TTS backend, falling back when unavailable."""
    if requested and requested != "system":
        # Honour explicit backend requests
        return requested
    # Check if edge is available
    try:
        result = subprocess.run(
            [LECTURECREATE_BIN, "info"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if "edge       │ yes" in result.stdout:
            return "edge"
    except (OSError, subprocess.SubprocessError):
        logger.debug("LectureCreate backend probe failed", exc_info=True)
    return "system"


def _module_dirs(module_filter: int | None = None) -> list[Path]:
    """Return sorted module directories, optionally filtered by number."""
    modules = sorted(p for p in MODULES_DIR.glob("module-*") if p.is_dir())
    if module_filter is not None:
        modules = [p for p in modules if f"module-{module_filter:02d}" in p.name]
    return modules


def _convert_svgs_to_pngs(module_dir: Path, png_dir: Path) -> list[Path]:
    """Convert module generated SVGs to PNGs using cairosvg or rsvg-convert."""
    svg_dir = module_dir / "resources" / "generated"
    if not svg_dir.exists():
        return []

    png_dir.mkdir(parents=True, exist_ok=True)
    converted: list[Path] = []

    for svg_path in sorted(svg_dir.glob("*.svg")):
        png_path = png_dir / svg_path.with_suffix(".png").name

        try:
            import cairosvg

            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=1920)
        except ImportError:
            # fallback: rsvg-convert system binary
            result = subprocess.run(
                [
                    "rsvg-convert",
                    "-w",
                    "1920",
                    "--keep-aspect-ratio",
                    "-o",
                    str(png_path),
                    str(svg_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                print(
                    f"  WARNING: could not convert {svg_path.name}: {result.stderr.strip()}",
                    file=sys.stderr,
                )
                continue
        converted.append(png_path)

    return converted


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate BIOL-1 module lecture videos via LectureCreate"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--module", type=int, help="Generate for a single module number")
    group.add_argument("--all", action="store_true", help="Generate for all 16 modules")
    group.add_argument(
        "--combined",
        action="store_true",
        help="Generate a single combined lecture YAML for all 16 modules",
    )
    parser.add_argument("--dry-run", action="store_true", help="Write YAML only, do not render")
    parser.add_argument("--render", action="store_true", help="Render video after generating YAML")
    parser.add_argument(
        "--qr",
        action="store_true",
        help="Add per-slide QR codes linking to module source on GitHub",
    )
    parser.add_argument(
        "--lecturecreate-bin", default=LECTURECREATE_BIN, help="Path to lecturecreate executable"
    )
    parser.add_argument(
        "--config", default=LECTURECREATE_CONFIG, help="Path to LectureCreate render config"
    )
    parser.add_argument(
        "--backend",
        default="auto",
        choices=["auto", "system", "edge", "silent", "kokoro", "clone", "elevenlabs"],
        help="TTS backend (default: auto — uses edge if available, else system)",
    )
    parser.add_argument(
        "--llm-narration",
        action="store_true",
        help="Enrich narration with LLM pass reading full module content",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    # Resolve backend: "auto" → edge if available, else system
    backend = _resolve_backend(args.backend) if args.backend == "auto" else args.backend

    # --- Combined full-course mode ---
    if args.combined:
        out_dir = LECTURE_OUTPUT_ROOT / "biol-1-combined"
        yaml_path = out_dir / "biol-1-combined.yaml"

        print(f"\n{'=' * 60}")
        print("Full Course: BIOL-1 Combined Lecture")
        print(f"{'=' * 60}")

        print("  1. Generating combined YAML...")
        yaml_content = build_combined_lecture_yaml(MODULES_DIR, out_dir, args.config or None)
        out_dir.mkdir(parents=True, exist_ok=True)
        yaml_path.write_text(yaml_content, encoding="utf-8")
        print(f"     → {yaml_path}")

        # Copy all module PNGs into combined output
        png_dir = out_dir / "png"
        png_dir.mkdir(parents=True, exist_ok=True)
        png_count = 0
        for mod_dir in sorted(MODULES_DIR.glob("module-*")):
            if not mod_dir.is_dir():
                continue
            svg_dir = mod_dir / "resources" / "generated"
            if not svg_dir.exists():
                continue
            print(f"  2. Converting SVGs for {mod_dir.name}...")
            pngs = _convert_svgs_to_pngs(mod_dir, png_dir)
            png_count += len(pngs)
        print(f"     → {png_count} PNG(s) in {png_dir}")

        if args.render:
            print(f"  3. Rendering video via {args.lecturecreate_bin}...")
            result = render_module_video(
                yaml_path,
                out_dir,
                config_path=args.config or None,
                lecturecreate_bin=args.lecturecreate_bin,
                qr=args.qr,
                backend=backend,
            )
            if result.returncode == 0:
                print("     ✓ rendered")
            else:
                print(f"     ✗ failed (exit {result.returncode})", file=sys.stderr)
                if result.stderr:
                    print(f"       {result.stderr.strip()[:200]}", file=sys.stderr)

        print(f"\n{'=' * 60}")
        print("Done: 1 combined YAML written")
        print(f"Output: {out_dir}")
        return 0

    module_numbers: list[int]
    if args.all:
        module_numbers = list(range(1, 17))
    else:
        module_numbers = [args.module]

    total_yaml = 0
    total_rendered = 0

    for num in module_numbers:
        modules = _module_dirs(num)
        if not modules:
            print(f"Module {num:02d}: not found", file=sys.stderr)
            continue

        module_dir = modules[0]
        slug = module_dir.name
        out_dir = LECTURE_OUTPUT_ROOT / slug
        yaml_path = out_dir / f"{slug}.yaml"

        print(f"\n{'=' * 60}")
        print(f"Module {num:02d}: {slug}")
        print(f"{'=' * 60}")

        # Optional LLM narration enrichment
        if args.llm_narration:
            print("  0. Enriching narration via LLM...")
            from src.module_content.main import load_module_content

            mod = load_module_content(module_dir)
            enrich_narrations_with_llm(mod)
            print("     ✓ enriched")

        # Step 1: Generate YAML
        print("  1. Generating YAML...")
        yaml_content = build_module_lecture_yaml(
            module_dir,
            out_dir,
            lecturecreate_config_path=args.config or None,
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        yaml_path.write_text(yaml_content, encoding="utf-8")
        total_yaml += 1
        print(f"     → {yaml_path}")

        # Step 2: Convert SVGs to PNGs
        png_dir = out_dir / "png"
        print("  2. Converting SVGs to PNGs...")
        pngs = _convert_svgs_to_pngs(module_dir, png_dir)
        print(f"     → {len(pngs)} PNG(s) in {png_dir}")

        # Step 3: Render video (if requested)
        if args.render:
            print(f"  3. Rendering video via {args.lecturecreate_bin}...")
            result = render_module_video(
                yaml_path,
                out_dir,
                config_path=args.config or None,
                lecturecreate_bin=args.lecturecreate_bin,
                qr=args.qr,
                backend=backend,
            )
            if result.returncode == 0:
                total_rendered += 1
                print("     ✓ rendered")
            else:
                print(f"     ✗ failed (exit {result.returncode})", file=sys.stderr)
                if result.stderr:
                    print(f"       {result.stderr.strip()[:200]}", file=sys.stderr)
        elif not args.dry_run:
            print("  3. (use --render to invoke lecturecreate)")

    print(f"\n{'=' * 60}")
    print(f"Done: {total_yaml} YAML(s) written, {total_rendered} video(s) rendered")
    print(f"Output: {LECTURE_OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
