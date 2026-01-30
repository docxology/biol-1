#!/usr/bin/env python3
"""Top-level publish entrypoint. Reads publish.toml and delegates to publish_all.py."""

import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

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
    args: list[str] = []

    if pub.get("clean"):
        args.append("--clean")
    if pub.get("verbose"):
        args.append("--verbose")
    if not pub.get("pipeline", {}).get("generate", True):
        args.append("--skip-generation")

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
        print("publish.toml config loaded:")
        print(f"  formats: {enabled_formats(config)}")
        print(f"  clean:   {config['publish'].get('clean')}")
        print(f"  verbose: {config['publish'].get('verbose')}")
        print()
        print("Would run (cwd: software/):")
        print(f"  {' '.join(cmd)}")
        return

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT / "software")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
