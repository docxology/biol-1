# Software Documentation

> **Quick Navigation**: [Quick Start](QUICKSTART.md) | [Architecture](ARCHITECTURE.md) | [Orchestration](ORCHESTRATION.md) | [Standards](AGENTS.md) | [Lab Format](LAB_FORMAT.md) | [Dashboard Format](DASHBOARD_FORMAT.md) | [Course Structure](COURSE_STRUCTURE.md) | [API Reference](../AGENTS.md)

## Overview

CR-BIO is an automated curriculum management system for Biology courses at College of the Redwoods. It transforms Markdown source files into multiple output formats (PDF, MP3, HTML, DOCX, TXT) and interactive websites for two courses:

- **BIOL-1**: General Biology (15 content modules) — Pelican Bay Prison
- **BIOL-8**: Human Anatomy & Physiology (17 modules) — College of the Redwoods

```mermaid
flowchart LR
    subgraph SOURCE["📝 Source (Private)"]
        CD[course_development/]
    end
    
    subgraph PROCESS["⚙️ Processing"]
        SW[software/]
        PUB[publish.py]
    end
    
    subgraph OUTPUT["📤 Output (Public)"]
        PUBD[PUBLISHED/]
    end
    
    CD --> SW
    SW --> PUB
    PUB --> PUBD
    
    style SOURCE fill:#fff9c4
    style PROCESS fill:#e8f5e9
    style OUTPUT fill:#c8e6c9
```

---

## Verify tests and coverage

Counts change as the suite grows. From `software/`:

```bash
uv run pytest --collect-only -q    # test count
uv run pytest -q --no-cov            # pass/fail
uv run pytest --cov=src --cov-report=term-missing   # coverage (terminal)
```

Structural facts (update if layout changes): **`software/src/`** holds **16** Python packages (see [`../src/AGENTS.md`](../src/AGENTS.md)).

### Supported courses

- **BIOL-1**: 15 modules under `course_development/biol-1/course/module-*`
- **BIOL-8**: 17 modules under `course_development/biol-8/course/module-*`

---

## Documentation Guide

### By Audience

| If you are a... | Start with... | Then explore... |
|-----------------|---------------|-----------------|
| **New User** | [QUICKSTART.md](QUICKSTART.md) | [ORCHESTRATION.md](ORCHESTRATION.md) |
| **Content Author** | [LAB_FORMAT.md](LAB_FORMAT.md) | [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md), [COURSE_STRUCTURE.md](COURSE_STRUCTURE.md) |
| **Developer** | [ARCHITECTURE.md](ARCHITECTURE.md) | [../AGENTS.md](../AGENTS.md) |
| **AI Assistant** | [../../CLAUDE.md](../../CLAUDE.md) | [AGENTS.md](AGENTS.md) |

### By Topic

| Topic | Document | Description |
|-------|----------|-------------|
| **Getting Started** | [QUICKSTART.md](QUICKSTART.md) | Installation, setup, quick commands |
| **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) | System design, module layers, document types |
| **Workflows** | [ORCHESTRATION.md](ORCHESTRATION.md) | Multi-module patterns, publish pipeline, lab generation |
| **Standards** | [AGENTS.md](AGENTS.md) | Documentation standards, output format reference |
| **Lab Authoring** | [LAB_FORMAT.md](LAB_FORMAT.md) | Lab protocol format, directives, templates |
| **Dashboard Authoring** | [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md) | Interactive dashboard architecture |
| **Course Structure** | [COURSE_STRUCTURE.md](COURSE_STRUCTURE.md) | Directory layout, content organization |
| **PDF Output** | [OUTPUT_PDF.md](OUTPUT_PDF.md) | PDF generation via WeasyPrint |
| **Audio Output** | [OUTPUT_AUDIO.md](OUTPUT_AUDIO.md) | MP3 generation via gTTS |
| **DOCX Output** | [OUTPUT_DOCX.md](OUTPUT_DOCX.md) | Word document generation |
| **HTML Output** | [OUTPUT_HTML.md](OUTPUT_HTML.md) | All HTML output types |
| **API Reference** | [../AGENTS.md](../AGENTS.md) | All function signatures |
| **Configuration** | [../../publish.toml](../../publish.toml) | Pipeline configuration options |
| **Contributing** | [../../CONTRIBUTING.md](../../CONTRIBUTING.md) | How to add labs, assessments, content |
| **Testing** | [../tests/README.md](../tests/README.md) | Test suite documentation |

