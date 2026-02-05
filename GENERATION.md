# Course Material Generation Guide

## Overview

This guide explains how to generate all course material outputs including PDF, MP3, DOCX, HTML, TXT formats and HTML websites for both BIOL-1 and BIOL-8 courses.

## Quick Start

To generate all outputs for all courses:

```bash
cd software
uv run python scripts/generate_all_outputs.py
```

For a specific course or module:

```bash
# BIOL-1 only
uv run python scripts/generate_all_outputs.py --course biol-1

# Specific module
uv run python scripts/generate_all_outputs.py --course biol-8 --module 2

# Preview what would be generated
uv run python scripts/generate_all_outputs.py --dry-run
```

### Recommended: Top-Level Publish Command

For the full publish pipeline with configuration:

```bash
# From repository root (not software/)
cd /path/to/cr-bio
python publish.py                        # Full pipeline
python publish.py --dry-run               # Preview
python publish.py --override-formats pdf  # Override formats
```

See `publish.toml` for configuration options.

### Selective Generation: Module and Lab Limits

You can limit generation to specific ranges of modules and labs using `publish.toml`:

```toml
[publish.courses.biol-8]
enabled = true
modules = 15
max_module = 6      # Only generate modules 1-6
max_lab = 5         # Only generate labs 1-5
```

Or via command-line:

```bash
# In software/ directory
uv run python scripts/generate_all_outputs.py --max-module biol-8:6 --max-lab biol-8:5
```

This is useful for:

- Faster iteration during development (generate only what's needed)
- Progressive course rollout (release content incrementally)
- Testing specific module ranges

This will:

- Process all modules for both courses in `course_development/`
- Generate all format outputs (PDF, MP3, DOCX, HTML, TXT)
- Generate HTML websites for each module
- Process syllabi
- Clear outputs in `PUBLISHED/`? No, outputs are generated in place first, then published.
- Actually, the scripts generate to `course_development/.../output`, then `publish_course.py` moves them.
  - Wait, `generate_all_outputs.py` clears outputs in `course_development`? Yes, `clear_all_outputs(repo_root)`.

**Note**: To push changes to the public folder, run:

```bash
uv run python software/scripts/publish_course.py --course all
```

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
- Interactive quizzes (multiple choice, true/false, matching, free response)
- Progress tracking for completed questions

**Website Features**:

- 🗂️ **Sidebar Navigation** - Collapsible sidebar with quick links to all sections
- ↔️ **Resizable Split-View** - Draggable handle to adjust sidebar/content width
- 🌙 **Dark Mode** - Toggle persists via localStorage
- ⬆️ **Back to Top** - Button appears when scrolling
- 📱 **Mobile Responsive** - Works on phones and tablets (with toggleable menu)
- 🖨️ **Print Friendly** - Clean output for printing
- ♿ **Accessibility** - Skip navigation, high contrast mode

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
├── BIOL-X_Spring-2026_Syllabus.pdf
├── BIOL-X_Spring-2026_Syllabus.docx
├── BIOL-X_Spring-2026_Syllabus.html
├── BIOL-X_Spring-2026_Syllabus.txt
├── Schedule.pdf
├── Schedule.docx
├── Schedule.html
└── Schedule.txt
```

**Note:** Syllabus outputs use a flat structure (files directly in output/, not subdirectories).

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

## Lab Manual Generation

Labs are processed separately using the `lab_manual` module, which supports interactive elements and fillable fields.

### Location

Labs are stored in standalone `labs/` directories for each course:

- `course_development/biol-1/course/labs/`
- `course_development/biol-8/course/labs/`

### Generation Commands

```bash
cd software

# Generate single lab (PDF)
uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"

# Generate single lab (HTML with interactive fields)
uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.html',
    'html',
    course_name='BIOL-8: Human Biology'
)
"

# Batch render all labs in a directory
uv run python -c "
from src.lab_manual.main import batch_render_lab_manuals
batch_render_lab_manuals(
    '../course_development/biol-8/course/labs',
    '../course_development/biol-8/course/labs/output',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"
```

### Lab Directive Syntax

Labs use special markdown directives for interactive elements:

| Directive | Purpose |
|-----------|---------|
| `<!-- lab:data-table rows=N -->` | Fillable data tables |
| `<!-- lab:object-selection -->` | Object selection fields |
| `<!-- lab:measurement-feasibility -->` | Feasibility analysis sections |
| `<!-- lab:reflection -->` | Reflection/response boxes |
| `{fill:text}` | Inline text input |
| `{fill:textarea rows=N}` | Multi-line text area |

See [`software/src/lab_manual/README.md`](software/src/lab_manual/README.md) for complete documentation.

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
