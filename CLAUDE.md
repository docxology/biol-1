# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Complete Documentation**: See [software/docs/README.md](software/docs/README.md) for visual diagrams, the full documentation map, and system architecture.

## Project Overview

CR-BIO is a course management and content generation system for Biology courses at College of the Redwoods. It converts Markdown source files into multiple output formats (PDF, DOCX, HTML, TXT, MD, MP3, interactive websites) for two courses:

- **BIOL-1**: Biology at Pelican Bay (17 modules)
- **BIOL-8**: Human Biology at College of the Redwoods (15 modules)

## Development Commands

All Python commands run from `software/` using `uv` as the package manager.

```bash
# Install dependencies
cd software && uv sync --extra dev

# System deps for WeasyPrint (macOS)
brew install cairo pango gdk-pixbuf glib
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH"
```

Note: `publish.py` auto-sets `DYLD_FALLBACK_LIBRARY_PATH` on macOS, so manual export is only needed when running scripts directly.

### Testing

```bash
cd software
uv run pytest tests/ -v                                    # All tests
uv run pytest tests/test_batch_processing_main.py -v       # Single file
uv run pytest tests/test_batch_processing_main.py::test_name -v  # Single test
uv run pytest -m "not requires_internet"                   # Skip network tests
uv run pytest --cov=src --cov-report=html                  # Coverage report
```

Note: `pyproject.toml` already configures `--cov=src`, `--cov-report=term-missing`, and `-v` via `addopts`.

### Linting & Formatting

```bash
cd software
uv run black src/ tests/ --check   # Format check (line-length=100, py311)
uv run ruff check src/ tests/      # Lint (line-length=100, py311)
uv run mypy src/                   # Type check (disallow_untyped_defs=true)
```

### Content Generation

```bash
# Full publishing pipeline from repo root (reads publish.toml config)
python publish.py
python publish.py --dry-run                    # Preview without executing
python publish.py --override-formats pdf,html  # Override formats

# Git operations
python publish.py --git-only     # Skip generation, commit + push only
python publish.py --skip-git     # Run pipeline but skip git push
python publish.py --setup-git    # Configure git remotes from publish.toml

# Direct script access from software/
cd software
uv run python scripts/generate_all_outputs.py --course biol-8        # One course
uv run python scripts/generate_module_renderings.py --course biol-8 --module 1  # Single module
uv run python scripts/generate_module_website.py --course biol-8 --module 1     # Single website
uv run python scripts/generate_syllabus_renderings.py --course biol-8           # Syllabus
uv run python scripts/publish_course.py --course all                 # Publish to PUBLISHED/
uv run python scripts/validate_outputs.py --course all               # Validate outputs
```

## Architecture

### Directory Layout

```text
course_development/          # Source content (Markdown)
  biol-{1,8}/
    course/
      module-XX-topic/       # keys-to-success.md, questions.md, output/
      labs/                  # lab-XX_topic.md + dashboards/ (HTML)
      exams/, quizzes/       # BIOL-8 only: assessment content
    syllabus/                # Syllabus.md, Schedule.md, output/
    resources/               # Slides PDFs
    private/                 # Instructor-only (not published)

PUBLISHED/                   # Generated outputs (independent git repos per course)
  biol-1/                    # → github.com/docxology/biol-1
  biol-8/                    # → github.com/docxology/biol-8

software/
  src/                       # 15 Python modules
  scripts/                   # CLI orchestration scripts
  tests/                     # pytest test suite
```

### Software Module Layers

Modules are in `software/src/`. Each has `__init__.py`, `main.py` (public API), `utils.py`, `config.py`.

**Layer 0 - Independent:** `module_organization`, `file_validation`

**Layer 1 - Core converters:** `markdown_to_pdf` (WeasyPrint), `text_to_speech` (gTTS), `speech_to_text` (SpeechRecognition), `lab_manual`

**Layer 2 - Composition:** `format_conversion`, `content_processing`

**Layer 3 - Orchestration:** `batch_processing`, `html_website`, `schedule`

**Layer 4 - Integration:** `canvas_integration`, `publish`, `validation`, `legacy_import`

### Publishing Pipeline

Configured via `publish.toml` at repo root. Six stages: generate → publish → copy_extras → flatten → validate → git_push. The top-level `publish.py` reads this config and delegates to `software/scripts/publish_all.py`.

Available formats: `pdf`, `docx`, `html`, `txt`, `md`, `mp3`. Per-course module/lab limits are configurable via `max_module` and `max_lab` in `publish.toml`.

PUBLISHED/ subdirectories are independent git repos. `publish.py` uses `git subtree push` to deploy each course to its public repo (configured in `publish.toml [publish.git.repos.*]`).

### Content Structure

Each module contains two source files:

- `keys-to-success.md` - Learning objectives, key concepts, study tips
- `questions.md` - Study/review questions

Labs use special directive syntax for interactive HTML dashboards:

- `{fill:text}`, `{fill:textarea rows=N}` - Fillable fields
- `<!-- lab:data-table rows=N -->` - Data tables
- `<!-- lab:reflection -->` - Reflection boxes

## Real Methods Policy

**No mocks, stubs, or fakes anywhere in the codebase.** This is enforced in `.cursorrules`:

- All functions use real library implementations (WeasyPrint, gTTS, etc.)
- All tests use real file operations and real library calls
- External API tests validate structure/logic only, not actual API calls
- Integration tests requiring external services are marked with `@pytest.mark.requires_internet` or `@pytest.mark.requires_api`

## Key Conventions

- Python 3.11+, managed with `uv`
- Type hints on all functions, docstrings required
- Black formatting (100 char lines), Ruff linting, mypy type checking
- Module public API lives in `main.py`, internals in `utils.py`, constants in `config.py`
- Two supported courses: `biol-1` (17 modules) and `biol-8` (15 modules) defined in `batch_processing/config.py` as `SUPPORTED_COURSES`
