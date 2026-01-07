# Course Material Generation Guide

## Overview

This guide explains how to generate all course material outputs including PDF, MP3, DOCX, HTML, TXT formats and HTML websites for both BIOL-1 and BIOL-8 courses.

## Quick Start

To generate all outputs for all courses:

```bash
cd software
uv run python scripts/generate_all_outputs.py
```

This will:
- Process all modules (1-3) for both BIOL-1 and BIOL-8
- Generate all format outputs (PDF, MP3, DOCX, HTML, TXT)
- Generate HTML websites for each module
- Process syllabi for both courses

## Generation Methods

### Module Processing

Each module is processed to generate multiple output formats:

1. **PDF**: Printable document format (requires WeasyPrint system libraries)
2. **MP3**: Audio format for listening (works on all systems)
3. **DOCX**: Microsoft Word format (requires WeasyPrint system libraries)
4. **HTML**: Web format (requires format conversion libraries)
5. **TXT**: Plain text format (works on all systems)

### Website Generation

HTML websites are generated for each module containing:
- All module content (lecture, lab, study guide, assignments)
- Embedded audio players
- Interactive quizzes extracted from study guides
- Simple grayscale design

### Syllabus Processing

Syllabi are processed to all export formats, organized by format type rather than curriculum type.

## Output Locations

### Module Outputs

```
[course]/course/module-[N]/output/
├── assignments/        # Processed assignment files
├── lab-protocols/      # Processed lab protocol files
├── lecture-content/    # Processed lecture files
├── study-guides/       # Processed study guide files
└── website/           # HTML website (index.html)
```

### Syllabus Outputs

```
[course]/syllabus/output/
├── pdf/
├── mp3/
├── docx/
├── html/
└── txt/
```

## Scripts

### `generate_all_outputs.py`

Comprehensive script that processes everything:

```bash
cd software
uv run python scripts/generate_all_outputs.py
```

**Features**:
- Processes all modules for both courses
- Generates all format outputs
- Generates HTML websites
- Processes syllabi
- Provides comprehensive summary

### Individual Scripts

For processing specific components:

- `generate_module_renderings.py` - Process a specific module
- `generate_module_website.py` - Generate HTML website for a module
- `generate_syllabus_renderings.py` - Process syllabus files

See [`software/scripts/README.md`](software/scripts/README.md) for details.

## Known Limitations

### System Dependencies

Some output formats require system libraries:

- **PDF/DOCX/HTML**: Require WeasyPrint system libraries (libgobject, etc.)
  - These may not be available on all systems
  - MP3 and TXT generation work without these dependencies

### Workarounds

- MP3 and TXT formats work reliably on all systems
- PDF/DOCX/HTML may fail if system libraries are not installed
- See WeasyPrint documentation for installation instructions

## Verification

After running generation scripts:

1. **Check Output Directories**: Verify files were generated in `output/` directories
2. **Review Errors**: Check error messages for any failed generations
3. **Test Websites**: Open HTML websites in a browser to verify functionality
4. **Test Audio**: Verify MP3 files play correctly

## Testing

All generation methods are tested and documented:

- Module processing: `process_module_by_type()`
- Website generation: `process_module_website()`
- Syllabus processing: `process_syllabus()`

See [`software/src/batch_processing/AGENTS.md`](software/src/batch_processing/AGENTS.md) for technical documentation.

## Documentation

- **Scripts**: [`software/scripts/README.md`](software/scripts/README.md)
- **Batch Processing**: [`software/src/batch_processing/AGENTS.md`](software/src/batch_processing/AGENTS.md)
- **HTML Website**: [`software/src/html_website/AGENTS.md`](software/src/html_website/AGENTS.md)
- **Course Materials**: Course-specific documentation in each course's `course/AGENTS.md`
