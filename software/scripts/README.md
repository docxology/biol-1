# Scripts

> **Navigation**: [← README](../README.md) | [AGENTS.md](../AGENTS.md) | [docs/](../docs/) | [src/](../src/)

Thin CLI orchestrators for course material generation and publishing. All business logic resides in `src/` modules; scripts handle CLI parsing and orchestration only.

---

## Thin Orchestrator Pattern

Scripts follow the "thin orchestrator" pattern:

```
Script (CLI parsing) → Module (business logic) → Output
```

Scripts do NOT contain business logic. They:

1. Parse command-line arguments
2. Call module functions from `src/`
3. Report results

---

## Script-to-Module Mapping

| Script | Primary Module(s) | Purpose |
|--------|-------------------|---------|
| `publish_all.py` | `batch_processing`, `publish`, `validation` | **Top-level pipeline** |
| `generate_all_outputs.py` | `batch_processing` | Generate all course outputs |
| `generate_module_renderings.py` | `batch_processing` | Single module processing |
| `generate_module_website.py` | `html_website` | Website generation |
| `generate_syllabus_renderings.py` | `schedule`, `batch_processing` | Syllabus processing |
| `publish_course.py` | `publish` | Publish to PUBLISHED/ |
| `validate_outputs.py` | `validation` | Validate generated outputs |
| `validate_repo_contracts.py` | `validation.repo_contracts` | Validate repository/documentation contracts |
| `generate_biol1_lab_dashboards.py` | (stdlib; BIOL-1 lab specs) | Regenerate active BIOL-1 lab dashboards from the lab list |
| `flatten_published.py` | `publish.utils` | Flatten directory structure |
| `renumber_questions.py` | `content_processing` | Question renumbering |
| `import_legacy_materials.py` | `legacy_import` | Import legacy format |
| `assemble_practice_test_12.py` | (stdlib; archived BIOL-8 practice tests) | Rebuild Spring 2026 cumulative `practice-test-12` + key |

---

## Primary Scripts

### `publish_all.py` — Top-Level Pipeline

The main orchestrator that runs the complete publish pipeline for all enabled courses:

1. **Generate** → Create requested output formats (PDF, DOCX, MD by default; HTML, TXT, MP3 opt-in)
2. **Publish** → Copy to PUBLISHED/ directory
3. **Validate** → Verify all outputs

```bash
# Full publish (~17 min with MP3)
uv run python scripts/publish_all.py --clean --verbose

# Skip MP3 for faster iteration (~5 min)
uv run python scripts/publish_all.py --clean --skip-mp3

# PDF-only for quick testing
uv run python scripts/publish_all.py --clean --formats pdf

# Re-copy/reorganize existing generated outputs without regenerating
uv run python scripts/publish_all.py --skip-generation

# Skip validation when debugging copy/reorganization only
uv run python scripts/publish_all.py --skip-validate
```

| Option | Description |
|--------|-------------|
| `--clean` | Clear outputs before generation |
| `--verbose` | Detailed progress output |
| `--skip-mp3` | Skip audio generation |
| `--formats` | Comma-separated list: pdf,docx,html,txt,md,mp3 |
| `--skip-generation` | Use existing source outputs instead of regenerating |
| `--skip-publish` | Skip copying generated files into `PUBLISHED/` |
| `--skip-copy-extras` | Skip labs, dashboards, slides, and practice-test extras |
| `--skip-flatten` | Skip flattening into `ALL_FILES/` |
| `--skip-validate` | Skip output validation |
| `--skip-labs` | Skip lab manual rendering during generation |
| `--max-module` | Limit module processing per course, e.g. `biol-1:6` |
| `--max-lab` | Limit lab processing per course, e.g. `biol-1:5` |
| `--strict-dashboards` | Enforce one-dashboard-per-numbered-lab invariant plus course overrides |

---

### `generate_all_outputs.py` — Course Output Generation

Generate all output formats for modules in a course:

```bash
# Generate for one course
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate for specific module
uv run python scripts/generate_all_outputs.py --course biol-1 --module 1

# All courses, all modules
uv run python scripts/generate_all_outputs.py --course all

# Dry run
uv run python scripts/generate_all_outputs.py --course biol-1 --dry-run
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`) or `all` |
| `--module` | Optional: specific module number |
| `--formats` | Output formats (default: all) |
| `--dry-run` | Preview without generating |
| `--skip-clear` | Don't clear existing outputs |
| `--no-website` | Skip website generation |
| `--skip-labs` | Skip lab manual rendering |

**Module Used**: `src/batch_processing`

---

### `publish_course.py` — Publish to PUBLISHED/

Copy generated outputs to the PUBLISHED directory:

```bash
# Publish all courses
uv run python scripts/publish_course.py --course all

# Publish specific course
uv run python scripts/publish_course.py --course biol-1
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`) or `all` |

**Module Used**: `src/publish`

---

### `validate_outputs.py` — Output Validation

Validate that generated outputs meet quality standards:

```bash
# Validate all courses
uv run python scripts/validate_outputs.py --course all

# Validate specific course
uv run python scripts/validate_outputs.py --course biol-1

# Verbose output
uv run python scripts/validate_outputs.py --course all --verbose
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`) or `all` |
| `--formats` | Comma-separated list of formats to validate |
| `--max-module` | Limit module validation per course, e.g. `biol-1:15` |
| `--max-lab` | Limit lab validation per course, e.g. `biol-1:17` |
| `--strict-dashboards` | Enforce dashboard invariant for numbered labs |
| `--verbose` | Detailed validation output |

