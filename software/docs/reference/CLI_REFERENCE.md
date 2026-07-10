# CLI Reference

> **Navigation**: [← Reference Home](README.md) | [Config Reference](CONFIG_REFERENCE.md) | [Troubleshooting](TROUBLESHOOTING.md) | [Glossary](GLOSSARY.md)

Complete reference for every CLI script in `software/scripts/`. All commands are run from the `software/` directory unless noted otherwise.

---

## Contents

- [Top-Level Entry Point](#top-level-entry-point)
- [Pipeline Scripts](#pipeline-scripts)
- [Generation Scripts](#generation-scripts)
- [Validation Scripts](#validation-scripts)
- [Utility Scripts](#utility-scripts)
- [Migration Scripts](#migration-scripts)
- [Script Summary Table](#script-summary-table)

---

## Top-Level Entry Point

### `publish.py` — Top-Level Pipeline (repo root)

**Purpose**: Reads `publish.toml` and orchestrates the full publish pipeline — generate, publish, flatten, validate, and git push.

**Backing module**: `src.shared.runtime`, `src.shared.course_config`, delegates to `scripts/publish_all.py`

**Run from**: Repository root (not `software/`)

```bash
# Full publish pipeline
python publish.py

# Dry run — preview without executing
python publish.py --dry-run

# Override formats on command line
python publish.py --override-formats pdf,docx,md

# Skip generation, only run git commit and push
python publish.py --git-only

# Run pipeline but skip git push
python publish.py --skip-git

# Set up git remotes from config and exit
python publish.py --setup-git
```

| Option | Type | Description |
|--------|------|-------------|
| `--dry-run` | flag | Show what would be generated without executing |
| `--override-formats` | string | Override config formats (comma-separated: `pdf,docx,md`) |
| `--setup-git` | flag | Set up git remotes from `publish.toml` and exit |
| `--git-only` | flag | Skip generation; only run git commit and push |
| `--skip-git` | flag | Run pipeline but skip git operations even if enabled |

---

## Pipeline Scripts

### `publish_all.py` — Complete Pipeline Orchestrator

**Purpose**: Orchestrates the full course publishing workflow: clean → generate → publish → copy extras → flatten → reorganize → validate.

**Backing modules**: `src.batch_processing`, `src.publish`, `src.validation`

```bash
# Full publish (~17 min with MP3)
uv run python scripts/publish_all.py --clean --verbose

# Skip MP3 for faster iteration (~5 min)
uv run python scripts/publish_all.py --clean --skip-mp3

# PDF-only for quick testing
uv run python scripts/publish_all.py --clean --formats pdf

# Re-copy/reorganize existing outputs without regenerating
uv run python scripts/publish_all.py --skip-generation

# Skip validation when debugging copy/reorganization only
uv run python scripts/publish_all.py --skip-validate
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--clean` | flag | off | Clean `PUBLISHED/` directory before starting |
| `--clean-source-outputs` | flag | off | Clean source `output/` directories before generation |
| `--verbose`, `-v` | flag | off | Show detailed output from subscripts |
| `--skip-mp3` | flag | off | Skip MP3 audio generation (faster iteration) |
| `--formats` | string | `all` | Comma-separated formats: `pdf,mp3,docx,html,txt,md` |
| `--skip-generation` | flag | off | Use existing source outputs instead of regenerating |
| `--skip-publish` | flag | off | Skip copying generated files into `PUBLISHED/` |
| `--skip-copy-extras` | flag | off | Skip labs, dashboards, slides, and practice-test extras |
| `--skip-flatten` | flag | off | Skip flattening into `ALL_FILES/` |
| `--skip-validate` | flag | off | Skip output validation |
| `--skip-labs` | flag | off | Skip lab manual rendering during generation |
| `--max-module` | string (appendable) | — | Limit module processing per course (e.g. `biol-1:6`) |
| `--max-lab` | string (appendable) | — | Limit lab processing per course (e.g. `biol-1:5`) |
| `--strict-dashboards` | flag | off | Enforce one-dashboard-per-numbered-lab invariant |

### `publish_course.py` — Publish to PUBLISHED/

**Purpose**: Copy generated outputs to the `PUBLISHED/` directory.

**Backing module**: `src.publish`

```bash
# Publish all courses
uv run python scripts/publish_course.py --course all

# Publish specific course
uv run python scripts/publish_course.py --course biol-1
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--course` | string | yes | Active course id (`biol-1`) or `all` |

---

## Generation Scripts

### `generate_all_outputs.py` — Course Output Generation

**Purpose**: Generate all output formats for modules, syllabi, labs, practice tests, and exams across one or all courses.

**Backing module**: `src.batch_processing`

```bash
# Generate for one course
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate for specific module
uv run python scripts/generate_all_outputs.py --course biol-1 --module 1

# All courses, all modules
uv run python scripts/generate_all_outputs.py --course all

# Dry run
uv run python scripts/generate_all_outputs.py --course biol-1 --dry-run

# Specific formats only
uv run python scripts/generate_all_outputs.py --formats pdf,docx,md
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `all` | Active course id or `all` |
| `--module` | int | all modules | Specific module number to process |
| `--formats` | string | `all` | Comma-separated formats: `pdf,mp3,docx,html,txt,md` |
| `--dry-run` | flag | off | Preview without generating files |
| `--skip-clear` | flag | off | Don't clear existing outputs before generation |
| `--no-website` | flag | off | Skip website generation |
| `--skip-labs` | flag | off | Skip lab manual rendering |
| `--max-module` | string (appendable) | — | Max module per course (e.g. `biol-1:6`) |
| `--max-lab` | string (appendable) | — | Max lab per course (e.g. `biol-1:5`) |

### `generate_module_materials.py` — Structured Module Materials

**Purpose**: Generate BIOL-1 module Markdown, practice quizzes, and deterministic SVG assets from `module.toml` manifests.

**Backing module**: `src.module_content`

```bash
# Generate for all courses
uv run python scripts/generate_module_materials.py --course all

# Generate for a specific course
uv run python scripts/generate_module_materials.py --course biol-1

# Single module
uv run python scripts/generate_module_materials.py --course biol-1 --module 3

# Dry run
uv run python scripts/generate_module_materials.py --course biol-1 --dry-run
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `all` | Active course id or `all` |
| `--module` | int | all modules | Optional module number |
| `--dry-run` | flag | off | Report generated files without writing |

### `generate_module_renderings.py` — Single Module Processing

**Purpose**: Process one module by course name and module number. Output goes to that module's `output/` directory.

**Backing module**: `src.batch_processing` (`process_module_by_type`)

```bash
# Generate renderings for biol-1 module-1 (default)
uv run python scripts/generate_module_renderings.py

# Generate renderings for biol-1 module-2
uv run python scripts/generate_module_renderings.py --course biol-1 --module 2
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `biol-1` | Active course id |
| `--module` | int | `1` | Module number to process |

### `generate_module_website.py` — Website Generation

**Purpose**: Generate an interactive HTML website for a single module.

**Backing module**: `src.batch_processing` → `src.html_website`

```bash
# Generate website for biol-1 module-1 (default)
uv run python scripts/generate_module_website.py

# Generate website for biol-1 module-2
uv run python scripts/generate_module_website.py --course biol-1 --module 2
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `biol-1` | Active course id |
| `--module` | int | `1` | Module number to process |

### `generate_syllabus_renderings.py` — Syllabus Processing

**Purpose**: Render syllabus sources under `course_development/<course>/syllabus/` into `syllabus/output/`.

**Backing module**: `src.batch_processing` (`process_syllabus`)

```bash
# Generate syllabus renderings for biol-1 (default)
uv run python scripts/generate_syllabus_renderings.py

# Generate for biol-1 explicitly
uv run python scripts/generate_syllabus_renderings.py --course biol-1
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `biol-1` | Active course id |

### `generate_slide_decks.py` — Slide Deck Generation

**Purpose**: Generate BIOL-1 slide decks (full and notes HTML + PDF) from structured module manifests.

**Backing module**: `src.slide_deck`

```bash
# Generate for all courses
uv run python scripts/generate_slide_decks.py --course all

# Generate for a specific course
uv run python scripts/generate_slide_decks.py --course biol-1

# Single module
uv run python scripts/generate_slide_decks.py --course biol-1 --module 3

# Dry run
uv run python scripts/generate_slide_decks.py --course biol-1 --dry-run
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `all` | Active course id or `all` |
| `--module` | int | all modules | Optional module number |
| `--dry-run` | flag | off | Report generated files without writing |

### `generate_biol1_lab_dashboards.py` — BIOL-1 Lab Dashboards

**Purpose**: Regenerate exact-stem BIOL-1 lab dashboard HTML files from the active lab list.

**Backing module**: `src.lab_dashboard`

```bash
# Generate dashboards (writes files)
uv run python scripts/generate_biol1_lab_dashboards.py

# Dry run — preview without writing
uv run python scripts/generate_biol1_lab_dashboards.py --dry-run
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--dry-run` | flag | off | Render dashboards without writing files |
| `--course` | string | `biol-1` | Course to generate dashboards for (only `biol-1` supported) |

---

## Validation Scripts

### `validate_outputs.py` — Output Validation

**Purpose**: Validate that generated outputs meet quality standards. Verifies expected files exist for every in-scope module.

**Backing module**: `src.validation`

```bash
# Validate all courses
uv run python scripts/validate_outputs.py --course all

# Validate specific course
uv run python scripts/validate_outputs.py --course biol-1

# Verbose output
uv run python scripts/validate_outputs.py --course all --verbose

# JSON output
uv run python scripts/validate_outputs.py --course all --json
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | required | Active course id or `all` |
| `--formats` | string | `pdf,docx` | Comma-separated list of formats to validate |
| `--json` | flag | off | Output results as JSON |
| `--verbose` | flag | off | Show detailed module-level results |
| `--max-module` | string (appendable) | — | Max module per course (e.g. `biol-1:15`) |
| `--max-lab` | string (appendable) | — | Max lab per course (e.g. `biol-1:17`) |
| `--strict-dashboards` | flag | off | Enforce per-numbered-lab dashboard invariant |

### `validate_repo_contracts.py` — Repository Contract Validation

**Purpose**: Validate documentation and repository invariants without rendering artifacts.

**Backing module**: `src.validation.repo_contracts`

```bash
# Plain text report
uv run python scripts/validate_repo_contracts.py

# JSON report
uv run python scripts/validate_repo_contracts.py --json
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--json` | flag | off | Print JSON report |

**Checks performed**:

- `README.md` and `AGENTS.md` coverage under `course_development/` and `software/src/`
- Relative Markdown links in root, software, and course-development docs
- `publish.toml` course module/lab counts against source folders
- `PUBLISHED/` tracked status for subtree publishing
- Production Python source free of mock/test-double imports

---

## Utility Scripts

### `flatten_published.py` — Flatten Directory Structure

**Purpose**: Move files from subdirectories to module root for simpler distribution.

**Backing module**: `src.publish.utils` (`flatten_published`)

```bash
# Flatten all published content
uv run python scripts/flatten_published.py

# Dry run
uv run python scripts/flatten_published.py --dry-run

# Verbose
uv run python scripts/flatten_published.py --verbose

# Custom path
uv run python scripts/flatten_published.py --path /custom/PUBLISHED
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--path` | string | auto-detect | Path to `PUBLISHED/` directory |
| `--dry-run` | flag | off | Preview without modifying |
| `--verbose` | flag | off | Show each file operation |

### `renumber_questions.py` — Question Renumbering

**Purpose**: Convert section-based question numbering to continuous numbering across all questions in a module.

**Backing module**: `src.content_processing`

```bash
# Process all courses
uv run python scripts/renumber_questions.py --course all

# Specific course
uv run python scripts/renumber_questions.py --course biol-1

# Specific module
uv run python scripts/renumber_questions.py --course biol-1 --module module-03

# Dry run
uv run python scripts/renumber_questions.py --course biol-1 --dry-run --verbose
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `all` | Active course id or `all` |
| `--module` | string | all modules | Process a single module (e.g. `module-03`) |
| `--dry-run` | flag | off | Show what would be changed without writing |
| `--verbose` | flag | off | Show detailed processing information |

---

## Migration Scripts

### `import_legacy_materials.py` — Legacy Import

**Purpose**: Import materials from legacy `bio_1_2025` format into the current module layout.

**Backing module**: `src.legacy_import`

```bash
# Import all materials for biol-1 (default)
uv run python scripts/import_legacy_materials.py

# Dry run to preview
uv run python scripts/import_legacy_materials.py --dry-run

# Import only slides, skip questions
uv run python scripts/import_legacy_materials.py --skip-questions

# Import only questions, skip slides
uv run python scripts/import_legacy_materials.py --skip-slides
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--course` | string | `biol-1` | Target course directory |
| `--dry-run` | flag | off | Preview without importing |
| `--skip-questions` | flag | off | Skip importing chapter questions |
| `--skip-slides` | flag | off | Skip importing slides |

### `assemble_practice_test_12.py` — Archived BIOL-8 Practice Test Assembler

**Purpose**: Rebuild the archived Spring 2026 BIOL-8 cumulative `practice-test-12` student and key Markdown from scripted slices of earlier practice tests (PT01–PT11) plus built-in ecology/evolution items.

**Backing module**: Self-contained (stdlib only; no `src/` dependency)

**Run from**: `software/` directory

```bash
cd software && uv run python scripts/assemble_practice_test_12.py
```

No CLI arguments. Reads the `SPEC` list in the script and writes to `archive/spring-2026/course_development/biol-8/course/practice_tests/`.

> ⚠️ Read the script docstring before editing `SPEC` or output paths.

---

## Script Summary Table

| # | Script | Category | Backing Module(s) |
|---|--------|----------|-------------------|
| 1 | `publish.py` | Top-level | `publish.toml` → `publish_all.py` |
| 2 | `publish_all.py` | Pipeline | `batch_processing`, `publish`, `validation` |
| 3 | `publish_course.py` | Pipeline | `publish` |
| 4 | `generate_all_outputs.py` | Generation | `batch_processing` |
| 5 | `generate_module_materials.py` | Generation | `module_content` |
| 6 | `generate_module_renderings.py` | Generation | `batch_processing` |
| 7 | `generate_module_website.py` | Generation | `batch_processing` → `html_website` |
| 8 | `generate_syllabus_renderings.py` | Generation | `batch_processing` (`process_syllabus`) |
| 9 | `generate_slide_decks.py` | Generation | `slide_deck` |
| 10 | `generate_biol1_lab_dashboards.py` | Generation | `lab_dashboard` |
| 11 | `validate_outputs.py` | Validation | `validation` |
| 12 | `validate_repo_contracts.py` | Validation | `validation.repo_contracts` |
| 13 | `flatten_published.py` | Utility | `publish.utils` |
| 14 | `renumber_questions.py` | Utility | `content_processing` |
| 15 | `import_legacy_materials.py` | Migration | `legacy_import` |
| 16 | `assemble_practice_test_12.py` | Migration | (stdlib; archived BIOL-8) |
| 17 | `utils.py` | Helper | (shared CLI helpers, not user-facing) |

---

## Output Formats

| Format | Extension | Description | Generator | Default |
|--------|-----------|-------------|-----------|---------|
| PDF | `.pdf` | Print-ready document | WeasyPrint | ✓ on |
| DOCX | `.docx` | Microsoft Word format | python-docx | ✓ on |
| HTML | `.html` | Web page | markdown2 | ✗ off |
| MP3 | `.mp3` | Audio narration | local TTS + ffmpeg | ✗ off |
| TXT | `.txt` | Plain text extraction | Markdown strip | ✗ off |
| MD | `.md` | Markdown copy (prefixed) | Copy + rename | ✓ on |

---

## CLI Conventions

- **Course selection**: `--course {biol-1, all}` for active courses. Archived BIOL-8 is not a live target.
- **Format selection**: `--formats pdf,docx,html,txt,md,mp3` (comma-separated; defaults vary per script).
- **Verbosity**: Most scripts accept `--verbose` to enable `INFO`-level logging.
- **Exit codes**: `0` = success, non-zero = at least one error; per-file errors are collected and reported in the summary even when the run continues.
- **Dry runs**: Most scripts support `--dry-run` to preview without writing.

---

## Logging

Each run writes a timestamped log to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log` containing:

- Start/end times
- Every file processed
- Errors encountered
- Summary statistics

The `logs/` directory is git-ignored.

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [../../scripts/README.md](../../scripts/README.md) | Scripts overview and script-to-module mapping |
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Pipeline workflows and composition patterns |
| [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) | Configuration reference for `publish.toml` and `pyproject.toml` |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Troubleshooting guide |