---

## Documentation Index

### Getting Started

| Document | Description | Audience |
|----------|-------------|----------|
| **[QUICKSTART.md](QUICKSTART.md)** | Installation, setup, quick commands | New users |
| **[../README.md](../README.md)** | Project overview and setup | All users |

### Content Authoring

| Document | Description | Audience |
|----------|-------------|----------|
| **[LAB_FORMAT.md](LAB_FORMAT.md)** | Lab protocol format, directives, templates | Content Authors |
| **[DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md)** | Interactive dashboard architecture guide | Content Authors |
| **[COURSE_STRUCTURE.md](COURSE_STRUCTURE.md)** | Course directory layout reference | All users |

### Output Format Guides

| Document | Description | Audience |
|----------|-------------|----------|
| **[OUTPUT_PDF.md](OUTPUT_PDF.md)** | PDF generation via WeasyPrint | Developers, Authors |
| **[OUTPUT_AUDIO.md](OUTPUT_AUDIO.md)** | MP3 audio generation via gTTS | Developers, Authors |
| **[OUTPUT_DOCX.md](OUTPUT_DOCX.md)** | Word document generation | Developers, Authors |
| **[OUTPUT_HTML.md](OUTPUT_HTML.md)** | All HTML output types (4 variants) | Developers, Authors |

### Technical Reference

| Document | Description | Audience |
|----------|-------------|----------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design, module diagrams, document types | Developers |
| **[ORCHESTRATION.md](ORCHESTRATION.md)** | Multi-module workflows, publish pipeline | Developers |
| **[AGENTS.md](AGENTS.md)** | Documentation standards, output format reference | Contributors |
| **[../AGENTS.md](../AGENTS.md)** | API reference (all functions) | Developers |

### Source and Tests

| Document | Description | Audience |
|----------|-------------|----------|
| **[../src/README.md](../src/README.md)** | Source code overview | Developers |
| **[../src/AGENTS.md](../src/AGENTS.md)** | Module-level docs | Developers |
| **[../tests/README.md](../tests/README.md)** | Test suite overview | Contributors |
| **[../tests/AGENTS.md](../tests/AGENTS.md)** | Testing standards | Contributors |

---

## Modular Architecture

The software is built on a modular architecture where each module is:

- **Self-contained**: Contains all code, configuration, and logic needed for its purpose
- **Independently usable**: Can be imported and used without other modules
- **Clearly bounded**: Public API (`main.py`) vs internal implementation (`utils.py`)
- **Minimally dependent**: Only essential inter-module dependencies
- **Composable**: Modules can be combined in various workflows

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design principles and [ORCHESTRATION.md](ORCHESTRATION.md) for composition patterns.

## Module Reference

### Content Generation

| Module | Purpose | Key Function | Standalone | Dependencies |
|--------|---------|--------------|------------|--------------|
| [markdown_to_pdf](../src/markdown_to_pdf/) | Markdown → PDF via WeasyPrint | `render_markdown_to_pdf()` | Yes | WeasyPrint only |
| [text_to_speech](../src/text_to_speech/) | Text → MP3 via gTTS | `generate_speech()` | Yes | gTTS only |
| [speech_to_text](../src/speech_to_text/) | Audio → Text transcription | `transcribe_audio()` | Yes | SpeechRecognition only |
| [format_conversion](../src/format_conversion/) | Multi-format conversion | `convert_file()` | Yes | Core converters |
| [batch_processing](../src/batch_processing/) | Batch module processing | `process_module_by_type()` | Yes | Core/format modules |
| [html_website](../src/html_website/) | Interactive HTML websites | `generate_module_website()` | Yes | batch_processing, format_conversion |
| [schedule](../src/schedule/) | Schedule file processing | `process_schedule()` | Yes | Core/format modules |
| [lab_manual](../src/lab_manual/) | Rich lab manual rendering | `render_lab_manual()` | Yes | markdown, weasyprint |

