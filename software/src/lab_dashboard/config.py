"""Configuration for the lab_dashboard module."""

from pathlib import Path

# Repository root is two parents up from this package (software/src/lab_dashboard/)
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

# Directory where generated dashboard HTML files are written.
DASHBOARD_DIR: Path = REPO_ROOT / "course_development" / "biol-1" / "course" / "labs" / "dashboards"
