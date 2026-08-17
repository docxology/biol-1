"""Validation module for course output verification.

This module provides functions to validate that course outputs have been
generated correctly and published to the expected locations.
"""

from .main import (
    generate_validation_report,
    get_output_summary,
    validate_outputs,
    validate_published,
    validate_published_directory,
)

__all__ = [
    "generate_validation_report",
    "get_output_summary",
    "validate_outputs",
    "validate_published",
    "validate_published_directory",
]
