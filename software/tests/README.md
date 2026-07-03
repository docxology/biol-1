# Test Files

## Overview

This directory contains the test suite for the CR-BIO software. Tests use **real
implementations** (real files, real WeasyPrint/PDF rendering, real HTTP through a
local stub) — no mocking frameworks. Test structure mirrors the source packages
in `src/`. The suite is **42 test files** covering 662 fast offline tests plus a
handful of opt-in audio/network tests.

## Running Tests

Run everything from the `software/` directory.

### Recommended: the wrapper script

`run_tests.sh` sets the macOS WeasyPrint library path and selects a sensible
marker set:

```bash
./run_tests.sh            # fast offline gate (default) — excludes audio/slow/internet/api
./run_tests.sh --fast     # same as default, explicit
./run_tests.sh --full     # every test, including audio/network (needs deps + connectivity)
./run_tests.sh --audio    # only the local TTS/audio tests
./run_tests.sh --fast tests/test_markdown_to_pdf_main.py -v   # extra flags pass through
```

### Direct pytest

```bash
uv sync --extra dev                         # install runtime + dev deps first
uv run pytest -m "not audio and not slow and not requires_internet and not requires_api"
uv run pytest tests/test_format_conversion_main.py -v        # one file
uv run pytest --cov=src --cov-report=html                    # coverage → htmlcov/
```

> ### ⚠️ Troubleshooting: `ModuleNotFoundError` for `markdown` / `speech_recognition`
>
> `markdown`, `speechrecognition`, `weasyprint`, etc. are **runtime**
> dependencies (declared in `[project].dependencies`), so `uv sync` alone
> installs them. If a collection run still fails with
> `ModuleNotFoundError: No module named 'markdown'`, a **foreign virtualenv is
> shadowing this project's `.venv`** — e.g. an inherited `VIRTUAL_ENV` pointing
> at a parent workspace, or `uv run` resolving a parent `pyproject.toml`.
> Two reliable fixes:
>
> ```bash
> # A) clear the leaked venv so uv resolves this project
> env -u VIRTUAL_ENV uv run pytest -m "not audio and not slow and not requires_internet and not requires_api"
>
> # B) call this project's interpreter directly (most robust)
> .venv/bin/python -m pytest -m "not audio and not slow and not requires_internet and not requires_api"
> ```
>
> `.venv/bin/python -m pytest` is the environment-independent path and is worth
> using in CI or any nested-checkout layout.

### WeasyPrint on macOS

PDF rendering needs the Homebrew libraries on the loader path. `run_tests.sh`
and `publish.py` set this automatically; for a raw `pytest` invocation export it
yourself:

```bash
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
```

## Test Organization

Tests mirror the source packages in `src/`. Recompute the live inventory and
coverage after any suite change:

```bash
uv run pytest --collect-only -q          # test count
uv run pytest --cov=src --cov-report=term-missing
```

### Rendering & output tests

These exercise the multi-format rendering pipeline (Markdown → PDF/HTML/DOCX/TXT/
audio, labs, slides). Pair each with its format contract under
[`../docs/`](../docs/).

| Test File | Renders / Validates | Format doc |
|-----------|---------------------|------------|
| `test_markdown_to_pdf_main.py` | Markdown → PDF via WeasyPrint | [OUTPUT_PDF.md](../docs/OUTPUT_PDF.md) |
| `test_format_conversion_main.py` / `test_format_conversion_utils.py` | Multi-format conversion orchestration (PDF/DOCX/HTML/TXT/MD) | [OUTPUT_DOCX.md](../docs/OUTPUT_DOCX.md) |
| `test_html_website_features.py` / `test_html_website_utils.py` | Self-contained interactive module website | [OUTPUT_HTML.md](../docs/OUTPUT_HTML.md) |
| `test_lab_manual_main.py` / `test_lab_manual_utils.py` | Lab-manual directives → rendered labs + dashboards | [LAB_FORMAT.md](../docs/LAB_FORMAT.md), [DASHBOARD_FORMAT.md](../docs/DASHBOARD_FORMAT.md) |
| `test_slide_deck.py` | Structured module → classroom + notes slide decks | [ARCHITECTURE.md](../docs/ARCHITECTURE.md) |
| `test_text_to_speech_main.py` / `test_speech_to_text_main.py` | Audio narration (opt-in, `audio`/`slow` markers) | [OUTPUT_AUDIO.md](../docs/OUTPUT_AUDIO.md) |
| `test_module_content.py` | Typed `module.toml` → keys/questions/practice-quiz/SVG generation + validation | [COURSE_STRUCTURE.md](../docs/COURSE_STRUCTURE.md) |

