#!/usr/bin/env python3
"""Top-level publish entrypoint. Reads publish.toml and delegates to publish_all.py."""

import argparse
import os
import subprocess
import sys
import tomllib
from pathlib import Path

# Set library path for macOS Homebrew (WeasyPrint needs GLib/GObject)
if sys.platform == "darwin":
    homebrew_lib = "/opt/homebrew/lib"
    current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if homebrew_lib not in current:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{homebrew_lib}:{current}" if current else homebrew_lib

REPO_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = REPO_ROOT / "publish.toml"
PUBLISH_SCRIPT = REPO_ROOT / "software" / "scripts" / "publish_all.py"


def load_config() -> dict:
    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f)


def enabled_formats(config: dict) -> list[str]:
    return [fmt for fmt, on in config["publish"]["formats"].items() if on]


def build_args(config: dict, override_formats: str | None = None) -> list[str]:
    pub = config["publish"]
    pipeline = pub.get("pipeline", {})
    args: list[str] = []

    if pub.get("clean"):
        args.append("--clean")
        args.append("--clean-source-outputs")
    if pub.get("verbose"):
        args.append("--verbose")

    # Pipeline stage toggles
    if not pipeline.get("generate", True):
        args.append("--skip-generation")
    if not pipeline.get("publish", True):
        args.append("--skip-publish")
    if not pipeline.get("copy_extras", True):
        args.append("--skip-copy-extras")
    if not pipeline.get("flatten", True):
        args.append("--skip-flatten")
    if not pipeline.get("validate", True):
        args.append("--skip-validate")

    # Per-course lab settings: skip labs if ALL enabled courses have include_labs=false
    courses = pub.get("courses", {})
    enabled_courses = {k: v for k, v in courses.items() if v.get("enabled", True)}
    if enabled_courses and all(not c.get("include_labs", True) for c in enabled_courses.values()):
        args.append("--skip-labs")

    # Formats
    if override_formats:
        args.extend(["--formats", override_formats])
    else:
        fmts = enabled_formats(config)
        if fmts:
            args.extend(["--formats", ",".join(fmts)])

    return args


def main():
    parser = argparse.ArgumentParser(description="Publish courses using publish.toml config")
    parser.add_argument("--dry-run", action="store_true", help="Show command without executing")
    parser.add_argument("--override-formats", type=str, default=None,
                        help="Override config formats (comma-separated, e.g. pdf,html)")
    cli = parser.parse_args()

    config = load_config()
    args = build_args(config, cli.override_formats)

    cmd = ["uv", "run", "python", str(PUBLISH_SCRIPT)] + args

    if cli.dry_run:
        pub = config["publish"]
        pipeline = pub.get("pipeline", {})
        courses_cfg = pub.get("courses", {})

        print("publish.toml config loaded:")
        print(f"  formats:  {enabled_formats(config)}")
        print(f"  clean:    {pub.get('clean')}")
        print(f"  verbose:  {pub.get('verbose')}")
        print(f"  pipeline: generate={pipeline.get('generate', True)}, "
              f"publish={pipeline.get('publish', True)}, "
              f"copy_extras={pipeline.get('copy_extras', True)}, "
              f"flatten={pipeline.get('flatten', True)}, "
              f"validate={pipeline.get('validate', True)}")
        for name, course in courses_cfg.items():
            print(f"  {name}: enabled={course.get('enabled', True)}, "
                  f"labs={course.get('include_labs', True)}, "
                  f"syllabus={course.get('include_syllabus', True)}, "
                  f"dashboards={course.get('include_dashboards', True)}")
        print()
        print("Would run (cwd: software/):")
        print(f"  {' '.join(cmd)}")
        return

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT / "software")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
