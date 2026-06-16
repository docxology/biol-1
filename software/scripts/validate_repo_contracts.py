#!/usr/bin/env python3
"""Validate repository-level documentation and publish contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

software_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(software_dir))

from src.shared.runtime import configure_runtime_environment  # noqa: E402
from src.validation.repo_contracts import validate_repo_contracts  # noqa: E402

configure_runtime_environment()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cr-bio repository contracts.")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    repo_root = software_dir.parent
    report = validate_repo_contracts(repo_root)

    if args.json:
        print(json.dumps({"valid": report.valid, "issues": report.issues, "summary": report.summary}, indent=2))
    else:
        print("Repository contract validation")
        print(f"  status: {'PASS' if report.valid else 'FAIL'}")
        for key, value in report.summary.items():
            print(f"  {key}: {value}")
        if report.issues:
            print("\nIssues:")
            for issue in report.issues:
                print(f"  - {issue}")

    return 0 if report.valid else 1


if __name__ == "__main__":
    sys.exit(main())
