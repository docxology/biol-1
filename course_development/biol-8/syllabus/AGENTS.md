# BIOL-8 Syllabus Technical Documentation

## Overview

Technical documentation for syllabus file processing and format generation.

## Directory Structure

```
syllabus/
├── README.md                        # Syllabus overview
├── AGENTS.md                        # This file
├── BIOL-8_Spring-2026_Syllabus.md  # Main syllabus markdown file
└── output/                          # Processed output files (flat organization)
    ├── BIOL-8_Spring-2026_Syllabus.pdf
    ├── BIOL-8_Spring-2026_Syllabus.mp3
    ├── BIOL-8_Spring-2026_Syllabus.docx
    ├── BIOL-8_Spring-2026_Syllabus.html
    └── BIOL-8_Spring-2026_Syllabus.txt
```

## File Processing

### Processing Function

**Module**: `software/src/batch_processing/main.py`

**Function**: `process_syllabus(syllabus_path: str, output_dir: str) -> Dict[str, Any]`

Processes all markdown files in the syllabus directory and generates multiple output formats.

### Processing Pipeline

For each markdown file in the syllabus directory:

       1. **PDF Generation**
          - Function: `markdown_to_pdf.main.render_markdown_to_pdf()`
          - Input: Markdown file path
          - Output: PDF file in `output/` directory

       2. **MP3 Audio Generation**
          - Function: `text_to_speech.main.generate_speech()`
          - Process: Extract text from markdown → Generate speech
          - Utilities: `text_to_speech.utils.extract_text_from_markdown()`, `read_text_file()`
          - Output: MP3 file in `output/` directory

       3. **DOCX Generation**
          - Function: `format_conversion.main.convert_file()`
          - Conversion: `md->docx`
          - Output: DOCX file in `output/` directory

       4. **HTML Generation**
          - Function: `format_conversion.main.convert_file()`
          - Conversion: `md->html`
          - Output: HTML file in `output/` directory

       5. **TXT Generation**
          - Process: Extract text from markdown → Write plain text
          - Utilities: `text_to_speech.utils.extract_text_from_markdown()`, `read_text_file()`
          - Output: TXT file in `output/` directory

### Output Structure

```
output/
├── [filename].pdf
├── [filename].mp3
├── [filename].docx
├── [filename].html
└── [filename].txt
```

All output files are organized flat in the `output/` directory, matching the structure used for module assignments.

## File Naming

### Source Files

- Markdown files in syllabus directory are processed
- Primary syllabus file: `BIOL-8_Spring-2026_Syllabus.md`
- Additional syllabus-related files can be added as needed

### Output Files

- **Base Name**: Derived from source markdown filename (without extension)
- **Extensions**: `.pdf`, `.mp3`, `.docx`, `.html`, `.txt`
- **Location**: Flat in `output/` directory (same structure as module assignments)

## Processing Script

**Script**: `software/scripts/generate_syllabus_renderings.py`

**Usage**: Processes all markdown files in the syllabus directory

**Output**: All format renderings organized by format type

## Dependencies

### Software Modules

- **batch_processing**: Main orchestration module
- **markdown_to_pdf**: PDF generation from markdown
- **text_to_speech**: Audio generation from text
- **format_conversion**: Format conversions (DOCX, HTML)

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
