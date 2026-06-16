# BIOL-1 Syllabus Technical Documentation

## Overview

Technical documentation for syllabus file processing and format generation.

## Directory Structure

```
syllabus/
├── README.md                        # Syllabus overview
├── AGENTS.md                        # This file
├── BIOL-1_Fall-2026_Syllabus.md   # Main syllabus (source)
├── Schedule.md                      # Term schedule (source)
└── output/                          # Processed outputs (do not add new *source* .md here)
    ├── BIOL-1_Fall-2026_Syllabus.{pdf,docx,md}
    └── Schedule.{pdf,docx,md}
```

`generate_syllabus_renderings.py` processes **only** top-level `*.md` in this directory that are not under `output/`. The batch layer should not treat `output/*.md` copies as second sources.

## File Processing

### Processing Function

**Module**: `software/src/batch_processing/main.py`

**Function**: `process_syllabus(syllabus_path: str, output_dir: str) -> Dict[str, Any]`

Processes all markdown files in the syllabus directory and generates the requested output formats.

### Processing Pipeline

For each markdown file in the syllabus directory, the default publish profile
generates PDF, DOCX, and MD outputs. HTML, TXT, and MP3 are supported opt-in
formats requested through `publish.toml` or `python publish.py --override-formats`.

### Output Structure

```
output/
├── [filename].pdf
├── [filename].docx
└── [filename].md
```

All output files are organized flat in the `output/` directory, matching the structure used for module assignments.

## File Naming

### Source Files

- Markdown files in syllabus directory are processed
- Primary syllabus file: `BIOL-1_Fall-2026_Syllabus.md`
- Additional syllabus-related files can be added as needed

### Output Files

- **Base Name**: Derived from source markdown filename (without extension)
- **Extensions**: `.pdf`, `.docx`, `.md` by default; `.html`, `.txt`, and `.mp3` when requested
- **Location**: Flat in `output/` directory (same structure as module assignments)

## Processing Script

**Script**: `software/scripts/generate_syllabus_renderings.py`

**Usage**: Processes all markdown files in the syllabus directory

**Output**: Requested format renderings organized by format type

## Dependencies

### Software Modules

- **batch_processing**: Main orchestration module
- **markdown_to_pdf**: PDF generation from markdown
- **text_to_speech**: Opt-in audio generation from text
- **format_conversion**: Format conversions (DOCX, MD, HTML, TXT)

### Utility Functions

- `find_markdown_files()`: Recursively find markdown files
- `should_process_file()`: Filter files to process
- `ensure_output_directory()`: Create output directories
- `extract_text_from_markdown()`: Extract plain text from markdown
- `read_text_file()`: Read file content

## Error Handling

- Individual file processing errors are caught and logged
- Errors are collected in results dictionary
- Processing continues for remaining files after errors

## Integration Points

### Canvas Upload

- Syllabus files can be uploaded to Canvas
- Multiple formats provide accessibility options
- PDF format recommended for primary Canvas posting

### Course Materials

- Syllabus is processed separately from module materials
- Uses same processing pipeline as module materials
- Outputs organized by format type (not curriculum type)
