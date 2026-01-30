# Document Types Reference

Complete reference for all document types in the CR-BIO course development system, their supported output formats, and generation commands.

---

## Quick Reference

### Input → Output Matrix

| Input Type | PDF | DOCX | HTML | TXT | MP3 | Website |
|------------|-----|------|------|-----|-----|---------|
| **Markdown (.md)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Plain Text (.txt)** | ✅ | - | ✅ | - | ✅ | - |
| **HTML (.html)** | ✅ | - | - | ✅ | - | - |
| **PDF (.pdf)** | - | - | - | ✅ | - | - |
| **Audio (.mp3/.wav/.m4a)** | - | - | - | ✅ | - | - |

### Generation Command (All Formats)

```bash
cd software
uv run python scripts/generate_all_outputs.py --course {biol-1|biol-8|all}
```

---

## Document Type Catalog

### 1. Module Content

#### keys-to-success.md

Learning objectives, key concepts, and study tips for each module.

| Property | Value |
|----------|-------|
| **Location** | `course/module-XX-*/keys-to-success.md` |
| **BIOL-1 Count** | 17 files |
| **BIOL-8 Count** | 15 files |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |
| **Output Location** | `module-XX/output/study-guides/` |

**Generation:**

```bash
uv run python scripts/generate_module_renderings.py --course biol-8 --module 1
```

```python
from src.batch_processing.main import process_module_by_type
process_module_by_type("course/module-01", "course/module-01/output")
```

---

#### questions.md

Comprehension and review questions for each module.

| Property | Value |
|----------|-------|
| **Location** | `course/module-XX-*/questions.md` |
| **BIOL-1 Count** | 17 files |
| **BIOL-8 Count** | 14 files |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |
| **Output Location** | `module-XX/output/study-guides/` |

**Generation:** Same as keys-to-success.md

---

### 2. Laboratory Protocols

#### lab-XX_topic.md

Structured lab protocols with interactive elements (fillable fields, data tables).

| Property | Value |
|----------|-------|
| **Location** | `course/labs/lab-XX_*.md` |
| **BIOL-1 Count** | 1 complete |
| **BIOL-8 Count** | 1 complete, 14 stubs |
| **Output Formats** | PDF (fillable), HTML (interactive) |
| **Output Location** | `course/labs/output/` |

**Lab Directives Supported:**

- `{fill:text}` - Single-line input
- `{fill:textarea rows=N}` - Multi-line text area
- `<!-- lab:data-table rows=N -->` - Fillable data table
- `<!-- lab:reflection prompt="Q" -->` - Reflection box
- `<!-- lab:object-selection -->` - Object selection field

**Generation:**

```python
from src.lab_manual.main import render_lab_manual, batch_render_lab_manuals

# Single lab
render_lab_manual("lab-01.md", "lab-01.pdf", output_format="pdf", course_name="BIOL-8")

# All labs
batch_render_lab_manuals("course/labs/", "course/labs/output/", "pdf", course_name="BIOL-8")
```

---

### 3. Assessments

#### exam-XX.md / exam-XX_key.md

Formal examinations covering multiple modules.

| Property | Value |
|----------|-------|
| **Location** | `course/exams/` |
| **BIOL-1 Count** | 0 (templates only) |
| **BIOL-8 Count** | 4 exams + 4 keys |
| **Format** | 50 MC (2pts) + 30 SA (5pts) + 20 Essay = 100 pts |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |

**Structure:**

```
exam-01.md        → Modules 01-07
exam-02.md        → Modules 08-11
exam-03.md        → Modules 12-15
final-exam.md     → Comprehensive (150 pts)
```

---

#### module-XX_quiz.md / module-XX_quiz_key.md

Per-module quizzes for formative assessment.

| Property | Value |
|----------|-------|
| **Location** | `course/quizzes/` |
| **BIOL-1 Count** | 0 (templates only) |
| **BIOL-8 Count** | 15 quizzes + 15 keys |
| **Format** | 7 MC (1pt) + 3 FR (1pt) = 10 pts |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |

---

### 4. Syllabus Materials

#### Syllabus.md

Course syllabus with policies, grading, and schedule.

| Property | Value |
|----------|-------|
| **Location** | `syllabus/BIOL-X_*.md` |
| **BIOL-1** | BIOL-1_Spring-2026_Syllabus.md |
| **BIOL-8** | BIOL-8_Spring-2026_Syllabus.md |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |
| **Output Location** | `syllabus/output/` |

