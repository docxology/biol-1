# Generation Scripts

## Overview

Scripts for generating all course material outputs including PDF, MP3, DOCX, HTML, TXT formats and HTML websites.

## Available Scripts

### `generate_all_outputs.py`

Comprehensive script to generate all outputs for all modules and courses.

**Usage**:

```bash
cd software
uv run python scripts/generate_all_outputs.py [OPTIONS]
```

**Options**:

| Option | Description |
|--------|-------------|
| `--course {biol-1,biol-8,all}` | Course to process (default: all) |
| `--module MODULE` | Specific module number to process |
| `--formats FORMATS` | Comma-separated formats: pdf,mp3,docx,html,txt (default: all) |
| `--dry-run` | Show what would be generated without generating |
| `--skip-clear` | Skip clearing existing outputs before generation |
| `--no-website` | Skip website generation |

**Examples**:

```bash
# Generate all outputs for all courses
uv run python scripts/generate_all_outputs.py

# Generate only for BIOL-1
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate only module 2 for BIOL-8
uv run python scripts/generate_all_outputs.py --course biol-8 --module 2

# Generate only MP3 and TXT formats (works without system dependencies)
uv run python scripts/generate_all_outputs.py --formats mp3,txt

# Preview what would be generated
uv run python scripts/generate_all_outputs.py --dry-run
```

**What it does**:

- Clears all existing output directories before regeneration (unless `--skip-clear`)
- Processes modules for selected courses
- Generates all format outputs (PDF, MP3, DOCX, HTML, TXT) or selected formats
- Generates HTML websites for each module (unless `--no-website`)
- Processes syllabi for selected courses
- Provides comprehensive summary with timing information

**Module Naming Convention Support**:

Scripts automatically handle both module naming patterns:
- BIOL-1 style: `module-1`, `module-2`, `module-10`
- BIOL-8 style: `module-01-topic-name`, `module-02-chemistry-of-life`

When using `--module N`, the scripts find the correct directory regardless of naming convention.

**Output**:

- Module outputs in `[course]/course/module-[N]/output/`
- Module websites in `[course]/course/module-[N]/output/website/`
- Syllabus outputs in `[course]/syllabus/output/`

### `generate_module_renderings.py`

Generate all renderings for a specific module.

**Usage**:

```bash
cd software
uv run python scripts/generate_module_renderings.py [OPTIONS]
```

**Options**:

| Option | Description |
|--------|-------------|
| `--course {biol-1,biol-8}` | Course to process (default: biol-1) |
| `--module MODULE` | Module number to process (default: 1) |

**Examples**:

```bash
# Generate for biol-1/module-1 (default)
uv run python scripts/generate_module_renderings.py

# Generate for biol-8/module-3
uv run python scripts/generate_module_renderings.py --course biol-8 --module 3
```

**Output**: All format renderings organized by curriculum element type

### `generate_module_website.py`

Generate HTML website for a specific module.

**Usage**:

```bash
cd software
uv run python scripts/generate_module_website.py [OPTIONS]
```

**Options**:

| Option | Description |
|--------|-------------|
| `--course {biol-1,biol-8}` | Course to process (default: biol-1) |
| `--module MODULE` | Module number to process (default: 1) |

**Examples**:

```bash
# Generate website for biol-1/module-1 (default)
uv run python scripts/generate_module_website.py

# Generate website for biol-8/module-2
uv run python scripts/generate_module_website.py --course biol-8 --module 2
```

**Output**: Single HTML file with all module content, audio, and interactive quizzes

**Website Features**:

- 🌙 **Dark Mode Toggle** - Persists via localStorage
- ⬆️ **Back to Top Button** - Appears when scrolling
- 📱 **Mobile Responsive** - Works on phones and tablets
- 🖨️ **Print Friendly** - Clean output for Cmd+P
- ♿ **Accessibility** - Skip link, high contrast mode
- 📝 **Interactive Quizzes** - Multiple choice, true/false, matching, free response

### `generate_syllabus_renderings.py`

Generate all renderings for syllabus files.

**Usage**:

```bash
cd software
uv run python scripts/generate_syllabus_renderings.py [OPTIONS]
```

**Options**:

| Option | Description |
|--------|-------------|
| `--course {biol-1,biol-8}` | Course to process (default: biol-1) |

**Examples**:

```bash
# Generate syllabus for biol-1 (default)
uv run python scripts/generate_syllabus_renderings.py

# Generate syllabus for biol-8
uv run python scripts/generate_syllabus_renderings.py --course biol-8
```

**Output**: All format renderings organized by format type

### Lab Manual Generation

Generate interactive lab manuals with fillable fields from Markdown source files.

**Location**: Labs are stored in standalone `labs/` directories:

