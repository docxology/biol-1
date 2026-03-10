"""One-time migration utility for bio_1_2025 source materials.

Not part of the main publishing pipeline. Used only by
``scripts/import_legacy_materials.py`` to convert legacy DOCX/PDF chapter
materials into the biol-1 module directory structure.
"""

from .main import (
    process_chapter_questions,
    process_slides,
    create_for_upload_files,
    process_for_upload_all_modules,
)

__all__: list[str] = [
    "process_chapter_questions",
    "process_slides",
    "create_for_upload_files",
    "process_for_upload_all_modules",
]
