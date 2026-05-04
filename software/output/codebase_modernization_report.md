# Codebase modernization notes

**Last reviewed:** 2026-05-04

This file records maintenance work on the `software/` tree (real implementations, exception handling, tests). It is not a certificate of “done forever”; rerun checks after substantive changes.

## Policy

The repo follows the **Real Methods Policy** (see [`.cursorrules`](../../.cursorrules)): production code uses real libraries and I/O; tests use real filesystem operations and library calls, not mocks.

## What changed (summary)

- **`batch_processing`**: Many per-format handlers use **`except (OSError, ValueError)`** (or narrower types) so failures surface predictably. **Broad `except Exception` remains in a few orchestration paths** (e.g. whole-module or syllabus runs) where one failure should be logged and recorded without aborting the entire course batch.
- **`legacy_import`**: Remains an optional **real** migration tool under `src/legacy_import/` (not removed).
- **BIOL-1 final exam tooling**: `scripts/shuffle_final_exam_mc.py` parses Part A stems as either `**N.**` (bold) or plain ordered-list `N.` (current `final-exam.md` style) so crosswalk tests stay aligned with authored markdown.

## How to verify

From `software/`:

```bash
uv run pytest --collect-only -q -o addopts=''   # inventory (no coverage)
uv run pytest -q -o addopts=''                 # full pass/fail without coverage
uv run pytest                                  # default run (coverage per pyproject)
uv run ruff check src/ tests/
uv run mypy src/
```

Test and skip counts **change as tests are added**; use `--collect-only` instead of quoting fixed numbers in documentation.

## Related

- [software/README.md](../README.md) — overview and commands
- [software/AGENTS.md](../AGENTS.md) — module index and conventions