**Generation:**

```bash
uv run python scripts/generate_syllabus_renderings.py --course biol-8
```

```python
from src.batch_processing.main import process_syllabus
process_syllabus("syllabus/", "syllabus/output/")
```

---

#### Schedule.md

Week-by-week course schedule with topics and dates.

| Property | Value |
|----------|-------|
| **Location** | `syllabus/Schedule.md` |
| **Both Courses** | 1 file each |
| **Output Formats** | PDF, DOCX, HTML, TXT, MP3 |
| **Output Location** | `syllabus/output/` |

**Generation:**

```python
from src.schedule.main import process_schedule
process_schedule("Schedule.md", "output/", formats=["pdf", "html", "mp3"])
```

---

### 5. Slide Resources

#### Module Slides (PDF)

Presentation slides in full and notes versions.

| Property | Value |
|----------|-------|
| **Location (BIOL-1)** | `resources/slides/module-XX-slides-*.pdf` |
| **Location (BIOL-8)** | `course/module-XX/resources/*.pdf` |
| **BIOL-1 Count** | 30 PDFs (15 modules × 2 versions; modules 9 and 17 missing) |
| **BIOL-8 Count** | 15 PDFs (1 per module) |
| **Versions** | `*-full.pdf` (complete), `*-notes.pdf` (with notes) |

**Note:** Slides are pre-generated PDFs, not dynamically rendered.

---

### 6. Interactive Website

#### Module Website (index.html)

Single-page interactive website per module with all content.

| Property | Value |
|----------|-------|
| **Output Location** | `module-XX/output/website/index.html` |
| **Both Courses** | Generated for all modules |
| **Features** | Dark mode, quizzes, audio, collapsible sections |

**Generation:**

```bash
uv run python scripts/generate_module_website.py --course biol-8 --module 1
```

```python
from src.html_website.main import generate_module_website
generate_module_website("course/module-01", output_dir="output/website", course_name="BIOL-8")
```

**Website Features:**

- Dark mode toggle (persists via localStorage)
- Back-to-top button
- Collapsible sections
- Interactive quizzes (MC, T/F, matching, free response)
- Embedded audio players
- Mobile responsive design
- Print-friendly layout
- Accessibility features (skip links, high contrast)

---

## Course Parity Matrix

| Document Type | BIOL-1 | BIOL-8 | Status |
|---------------|--------|--------|--------|
| **keys-to-success.md** | 17 | 15 | ✅ Complete |
| **questions.md** | 17 | 15 | ✅ Complete |
| **Labs (complete)** | 1 | 1 | ✅ Lab 01 only |
| **Labs (stubs)** | 16 | 14 | ✅ Both have stubs |
| **Exams** | Templates | 4 + keys | ❌ BIOL-1 needs content |
| **Quizzes** | Templates | 15 + keys | ❌ BIOL-1 needs content |
| **Syllabus** | 2 files | 2 files | ✅ Complete |
| **Schedule** | 1 file | 1 file | ✅ Complete |
| **Slides** | 30 PDFs (modules 9, 17 missing) | 15 PDFs | ⚠️ BIOL-1 missing 2 modules |
| **Module Resources** | Empty | 15 PDFs | ⚠️ BIOL-1 dirs empty |
| **Website Output** | All modules | All modules | ✅ Complete |

### Priority Actions

1. **CRITICAL:** Create BIOL-1 exams (5 exams + 5 keys)
2. **CRITICAL:** Create BIOL-1 quizzes (17 quizzes + 17 keys)
3. **HIGH:** Develop all lab stubs into complete protocols (30 total)
4. **MEDIUM:** Add BIOL-1 slides for modules 9 and 17
5. **LOW:** Populate BIOL-1 module resource directories

---

## Output Format Details

### PDF (.pdf)

- **Generator:** WeasyPrint
- **Use Case:** Print-ready documents, formal distribution
- **Dependencies:** cairo, pango, gdk-pixbuf, glib (system libraries)

### DOCX (.docx)

- **Generator:** python-docx
- **Use Case:** Editable documents for instructors
- **Dependencies:** python-docx package

### HTML (.html)

