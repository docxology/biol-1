"""Lab Manual rendering module for biology curriculum.

This module provides tools for rendering rich lab manuals from Markdown,
with support for data tables, fillable fields, measurement exercises,
and interactive worksheets.
"""

from .main import (
    batch_render_lab_manuals,
    generate_data_table,
    generate_measurement_table,
    get_lab_template,
    parse_lab_elements,
    render_lab_manual,
)

__all__ = [
    "batch_render_lab_manuals",
    "generate_data_table",
    "generate_measurement_table",
    "get_lab_template",
    "parse_lab_elements",
    "render_lab_manual",
]