### Course Management

| Module | Purpose | Key Function | Standalone | Dependencies |
|--------|---------|--------------|------------|--------------|
| [module_organization](../src/module_organization/) | Create module structures | `create_module_structure()` | Yes | None |
| [file_validation](../src/file_validation/) | Validate content | `validate_module_files()` | Yes | None |
| [validation](../src/validation/) | Validate published outputs | `validate_outputs()` | Yes | None |
| [canvas_integration](../src/canvas_integration/) | Upload to Canvas LMS | `upload_module_to_canvas()` | Yes | file_validation |
| [content_processing](../src/content_processing/) | Question renumbering | `renumber_questions_in_course()` | Yes | None |
| [legacy_import](../src/legacy_import/) | Import legacy formats | `import_legacy_course()` | Yes | None |
| [publish](../src/publish/) | Export to PUBLISHED/ | `publish_course()` | Yes | None |

---

## CLI Scripts

Scripts in `scripts/` are thin orchestrators that call src modules:

| Script | Purpose | Primary Module(s) |
|--------|---------|-------------------|
| `publish_all.py` | **Top-level pipeline** | `batch_processing`, `publish`, `validation` |
| `generate_all_outputs.py` | Generate all course outputs | `batch_processing` |
| `generate_module_renderings.py` | Single module processing | `batch_processing` |
| `generate_module_website.py` | Website generation | `html_website` |
| `generate_syllabus_renderings.py` | Syllabus processing | `schedule`, `batch_processing` |
| `publish_course.py` | Publish to PUBLISHED/ | `publish` |
| `validate_outputs.py` | Validate outputs | `validation` |
| `flatten_published.py` | Flatten directories | `publish.utils` |
| `renumber_questions.py` | Question renumbering | `content_processing` |
| `import_legacy_materials.py` | Import legacy | `legacy_import` |

See [../scripts/README.md](../scripts/README.md) for detailed documentation.

---

## Course Parity Matrix

| Document Type | BIOL-1 | BIOL-8 | Notes |
|---------------|--------|--------|--------|
| **keys-to-success.md** | 16 | 17 | One per `course/module-*` |
| **questions.md** | 16 | 17 | One per module |
| **Labs** | 17 protocols + dashboards | 18 protocols + dashboards | See each course `course/labs/` |
| **Exams** | 2 + keys on disk | 3 + keys on disk | Teacher-only; see `course/exams/` |
| **Quizzes** | Templates | 17 × 2 files | BIOL-8 full set in `course/quizzes/` |
| **Practice tests** | 3 + keys | 11 + keys (on disk) | `course/practice_tests/` |
| **Syllabus** | 2 sources | 2 sources | + `syllabus/output/` |
| **Schedule** | 1 source | 1 source | + rendered outputs |
| **Slides** | 30 PDFs in `resources/slides/` (module **9** missing both variants) | 15 PDFs in `resources/slides/` | Pre-generated; not rendered by pipeline |
| **Website output** | Per-module `output/website/` | Per-module `output/website/` | After generation |

### Priority actions (high level)

1. **BIOL-1 assessments:** Add unit coverage for modules 12–16 and/or final as the term requires; quizzes remain template-only unless the course adopts a BIOL-8-style quiz set.
2. **Labs:** Finish any remaining lab stubs the instructor wants taught this term.
3. **BIOL-1 slides:** Add module **9** full + notes PDFs if slides are required for that module.
4. **Module `resources/`:** Populate optional per-module assets when needed.

---

## Configuration Reference

### publish.toml

The main configuration file controls the entire pipeline:

