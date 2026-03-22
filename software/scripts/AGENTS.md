# Technical Documentation: Scripts

## Overview

CLI orchestration scripts following the **thin orchestrator** pattern. All business logic resides in `src/` modules; scripts handle CLI argument parsing and result reporting only.

## Script Inventory

| Script | Primary Module(s) | Purpose |
|--------|-------------------|---------|
| `publish_all.py` | `batch_processing`, `publish`, `validation` | Top-level pipeline (generate → publish → validate) |
| `generate_all_outputs.py` | `batch_processing` | Generate all course outputs |
| `generate_module_renderings.py` | `batch_processing` | Single module processing |
| `generate_module_website.py` | `html_website` | Website generation |
| `generate_syllabus_renderings.py` | `schedule`, `batch_processing` | Syllabus processing |
| `publish_course.py` | `publish` | Publish to PUBLISHED/ |
| `validate_outputs.py` | `validation` | Validate generated outputs |
| `flatten_published.py` | `publish.utils` | Flatten directory structure |
| `renumber_questions.py` | `content_processing` | Question renumbering |
| `import_legacy_materials.py` | `legacy_import` | Import legacy format |
| `utils.py` | (standalone) | Shared CLI helper functions |
| `remediate_docs.py` | (standalone) | Batch generate missing README.md/AGENTS.md |

## Thin Orchestrator Pattern

Scripts do NOT contain business logic. They:

1. Parse command-line arguments (`argparse`)
2. Call module functions from `src/`
3. Report results to stdout/log

```
Script (CLI parsing) → src/ Module (business logic) → Output
```

## Dependencies

All scripts import from `src/` modules. Runtime dependencies are managed via `pyproject.toml` and `uv sync`.

### Internal Dependencies

- `utils.py`: Provides `print_module_not_found()` helper used by generation scripts
- Most scripts import from `src.batch_processing`, `src.publish`, or `src.validation`

## Execution

All scripts should be run with `uv run` from the `software/` directory:

```bash
uv run python scripts/publish_all.py --clean --verbose
```

## Logging

Pipeline scripts write timestamped logs to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log`.

## Interface Contract

Each script follows consistent CLI conventions:

- `--course`: Target course (`biol-1`, `biol-8`, or `all`)
- `--dry-run`: Preview without executing
- `--verbose`: Detailed output
- `--formats`: Comma-separated output formats

See `scripts/README.md` for full CLI option tables per script.
