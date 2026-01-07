# Generation Scripts

## Overview

Scripts for generating all course material outputs including PDF, MP3, DOCX, HTML, TXT formats and HTML websites.

## Available Scripts

### `generate_all_outputs.py`

Comprehensive script to generate all outputs for all modules and courses.

**Usage**:
```bash
cd software
uv run python scripts/generate_all_outputs.py
```

**What it does**:
- Clears all existing output directories before regeneration
- Processes all modules for both BIOL-1 and BIOL-8
- Generates all format outputs (PDF, MP3, DOCX, HTML, TXT)
- Generates HTML websites for each module
- Processes syllabi for both courses
- Provides comprehensive summary of all processing with timing information

**Logging**:
- Logs to both console (INFO level) and file (DEBUG level)
- Log files are stored in `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log`
- Console shows progress and summary information
- File contains detailed debugging information including stack traces
- All operations are timestamped and logged with appropriate severity levels
- Logs include timing information for performance monitoring

**Output**:
- Module outputs in `[course]/course/module-[N]/output/`
- Module websites in `[course]/course/module-[N]/output/website/`
- Syllabus outputs in `[course]/syllabus/output/`

### `generate_module_renderings.py`

Generate all renderings for a specific module.

**Usage**:
```bash
cd software
uv run python scripts/generate_module_renderings.py
```

**Configuration**: Currently configured for `biol-1/course/module-1`

**Output**: All format renderings organized by curriculum element type

### `generate_module_website.py`

Generate HTML website for a specific module.

**Usage**:
```bash
cd software
uv run python scripts/generate_module_website.py
```

**Configuration**: Currently configured for `biol-1/course/module-1`

**Output**: Single HTML file with all module content, audio, and interactive quizzes

### `generate_syllabus_renderings.py`

Generate all renderings for syllabus files.

**Usage**:
```bash
cd software
uv run python scripts/generate_syllabus_renderings.py
```

**Configuration**: Currently configured for `biol-1/syllabus`

**Output**: All format renderings organized by format type

## Known Limitations

### System Dependencies

Some output formats require system libraries that may not be available:

- **PDF Generation**: Requires WeasyPrint system libraries (libgobject, etc.)
  - MP3 and TXT formats work without these dependencies
  - PDF/DOCX/HTML may fail if system libraries are not installed

- **HTML Generation**: May fail if format conversion dependencies are missing

### Workarounds

- MP3 and TXT generation work reliably on all systems
- PDF/DOCX/HTML generation requires proper system library installation
- See WeasyPrint documentation for installation instructions

## Testing

All scripts include error handling and will continue processing even if individual files fail. Check the error output for specific issues.

## Output Verification

After running scripts, verify outputs:

1. Check `output/` directories for generated files
2. Review error messages for any failed generations
3. Test HTML websites in a browser
4. Verify audio files play correctly