**Module Used**: `src/validation`

---

### `validate_repo_contracts.py` — Repository Contract Validation

Validate documentation and repository invariants without rendering artifacts:

```bash
uv run python scripts/validate_repo_contracts.py
uv run python scripts/validate_repo_contracts.py --json
```

Checks include:

- `README.md` and `AGENTS.md` coverage under `course_development/` and `software/src/`
- Relative Markdown links in root, software, and course-development docs
- `publish.toml` course module/lab counts against source folders
- `PUBLISHED/` tracked status for subtree publishing
- Production Python source free of mock/test-double imports

**Module Used**: `src/validation/repo_contracts.py`

---

## Single-Item Scripts

### `generate_module_renderings.py` — Single Module Processing

Process one module by course name and module number:

```bash
uv run python scripts/generate_module_renderings.py --course biol-1 --module 1
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`; default: `biol-1`) |
| `--module` | Module number to process (default: `1`) |

Output goes to that module's `output/` via `process_module_by_type`.

**Module Used**: `src/batch_processing`

---

### `generate_module_website.py` — Website Generation

Delegates to **`batch_processing.process_module_website`** (which calls **`html_website.generate_module_website`**).

```bash
uv run python scripts/generate_module_website.py --course biol-1 --module 1
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`; default: `biol-1`) |
| `--module` | Module number (default: `1`) |

**Module Used**: `src/batch_processing` → `src/html_website`

---

### `generate_syllabus_renderings.py` — Syllabus Processing

Renders syllabus sources under ``course_development/<course>/syllabus/`` into ``syllabus/output/``.

```bash
uv run python scripts/generate_syllabus_renderings.py --course biol-1
```

| Option | Description |
|--------|-------------|
| `--course` | Active course id (`biol-1`; default: `biol-1`) |

**Module Used**: `src/batch_processing` (`process_syllabus`)

---

## Utility Scripts

### `flatten_published.py` — Flatten Directory Structure

Move files from subdirectories to module root for simpler distribution:

```bash
# Flatten all published content
uv run python scripts/flatten_published.py

# Dry run
uv run python scripts/flatten_published.py --dry-run

# Verbose
uv run python scripts/flatten_published.py --verbose
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview without modifying |
| `--verbose` | Show each file operation |

**Module Used**: `src/publish.utils.flatten_published`

---

### `renumber_questions.py` — Question Renumbering

Convert section-based question numbering to continuous numbering:

```bash
# Process all courses
uv run python scripts/renumber_questions.py --course all

# Specific course
uv run python scripts/renumber_questions.py --course biol-1

# Dry run
uv run python scripts/renumber_questions.py --course biol-1 --dry-run
```

Before: `1.`, `2.`, `3.` per section
After: `1.`, `2.`, `3.`, `4.`, `5.`... continuously

**Module Used**: `src/content_processing`

---

## Migration Scripts

### `import_legacy_materials.py` — Legacy Import

Import materials from legacy bio_1_2025 format:

```bash
uv run python scripts/import_legacy_materials.py /path/to/legacy --course biol-1
```

| Option | Description |
|--------|-------------|
| `source_path` | Required: path to legacy materials |
| `--course` | Target course directory |
| `--dry-run` | Preview without importing |

**Module Used**: `src/legacy_import`

### `assemble_practice_test_12.py` — Archived BIOL-8 practice-test-12 assembler

Rebuilds student and key Markdown for the archived Spring 2026 cumulative **`practice-test-12`** set from scripted slices of earlier practice tests. Logic lives entirely in this file (paths under `archive/spring-2026/course_development/biol-8/course/practice_tests/`).

```bash
cd software && uv run python scripts/assemble_practice_test_12.py
```

Read the script docstring before editing `SPEC` or output paths.

---

## Output Formats

| Format | Extension | Description | Generator |
|--------|-----------|-------------|-----------|
| PDF | `.pdf` | Print-ready document | WeasyPrint |
| DOCX | `.docx` | Microsoft Word format | python-docx |
| HTML | `.html` | Web page | Markdown + custom |
| MP3 | `.mp3` | Audio narration | local TTS + ffmpeg |
| TXT | `.txt` | Plain text extraction | Markdown strip |
| MD | `.md` | Markdown copy (prefixed) | Copy + rename |

---

## Naming Convention

Output files are prefixed with module name for unique identification:

```
module-01-questions.pdf       (not questions.pdf)
module-01-keys-to-success.mp3 (not keys-to-success.mp3)
module-01-assignment-01.docx  (not assignment-01.docx)
```

This ensures files remain identifiable when distributed or combined.

---

## Dependencies

### System Libraries (macOS)

```bash
# Required for PDF/DOCX/audio generation
brew install cairo pango gdk-pixbuf glib ffmpeg

# Set library path (add to ~/.zshrc for persistence; matches publish.py / CLAUDE.md)
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
```

### Python Dependencies

All managed via `uv` and `pyproject.toml`:

```bash
cd software
uv sync --extra dev
```

---

## Logging

Logs are written to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log`.

Each run creates a new timestamped log file with:

- Start/end times
- Files processed
- Errors encountered
- Summary statistics

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [../docs/QUICKSTART.md](../docs/QUICKSTART.md) | Installation and quick commands |
| [../docs/ORCHESTRATION.md](../docs/ORCHESTRATION.md) | Multi-module workflows |
| [../src/README.md](../src/README.md) | Source module overview |
| [../src/AGENTS.md](../src/AGENTS.md) | Module API reference |
