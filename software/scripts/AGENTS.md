# Technical Documentation: `software/scripts`

Thin CLI orchestrators that wrap `software/src/` packages. Scripts contain only argument parsing and orchestration; all business logic lives in `src/`. See `software/scripts/README.md` for user-facing usage examples.

## Scripts

| Script | Backing package | Entry point | Purpose |
|---|---|---|---|
| `publish_all.py` | `batch_processing`, `publish`, `validation` | `main()` | End-to-end pipeline (generate → publish → validate). |
| `generate_all_outputs.py` | `batch_processing` | `main()` | Generate all output formats for one or all courses. |
| `generate_module_renderings.py` | `batch_processing` | `main()` | Run generation for a single module path. |
| `generate_module_website.py` | `html_website` | `main()` | Build a per-module interactive HTML site. |
| `generate_syllabus_renderings.py` | `schedule`, `batch_processing` | `main()` | Render syllabus / schedule documents. |
| `publish_course.py` | `publish` | `main()` | Copy generated artifacts into `PUBLISHED/<course>/`. |
| `flatten_published.py` | `publish.utils` | `main()` | Move per-module outputs into flat `homework/`, `module_keys/`, … buckets. |
| `validate_outputs.py` | `validation` | `main()` | Verify expected files exist for every in-scope module. |
| `renumber_questions.py` | `content_processing` | `main()` | Convert section-based question numbering to continuous. |
| `import_legacy_materials.py` | `legacy_import` | `main()` | Import an older lesson archive into the current module layout. |
| `assemble_practice_test_12.py` | (stdlib; BIOL-8 content) | `main()` | Rebuild `practice-test-12.md` / `_key.md` from PT01–11 slices (`course_development/biol-8/course/practice_tests/`). |
| `utils.py` | (helpers) | n/a | Shared CLI helpers (course resolution, formatter setup). |

## CLI conventions

- Every script exposes `--course {biol-1, biol-8, all}` where the operation is course-scoped, and `--dry-run` for preview-only runs.
- Format selection uses `--formats pdf,docx,html,txt,md,mp3` (comma-separated; defaults vary per script).
- Most scripts also accept `--verbose` to enable `INFO`-level logging.
- Exit codes: `0` = success, non-zero = at least one error; per-file errors are collected and reported in the summary even when the run continues.

## Logging

Each run writes a timestamped log to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log` containing start/end times, every file processed, errors, and summary statistics. The directory is git-ignored; see `software/logs/AGENTS.md`.

## Adding a script

1. Create the file under `software/scripts/`.
2. Import only from `src/` packages (and `argparse` / stdlib). Never put business logic here.
3. Provide `main()` and an `if __name__ == "__main__": main()` guard.
4. Add an entry to the script-to-module table above and to `README.md`.
5. If the script is meant for the publish pipeline, wire it into `publish_all.py` and the top-level `publish.py`.