```toml
[publish]
clean = true        # Clear outputs before generation
verbose = false     # Enable verbose logging

[publish.formats]
pdf  = true         # PDF files (via WeasyPrint)
docx = true         # Word documents
html = true         # HTML files
txt  = true         # Plain text
mp3  = false        # Audio narration (slower, ~30s per file)

[publish.courses.biol-1]
enabled = true
include_labs = true
include_syllabus = true

[publish.courses.biol-8]
enabled = true
include_labs = true
# Note: Exams are NOT published (teacher-only materials)

[publish.pipeline]
generate = true     # Generate outputs from source
publish  = true     # Copy to PUBLISHED/
flatten  = true     # Flatten and reorganize to categories
validate = true     # Validate all outputs
```

### Key Settings

| Setting | Purpose | Default |
|---------|---------|---------|
| `publish.clean` | Clear existing outputs first | `true` |
| `publish.formats.mp3` | Generate audio (slow) | `false` |
| `publish.courses.*.enabled` | Enable/disable specific course | `true` |
| `publish.pipeline.validate` | Run validation after generation | `true` |

---

## Real Methods Policy

> ⚠️ **Important**: This repository follows a strict Real Methods Policy.

**All code uses real implementations—no mocks, stubs, or fake methods.**

This applies to:

- ✅ All library implementations (WeasyPrint, gTTS, etc.)
- ✅ All file operations (real file system)
- ✅ All validation logic
- ✅ All tests (no mocking)

See [../../.cursorrules](../../.cursorrules) for the complete policy statement.

---

## Documentation Map

```
software/
├── README.md              ← Project entry point
├── AGENTS.md              ← API reference (function signatures)
├── docs/
│   ├── README.md          ← YOU ARE HERE
│   ├── QUICKSTART.md      → Installation and quick commands
│   ├── ARCHITECTURE.md    → System design, document types, diagrams
│   ├── ORCHESTRATION.md   → Multi-module workflows, publish pipeline
│   ├── AGENTS.md          → Documentation standards, output formats
│   ├── LAB_FORMAT.md      → Lab protocol authoring guide
│   ├── DASHBOARD_FORMAT.md → Interactive dashboard format guide
│   ├── COURSE_STRUCTURE.md → Course directory layout reference
│   ├── OUTPUT_PDF.md      → PDF output format details
│   ├── OUTPUT_AUDIO.md    → MP3 audio output format details
│   ├── OUTPUT_DOCX.md     → DOCX output format details
│   └── OUTPUT_HTML.md     → HTML output format details (all 4 types)
├── src/
│   ├── README.md          → Source code overview
│   └── AGENTS.md          → Module implementations
├── tests/
│   ├── README.md          → Test suite overview
│   └── AGENTS.md          → Testing standards
└── scripts/
    ├── generate_all_outputs.py   → Generate all course outputs
    └── generate_module_website.py → Generate single module website
```

---

## Quick Links

### By Task