- **Generator:** markdown library + custom templates
- **Use Case:** Web viewing, LMS embedding
- **Dependencies:** markdown, markdown2 packages

### TXT (.txt)

- **Generator:** Direct text extraction
- **Use Case:** Accessibility, screen readers, plain text systems
- **Dependencies:** None

### MP3 (.mp3)

- **Generator:** gTTS (Google Text-to-Speech)
- **Use Case:** Audio learning, accessibility
- **Dependencies:** gtts package, internet connection

### Website

- **Generator:** html_website module
- **Use Case:** Self-contained interactive learning
- **Dependencies:** None (generates standalone HTML)

---

## Software Module Reference

| Module | Purpose | Primary Function |
|--------|---------|------------------|
| `markdown_to_pdf` | Markdown → PDF | `render_markdown_to_pdf()` |
| `text_to_speech` | Text → MP3 | `generate_speech()` |
| `speech_to_text` | Audio → TXT | `transcribe_audio()` |
| `format_conversion` | Multi-format | `convert_file()` |
| `batch_processing` | Bulk generation | `process_module_by_type()` |
| `html_website` | Interactive sites | `generate_module_website()` |
| `lab_manual` | Lab protocols | `render_lab_manual()` |
| `schedule` | Schedule processing | `process_schedule()` |
| `module_organization` | Structure creation | `create_module_structure()` |
| `file_validation` | Validation | `validate_module_files()` |
| `canvas_integration` | LMS upload | `upload_module_to_canvas()` |
| `publish` | Export finalized | `publish_course()` |

---

## Directory Structure

```
course_development/
├── biol-1/
│   ├── course/
│   │   ├── module-01-study-of-life/
│   │   │   ├── keys-to-success.md       # Source
│   │   │   ├── questions.md             # Source
│   │   │   ├── resources/               # Supplementary materials
│   │   │   └── output/
│   │   │       ├── study-guides/        # PDF, DOCX, HTML, TXT, MP3
│   │   │       └── website/             # index.html
│   │   ├── labs/
│   │   │   ├── lab-01_measurement-methods.md
│   │   │   └── output/                  # PDF, HTML
│   │   ├── exams/                       # Templates only
│   │   └── quizzes/                     # Templates only
│   ├── syllabus/
│   │   ├── BIOL-1_Spring-2026_Syllabus.md
│   │   ├── Schedule.md
│   │   └── output/                      # PDF, DOCX, HTML, TXT, MP3
│   ├── resources/
│   │   └── slides/                      # 30 PDFs
│   └── private/                         # Facility-specific
│
├── biol-8/
│   ├── course/
│   │   ├── module-01-exploring-life-science/
│   │   │   ├── keys-to-success.md
│   │   │   ├── questions.md
│   │   │   ├── resources/               # Module PDF
│   │   │   └── output/
│   │   │       ├── study-guides/
│   │   │       └── website/
│   │   ├── labs/
│   │   │   ├── lab-01_measurement-methods.md  # Complete
│   │   │   ├── lab-02_chemistry-of-life.md    # Stub
│   │   │   └── ... (14 more stubs)
│   │   ├── exams/
│   │   │   ├── exam-01.md + exam-01_key.md
│   │   │   ├── exam-02.md + exam-02_key.md
│   │   │   ├── exam-03.md + exam-03_key.md
│   │   │   └── final-exam.md + final-exam_key.md
│   │   └── quizzes/
│   │       ├── module-01_quiz.md + module-01_quiz_key.md
│   │       └── ... (15 modules)
│   ├── syllabus/
│   ├── resources/
│   │   └── ConceptsofBiology-WEB.pdf    # Textbook
│   └── private/
```

---

## Quick Commands

```bash
# Generate everything for both courses
uv run python scripts/generate_all_outputs.py

# Generate specific course
uv run python scripts/generate_all_outputs.py --course biol-8

# Generate specific module
uv run python scripts/generate_all_outputs.py --course biol-8 --module 3

# Generate only specific formats (no system deps needed)
uv run python scripts/generate_all_outputs.py --formats mp3,txt

# Dry run (preview without generating)
uv run python scripts/generate_all_outputs.py --dry-run

# Validate file structure
uv run python -m src.file_validation.main --course biol-8

# Run tests
uv run pytest tests/ -v
```

---

*Last Updated: 2026-01-28*