- BIOL-1: `course_development/biol-1/course/labs/`
- BIOL-8: `course_development/biol-8/course/labs/`

**Usage** (Python API):

```python
cd software
uv run python -c "
from src.lab_manual.main import render_lab_manual, batch_render_lab_manuals

# Generate single lab (PDF)
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-8: Human Biology'
)

# Generate single lab (HTML with interactivity)
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.html',
    'html',
    course_name='BIOL-8: Human Biology'
)

# Batch process all labs in directory
batch_render_lab_manuals(
    '../course_development/biol-8/course/labs',
    '../course_development/biol-8/course/labs/output',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"
```

**Lab Directive Syntax**:

Labs support special directives for interactive elements:

| Directive | Purpose |
|-----------|---------|
| `<!-- lab:data-table rows=N columns="A,B,C" -->` | Fillable data table |
| `<!-- lab:object-selection fields="Field1,Field2" -->` | Object selection form |
| `<!-- lab:measurement-feasibility options="a,b,c" -->` | Feasibility checklist |
| `<!-- lab:reflection prompt="Question here" rows=N -->` | Reflection text box |
| `{fill:text}` | Inline fillable text field |
| `{fill:textarea rows=N}` | Multi-line text area |
| `{fill:checkbox}` | Checkbox input |

**Output Formats**:

- **PDF**: Print-ready with fillable fields as lines/boxes
- **HTML**: Interactive with input fields, localStorage save/restore

**Theme**: Black/white/gray with tasteful red accents (`#c41e3a`)

### `import_legacy_materials.py`

Import legacy materials from `bio_1_2025` directory to the structured course format.

**Usage**:

```bash
cd software
uv run python scripts/import_legacy_materials.py [OPTIONS]
```

**Options**:

| Option | Description |
|--------|-------------|
| `--course {biol-1,biol-8}` | Course to process (default: biol-1) |
| `--dry-run` | Show what would be imported without importing |
| `--skip-questions` | Skip importing chapter questions |
| `--skip-slides` | Skip importing slides |

**Examples**:

```bash
# Import all materials for biol-1 (default)
uv run python scripts/import_legacy_materials.py

# Dry run to preview what would be imported
uv run python scripts/import_legacy_materials.py --dry-run

# Import only slides, skip questions
uv run python scripts/import_legacy_materials.py --skip-questions

# Import only chapter questions, skip slides
uv run python scripts/import_legacy_materials.py --skip-slides
```

**What it does**:

- Converts Chapter Questions DOCX files to Markdown format
- Maps chapters to modules based on course schedule
- Saves chapter questions as assignment files in module `assignments/` directories
- Copies PDF slides (full and notes versions) to `resources/slides/` directory
- Organizes files with consistent naming conventions

**Chapter to Module Mapping**:

- Modules 1-8: Map to Chapters 1-8 (one-to-one)
- Module 9: Flexible Week (skipped - no chapter questions)
- Modules 10-14: Map to Chapters 9-13 (one-to-one)
- Module 15: Maps to Chapter 14
- Module 16: Maps to Chapters 16-17 (combined)

**Output**:

- Chapter questions: `[course]/course/module-[N]/assignments/module-[N]-chapter-questions.md`
- Full slides: `[course]/resources/slides/module-[N]-slides-full.pdf`
- Notes slides: `[course]/resources/slides/module-[N]-slides-notes.pdf`

**Source Files**:

- Chapter Questions: `bio_1_2025/files/Chapter Questions/Chapter [NN] Keys to Success.docx`
- Full Slides: `bio_1_2025/files/Slides/Slides_Full/General Biology Chapter [NN] Slides.pdf`
- Notes Slides: `bio_1_2025/files/Slides/Slides_Notes/Chapter [NN] - 3 Note.pdf`

## Logging

All scripts provide comprehensive logging:

- Console: INFO level (progress and summaries)
- File: DEBUG level (detailed information and stack traces)
- Log files: `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log`
- All operations are timestamped with timing information

## Known Limitations

### System Dependencies

Some output formats require system libraries:

- **PDF/DOCX/HTML Generation**: Requires WeasyPrint system libraries

  ```bash
  # macOS
  brew install cairo pango gdk-pixbuf glib
  export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
  ```

- **MP3/TXT Generation**: Works without system dependencies

### Workarounds

If system libraries are not available:

```bash
# Generate only formats that work without dependencies
uv run python scripts/generate_all_outputs.py --formats mp3,txt
```

## Testing

All scripts include error handling and will continue processing even if individual files fail. Check the error output for specific issues.

## Output Verification

After running scripts, verify outputs:

1. Check `output/` directories for generated files
2. Review error messages for any failed generations
3. Test HTML websites in a browser
4. Verify audio files play correctly
5. Test interactive quizzes (multiple choice, true/false, matching, free response)