### Content, structure & module tests

| Test File | Coverage For |
|-----------|--------------|
| `test_content_processing_main.py` / `_utils.py` / `_utils_extended.py` | Content parsing and transformation |
| `test_module_organization_main.py` / `_main_extended.py` / `_utils.py` | Module directory structure creation |
| `test_module_content.py` | Structured `module.toml` loading, validation, rendering |
| `test_schedule_main.py` / `test_schedule_utils.py` | Course schedule processing |
| `test_shared_course_config.py` | Shared course configuration |
| `test_shuffle_final_exam_mc.py` | Deterministic multiple-choice shuffling for the final exam |

### Pipeline, publish & integration tests

| Test File | Coverage For |
|-----------|--------------|
| `test_batch_processing_main.py` / `_orchestration.py` / `_utils.py` | Batch generation across modules |
| `test_publish_main.py` / `test_publish_utils.py` | Publish pipeline (generate → PUBLISHED/ → subtree) |
| `test_repo_contracts.py` | Repository invariants (e.g. PUBLISHED/ tracking for subtree publishing) |
| `test_orchestration.py` | Module orchestration patterns |
| `test_integration.py` | Cross-module end-to-end workflows |
| `test_cli.py` | CLI argument parsing |
| `test_canvas_integration_main.py` / `_utils.py` | Canvas LMS integration (real HTTP via local stub) |
| `test_legacy_import_main.py` / `_main_extended.py` / `_utils.py` | Legacy material import/compatibility |
| `test_file_validation_main.py` / `test_file_validation_utils.py` | File validation |
| `test_validation_main.py` / `test_validation_utils.py` | Output/content validation |

### Verification tests

| Test File | Purpose |
|-----------|---------|
| `test_imports.py` | Every package imports cleanly |
| `test_dependencies.py` | Required dependencies are installed and importable |
| `test_real_implementations.py` | Confirms real (non-mock) implementations are wired up |

## Test Markers

| Marker | Description | In fast gate? |
|--------|-------------|---------------|
| `requires_internet` | Needs a live internet connection | No |
| `requires_api` | Needs external API credentials (e.g. Canvas sandbox) | No |
| `audio` | Invokes local audio/TTS tools (`say`, `ffmpeg`, gTTS) | No |
| `slow` | Intentionally slower than the local gate | No |

The fast gate is `-m "not audio and not slow and not requires_internet and not requires_api"`.

## Test Standards

- pytest framework, AAA pattern (Arrange, Act, Assert).
- **No mocking frameworks** — use real implementations by default; a test double
  is allowed only at an external-service or expensive-orchestration boundary and
  must be made explicit in the test.
- Isolated and deterministic: temp dirs for I/O, fixed seeds, no shared state.
- Coverage floor (dev target): overall > 70%, critical paths > 90%. Coverage
  reflects only the subset exercised in a given run.

## Fixtures

Shared fixtures live in `conftest.py`:

- `temp_dir` — temporary directory for test files
- `sample_markdown_file` — sample Markdown for rendering tests
- `sample_text_file` — sample text file
- `sample_module_structure` — sample module directory tree
- `sample_curriculum_files` — one sample per curriculum type

`canvas_stub_server.py` provides a threaded local `HTTPServer` so Canvas upload
tests run against real HTTP without hitting the live API.

## Documentation

- **[AGENTS.md](AGENTS.md)** — test structure, processes, and the real-methods policy.
- **[../docs/](../docs/README.md)** — architecture and per-format rendering contracts.
