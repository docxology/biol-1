# BIOL-8 Course Materials Technical Documentation

## Overview

Technical documentation for course-level file processing, organization, and workflow management for BIOL-8 course materials.

## Directory Structure

```
course/
├── README.md              # Course materials overview
├── AGENTS.md              # This file
├── BIOL-8_Spring-2026_Syllabus.md  # Syllabus file (to be moved to syllabus/)
└── module-*/              # Individual course modules
    ├── assignments/      # Assignment files
    ├── output/           # Processed output files
    │   ├── assignments/
    │   ├── lab-protocols/
    │   ├── lecture-content/
    │   ├── study-guides/
    │   └── website/
    ├── sample_*.md       # Sample curriculum element files
    ├── README.md         # Module overview
    └── AGENTS.md         # Module technical documentation
```

## File Processing Workflow

### Processing Function

**Module**: `software/src/batch_processing/main.py`

**Function**: `process_module_by_type(module_path: str, output_dir: str) -> Dict[str, Any]`

Processes all markdown files in a module directory and generates multiple output formats, organizing outputs by curriculum element type.

### Curriculum Element Type Detection

Files are classified by filename patterns:

- **Assignments**: Filenames containing `"assignment"` → `assignments/` output directory
- **Lab Protocols**: Filenames containing `"lab-protocol"` → `lab-protocols/` output directory
- **Lecture Content**: Filenames containing `"lecture-content"` → `lecture-content/` output directory
- **Study Guides**: Filenames containing `"study-guide"` → `study-guides/` output directory

### Processing Pipeline

For each markdown file matching curriculum element types:

1. **PDF Generation**
   - Function: `markdown_to_pdf.main.render_markdown_to_pdf()`
   - Input: Markdown file path
   - Output: PDF file in type-specific output directory

2. **MP3 Audio Generation**
   - Function: `text_to_speech.main.generate_speech()`
   - Process: Extract text from markdown → Generate speech
   - Utilities: `text_to_speech.utils.extract_text_from_markdown()`, `read_text_file()`
   - Output: MP3 file in type-specific output directory

3. **DOCX Generation**
   - Function: `format_conversion.main.convert_file()`
   - Conversion: `md->docx`
   - Output: DOCX file in type-specific output directory

4. **HTML Generation**
   - Function: `format_conversion.main.convert_file()`
   - Conversion: `md->html`
   - Output: HTML file in type-specific output directory

5. **TXT Generation**
   - Process: Extract text from markdown → Write plain text
   - Utilities: `text_to_speech.utils.extract_text_from_markdown()`, `read_text_file()`
   - Output: TXT file in type-specific output directory

6. **Website Generation**
   - Function: `html_website.main.generate_module_website()`
   - Process: Combines all module content into single HTML website
   - Output: `output/website/index.html`

### Output Structure

```
module-X/output/
├── assignments/
│   ├── [basename].pdf
│   ├── [basename].mp3
│   ├── [basename].docx
│   ├── [basename].html
│   └── [basename].txt
├── lab-protocols/
│   └── [same structure]
├── lecture-content/
│   └── [same structure]
├── study-guides/
│   └── [same structure]
└── website/
    └── index.html
```

## File Naming Conventions

### Source Files

- **Pattern Matching**: Files starting with `sample_` are processed
- **Type Detection**: Filename must contain type identifier (assignment, lab-protocol, lecture-content, study-guide)
- **Assignments**: Located in `assignments/` subdirectory, follow pattern `module-[N]-assignment-[number]-[description].md`

### Output Files

- **Base Name**: Derived from source markdown filename (without extension)
- **Extensions**: `.pdf`, `.mp3`, `.docx`, `.html`, `.txt`
- **Location**: Type-specific subdirectory within `output/`

## Processing Scripts

### Module Processing

**Script**: `software/scripts/generate_module_renderings.py`

**Usage**: Processes a specific module (currently configured for module-1)

**Output**: All format renderings organized by curriculum element type

### Website Generation

**Script**: `software/scripts/generate_module_website.py`

**Usage**: Generates HTML website for a module

**Output**: Single HTML file with all module content, audio, and interactive quizzes

## Error Handling

The processing function collects errors without stopping:

- Individual file processing errors are caught and logged
- Errors are collected in `results["errors"]` list
- Processing continues for remaining files after errors
- Summary includes error count and details

## Dependencies

### Software Modules

- **batch_processing**: Main orchestration module
- **markdown_to_pdf**: PDF generation from markdown
- **text_to_speech**: Audio generation from text
- **format_conversion**: Format conversions (DOCX, HTML)
- **html_website**: HTML website generation

### Utility Functions

- `find_markdown_files()`: Recursively find markdown files
- `should_process_file()`: Filter files to process
- `ensure_output_directory()`: Create output directories
- `extract_text_from_markdown()`: Extract plain text from markdown
- `read_text_file()`: Read file content

## Integration Points

### Canvas Upload

- All materials in `course/` directory are suitable for Canvas
- Output formats provide multiple access methods for students
- Directory structure mirrors Canvas organization

### Module Organization

- Modules follow consistent structure
- Each module has `assignments/`, `output/`, and sample files
- Documentation at module level describes module-specific details

## Validation

### Pre-Processing Checks

- Verify module directory exists
- Check for markdown files matching patterns
- Ensure output directory can be created

### Post-Processing Verification

- Check that all expected output formats were generated
- Verify files are organized in correct type directories
- Review error logs for processing issues

## Workflow Management

### Adding New Modules

1. Create module directory: `course/module-[N]/`
2. Initialize with standard structure (assignments/, sample files)
3. Add README.md and AGENTS.md
4. Process module using batch processing script
5. Generate website using website generation script
6. Verify outputs in `output/` directory

### Updating Materials

1. Edit source markdown files
2. Re-run processing script to regenerate outputs
3. Regenerate website if needed
4. Verify updated outputs
5. Update Canvas if materials already uploaded

### Processing New Files

1. Add markdown file following naming conventions
2. Ensure filename contains type identifier
3. Run processing script
4. Verify outputs in appropriate type directory