| I want to... | Go to... |
|--------------|----------|
| **Install the software** | [QUICKSTART.md#prerequisites](QUICKSTART.md#-prerequisites) |
| **Convert Markdown to PDF** | [QUICKSTART.md#convert-markdown-to-pdf](QUICKSTART.md#convert-markdown-to-pdf) |
| **Generate audio from text** | [QUICKSTART.md#generate-audio](QUICKSTART.md#generate-audio) |
| **Process schedule files** | [ORCHESTRATION.md#schedule-processing-pipeline](ORCHESTRATION.md#3-schedule-processing-pipeline-schedule-processing-pipeline) |
| **Generate HTML website** | [ORCHESTRATION.md#html-website-generation](ORCHESTRATION.md#4-html-website-generation-html-website-generation) |
| **Combine modules in workflows** | [ORCHESTRATION.md](ORCHESTRATION.md) |
| **Understand the architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **Run tests** | [QUICKSTART.md#running-tests](QUICKSTART.md#running-tests) |
| **Look up a function** | [../AGENTS.md](../AGENTS.md) |
| **Generate lab manuals** | [ORCHESTRATION.md#lab-manual-generation](ORCHESTRATION.md#lab-manual-generation) |
| **Run full publish pipeline** | [QUICKSTART.md#full-publish-pipeline](QUICKSTART.md#full-publish-pipeline-recommended) |

### By Module

| Module | Quick Start | API | Tests |
|--------|-------------|-----|-------|
| markdown_to_pdf | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#markdown-to-pdf-rendering) | [Tests](../tests/test_markdown_to_pdf_main.py) |
| text_to_speech | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#text-to-speech-generation) | [Tests](../tests/test_text_to_speech_main.py) |
| schedule | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#schedule-processing) | [Tests](../tests/test_schedule_main.py) |
| html_website | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#html-website-generation) | [Tests](../tests/test_html_website_features.py) |
| batch_processing | [ORCHESTRATION](ORCHESTRATION.md) | [API](../AGENTS.md#batch-processing) | [Tests](../tests/test_batch_processing_main.py) |
| format_conversion | [ORCHESTRATION](ORCHESTRATION.md) | [API](../AGENTS.md#format-conversion) | [Tests](../tests/test_format_conversion_utils.py) |

---

## Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| `OSError: cannot load library 'pangocairo'` | [QUICKSTART.md#pdf-generation-fails](QUICKSTART.md#pdf-generation-fails) |
| `ModuleNotFoundError: No module named 'src'` | [QUICKSTART.md#module-not-found](QUICKSTART.md#module-not-found) |
| `gTTSError: 429 (Too Many Requests)` | [QUICKSTART.md#audio-generation-fails](QUICKSTART.md#audio-generation-fails) |
| Pipeline fails mid-way | [ORCHESTRATION.md#error-recovery-patterns](ORCHESTRATION.md#error-recovery-patterns) |
| Slow processing | [ORCHESTRATION.md#batch-processing-tips](ORCHESTRATION.md#batch-processing-tips) |
| Environment setup issues | [QUICKSTART.md#environment-verification-checklist](QUICKSTART.md#environment-verification-checklist) |

---

## Documentation Standards

1. **Navigation Headers**: Every doc links to related docs
2. **Consistent Structure**: Standardized sections across all docs
3. **Working Code Examples**: All examples are tested and runnable
4. **Current Statistics**: Test counts and coverage updated regularly
5. **Cross-References**: Links between related content

See [AGENTS.md](AGENTS.md) for complete documentation standards.

---

## External Links

| Resource | URL |
|----------|-----|
| BIOL-1 Public Repository | [github.com/docxology/biol-1](https://github.com/docxology/biol-1) |
| BIOL-8 Public Repository | [github.com/docxology/biol-8](https://github.com/docxology/biol-8) |
| Dr. Daniel Ari Friedman | [@docxology](https://github.com/docxology) |

---

## Version History

**Current Version**: `0.1.0` (pre-release)

> 📋 For detailed versioning information including semantic versioning policy, module stability, and function signatures, see [ARCHITECTURE.md#versioning](ARCHITECTURE.md#versioning).

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-23 | Pipeline logging improvements: 9-step renumber, per-step timing, publish_course collapse, validate_published scan reduction. TO-DO-PACKAGE.md added to `software/src/`. |
| 0.1.0 | 2026-02-23 | Comprehensive BIOL-1 Modules 7-11 Labs completion and repo-wide synchronization. |
| 0.1.0 | 2026-02-08 | Documentation consolidation (absorbed HOW_IT_WORKS, GENERATION, DOCUMENT_TYPES) |
| 0.1.0 | 2026-02-04 | Documentation synchronization (date updates, module count correction) |
| 0.1.0 | 2026-02-03 | Documentation improvements (scripts README, cross-references) |
| 0.1.0 | 2026-02-02 | Added versioning documentation to ARCHITECTURE.md and QUICKSTART.md |
| 0.1.0 | 2026-02-01 | Updated statistics (420 tests, 74% coverage), added validation module |
| 0.1.0 | 2026-01-15 | Updated statistics, corrected module count |
| 0.1.0 | 2026-01-09 | Updated test counts and coverage tracking |
| 0.1.0 | 2026-01-08 | Enhanced documentation modularity and signposting |
| 0.1.0 | 2026-01-01 | Initial comprehensive documentation |

### Version Locations

| Location | Purpose |
|----------|---------|
| `pyproject.toml` | Package metadata (`version = "0.1.0"`) |
| `src/__init__.py` | Runtime access (`__version__ = "0.1.0"`) |
