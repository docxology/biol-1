# AGENTS: `software/scripts`

Thin CLI orchestrators that wrap `software/src/` packages. Scripts contain only argument parsing, path bootstrap, logging, and orchestration; all business logic lives in `src/`. See `software/scripts/README.md` for user-facing usage and run commands.

## Thin-orchestrator contract

A script in this directory may only:

1. Parse CLI arguments (`argparse`).
2. Bootstrap `sys.path` (mandatory before any `from src…` import — see Gotchas).
3. Configure logging.
4. Invoke entry points in `software/src/<pkg>/` and report results.

Business, data, plot, and analysis logic lives in `software/src/` packages, which are importable and covered by `software/tests/`. Never add logic to a script; extend the package and delegate.

Every script must:

- Provide `main()` and an `if __name__ == "__main__": main()` guard.
- Exit `0` on success and non-zero on failure, collecting per-item errors into the summary instead of aborting mid-run.
- Be added to the inventory table below **and** to `scripts/README.md` in the same change.
- If the script belongs to the publish pipeline, be wired into `publish_all.py`.

## Inventory

| Script | Backing package | Entry point | Purpose |
|---|---|---|---|
| `publish_all.py` | `batch_processing`, `publish`, `validation` | `main()` | End-to-end pipeline (generate → publish → validate). |
| `generate_all_outputs.py` | `batch_processing`, `module_content` | `main()` | Generate all output formats for one or all courses. |
| `generate_module_materials.py` | `module_content` | `main()` | Generate Markdown, practice quizzes, and deterministic SVG assets from `module.toml`. |
| `generate_module_renderings.py` | `batch_processing` | `main()` | Run generation for a single module. |
| `generate_module_website.py` | `batch_processing` → `html_website` | `main()` | Build a per-module interactive HTML site. |
| `generate_slide_decks.py` | `slide_deck` | `main()` | Render BIOL-1 slide decks (full + notes HTML sources, PDF) from module manifests. |
| `generate_module_videos.py` | `lecture_create` | `main()` | Build LectureCreate YAML manifests and render lecture videos per module. |
| `generate_syllabus_renderings.py` | `batch_processing` (`process_syllabus`) | `main()` | Render syllabus / schedule documents into `syllabus/output/`. |
| `generate_course_by_date.py` | `course_by_date` | `main()` | Build and validate BIOL-1 dated teaching handoffs from `course_calendar.toml`. |
| `generate_biol1_lab_dashboards.py` | (stdlib; BIOL-1 lab specs) | `main()` | Regenerate exact-stem BIOL-1 lab dashboards from the active lab list. |
| `publish_course.py` | `publish` | `main()` | Copy generated artifacts into `PUBLISHED/<course>/`. |
| `flatten_published.py` | `publish.utils` | `main()` | Move per-module outputs into flat `homework/`, `module_keys/`, … buckets. |
| `validate_outputs.py` | `validation`, `course_by_date`, `lecture_create.validation` | `main()` | Verify expected files exist for every in-scope module. |
| `validate_repo_contracts.py` | `validation.repo_contracts` | `main()` | Validate documentation/repository contracts without rendering artifacts. |
| `renumber_questions.py` | `content_processing` | `main()` | Convert section-based question numbering to continuous. |
| `shuffle_final_exam_mc.py` | `exam_tools` | `main()` | Shuffle final-exam Part A MC options and re-key the answer key. |
| `import_legacy_materials.py` | `legacy_import` | `main()` | Import an older lesson archive into the current module layout. |
| `assemble_practice_test_12.py` | (stdlib; archived BIOL-8 content) | `main()` | Rebuild Spring 2026 `practice-test-12.md` / `_key.md` from PT01–11 slices (`archive/spring-2026/course_development/biol-8/course/practice_tests/`). |
| `utils.py` | (helpers) | n/a | Shared CLI helper (`print_module_not_found`); imported as `scripts.utils`, not runnable. |

## CLI conventions

- Course-scoped publish/generation scripts expose `--course {biol-1, all}` for active courses. Archived BIOL-8 is not a live target.
- Format selection uses `--formats pdf,docx,html,txt,md,mp3` (comma-separated; defaults vary per script).
- Most scripts also accept `--verbose` to enable `INFO`-level logging.
- Exit codes: `0` = success, non-zero = at least one error; per-file errors are collected and reported in the summary even when the run continues.

## Gotchas

- **Path bootstrap before `src` imports.** Every script that imports `from src…` must first run `sys.path.insert(0, str(Path(__file__).parent.parent))` (inserts the `software/` directory). `uv`'s project install masks a missing bootstrap, but plain `python3 scripts/<script>.py` from any other working directory fails with `ModuleNotFoundError: No module named 'src'`. The per-file ruff `E402` ignore for `scripts/*.py` exists precisely because imports follow this bootstrap.
- **Stdlib-only scripts** (`generate_biol1_lab_dashboards.py`, `assemble_practice_test_12.py`) import nothing from `src` and need no bootstrap.
- **`utils.py` is a helper, not a CLI.** Other scripts import it as `scripts.utils`; do not run it directly and do not put business logic in it.
- Run scripts through `uv run python scripts/<script>.py` from `software/` so third-party dependencies resolve from the project environment.
- Logs are written to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log` (git-ignored); see `software/logs/AGENTS.md`.
- `generate_slide_decks.py` is called by `generate_all_outputs.py` after structured module materials are refreshed; `publish_all.py` is the only end-to-end pipeline entry point.
- Video rendering honors `LECTURECREATE_BIN`, `LECTURECREATE_CONFIG`, and `LECTURECREATE_BACKEND` environment overrides; the canonical BIOL-1 config is `software/src/lecture_create/biol-1.yaml`.
