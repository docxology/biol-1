"""Tests for shared publish/course configuration helpers."""

import pytest

from src.shared.course_config import (
    PublishConfigError,
    active_course_names,
    enabled_publish_formats,
)


def test_enabled_publish_formats_rejects_unknown_format(temp_dir):
    """Unsupported publish.toml format keys fail immediately."""
    (temp_dir / "publish.toml").write_text(
        """
[publish]

[publish.formats]
pdf = true
epub = true

[publish.courses.biol-1]
enabled = true
path = "course_development/biol-1"
""",
        encoding="utf-8",
    )

    with pytest.raises(PublishConfigError, match="Unsupported format"):
        enabled_publish_formats(temp_dir)


def test_enabled_publish_formats_rejects_missing_formats_section(temp_dir):
    """A publish config without [publish.formats] is malformed."""
    (temp_dir / "publish.toml").write_text(
        """
[publish]

[publish.courses.biol-1]
enabled = true
path = "course_development/biol-1"
""",
        encoding="utf-8",
    )

    with pytest.raises(PublishConfigError, match="publish.formats"):
        enabled_publish_formats(temp_dir)


def test_active_course_names_rejects_missing_courses_section(temp_dir):
    """A publish config without [publish.courses] is malformed."""
    (temp_dir / "publish.toml").write_text(
        """
[publish]

[publish.formats]
pdf = true
""",
        encoding="utf-8",
    )

    with pytest.raises(PublishConfigError, match="publish.courses"):
        active_course_names(temp_dir)
