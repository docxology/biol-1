# Scripts

> **Navigation**: [← README](../README.md) | [AGENTS.md](../AGENTS.md) | [docs/](../docs/) | [src/](../src/)

Thin CLI orchestrators for course material generation, validation, and publishing. Scripts parse arguments, bootstrap paths, configure logging, and delegate to `src/` packages; all business logic lives in `src/`. See [AGENTS.md](AGENTS.md) for the thin-orchestrator contract and gotchas.

Run commands are shown from `software/` (where `pyproject.toml` lives); `uv run` resolves the project virtualenv.

## Script-to-Module Mapping

| Script | Purpose | Delegates to | Run command |
|--------|---------|--------------|-------------|
| `publish_all.py` | End-to-end pipeline: generate → publish → validate | `src.batch_processing`, `src.publish`, `src.validation` | `uv run python scripts/publish_all.py [--clean] [--skip-generation] [--skip-mp3]` |
| `generate_all_outputs.py` | Generate all output formats for one or all courses | `src.batch_processing`, `src.module_content` | `uv run python scripts/generate_all_outputs.py --course biol-1` |
| `generate_module_materials.py` | Regenerate `module.toml`-derived materials (key-points/questions/practice-quiz + deterministic SVGs) | `src.module_content` | `uv run python scripts/generate_module_materials.py --course biol-1 [--module N] [--dry-run]` |
| `generate_module_renderings.py` | Process a single module | `src.batch_processing` (`process_module_by_type`) | `uv run python scripts/generate_module_renderings.py --course biol-1 --module 1` |
| `generate_module_website.py` | Build a module's interactive HTML site | `src.batch_processing` → `src.html_website` | `uv run python scripts/generate_module_website.py --course biol-1 --module 1` |
| `generate_slide_decks.py` | Render BIOL-1 slide decks (full + notes HTML sources, PDF) from module manifests | `src.slide_deck` | `uv run python scripts/generate_slide_decks.py --course biol-1 [--module N] [--dry-run]` |
| `generate_module_videos.py` | Generate LectureCreate YAML manifests and render lecture videos per module | `src.lecture_create` + `lecturecreate` CLI | `uv run python scripts/generate_module_videos.py --module 1 [--render] [--dry-run]` (or `--all`) |
| `generate_syllabus_renderings.py` | Render syllabus sources into `syllabus/output/` | `src.batch_processing` (`process_syllabus`) | `uv run python scripts/generate_syllabus_renderings.py --course biol-1` |
| `generate_course_by_date.py` | Build BIOL-1 dated copy-only teaching handoffs from `course_calendar.toml` | `src.course_by_date` | `uv run python scripts/generate_course_by_date.py [--dry-run] [--validate-only]` |
| `generate_biol1_lab_dashboards.py` | Regenerate active BIOL-1 lab dashboards from the lab list | stdlib only (BIOL-1 lab specs) | `uv run python scripts/generate_biol1_lab_dashboards.py` |
| `publish_course.py` | Copy generated outputs into `PUBLISHED/<course>/` | `src.publish` | `uv run python scripts/publish_course.py --course biol-1` |
| `flatten_published.py` | Flatten per-module outputs into distribution buckets | `src.publish.utils` | `uv run python scripts/flatten_published.py [--dry-run] [--verbose]` |
| `validate_outputs.py` | Validate generated outputs for every in-scope module | `src.validation`, `src.course_by_date`, `src.lecture_create.validation` | `uv run python scripts/validate_outputs.py --course all [--json]` |
| `validate_repo_contracts.py` | Validate documentation/repository invariants without rendering artifacts | `src.validation.repo_contracts` | `uv run python scripts/validate_repo_contracts.py [--json]` |
| `renumber_questions.py` | Convert section-based question numbering to continuous | `src.content_processing` | `uv run python scripts/renumber_questions.py --course all [--dry-run]` |
| `shuffle_final_exam_mc.py` | Shuffle final-exam Part A MC options and re-key the answer key | `src.exam_tools` | `uv run python scripts/shuffle_final_exam_mc.py [--dry-run] [--spacing-only]` |
| `import_legacy_materials.py` | Import the legacy bio_1_2025 lesson archive into the current module layout | `src.legacy_import` | `uv run python scripts/import_legacy_materials.py [--dry-run] [--skip-questions] [--skip-slides]` |
| `assemble_practice_test_12.py` | Rebuild archived Spring 2026 `practice-test-12` + key from PT01–11 slices | stdlib only (`archive/spring-2026/course_development/biol-8/course/practice_tests/`) | `uv run python scripts/assemble_practice_test_12.py` |
| `utils.py` | Shared CLI helper (`print_module_not_found`); not runnable | — | imported by other scripts as `scripts.utils` |

## Conventions

- Run scripts from `software/` via `uv run python scripts/<script>.py` so third-party dependencies resolve from the project environment.
- Course-scoped scripts take `--course {biol-1, all}`. Archived BIOL-8 is not a live target.
- Format selection is `--formats pdf,docx,html,txt,md,mp3` (comma-separated; defaults vary per script).
- Most scripts accept `--verbose` for INFO-level logging. Exit code `0` = success, non-zero = at least one error; per-item errors are collected and reported in the summary even when the run continues.
- Every script that imports `from src…` bootstraps `sys.path` itself, so scripts also run with plain `python3` from any working directory (third-party dependencies still come from the `uv` environment).
- Per-script option details: `uv run python scripts/<script>.py --help`.

## Course-by-date projection

For BIOL-1, the canonical date-to-material mapping is
`course_development/biol-1/course_calendar.toml`. Only records marked
`used = true` are copied into the dated, copy-only teaching handoffs. The
generated `meeting.json` files preserve planned/used state and source
checksums, and LectureCreate build intermediates (frames, WAVs, hashes) are
excluded.

## Logging

Each run writes a timestamped log to
`software/logs/generation_YYYY-MM-DD_HH-MM-SS.log` containing start/end times,
every file processed, errors, and summary statistics. The directory is
git-ignored; see `software/logs/AGENTS.md`.

## Dependencies

- System libraries (macOS, for PDF/DOCX/audio generation):
  `brew install cairo pango gdk-pixbuf glib ffmpeg`, plus
  `export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"`.
- Python dependencies are managed via `uv` and `software/pyproject.toml`:
  `cd software && uv sync --extra dev`.

## Related Documentation

| Document | Description |
|----------|-------------|
| [../docs/QUICKSTART.md](../docs/QUICKSTART.md) | Installation and quick commands |
| [../docs/ORCHESTRATION.md](../docs/ORCHESTRATION.md) | Multi-module workflows |
| [../src/README.md](../src/README.md) | Source module overview |
| [../src/AGENTS.md](../src/AGENTS.md) | Module API reference |
