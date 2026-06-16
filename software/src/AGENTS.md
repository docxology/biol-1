# `software/src/` — Source Code Technical Documentation

This file is the **index** for the per-package documentation under `software/src/`. Each package owns its own `AGENTS.md` with current function signatures, dependencies, and downstream callers; this index avoids duplicating those signatures so they cannot drift.

## Package layout

Every package follows the same shape:

```text
<package_name>/
├── __init__.py     # Re-exports public API
├── main.py         # Public functions (the only entry point other packages import)
├── utils.py        # Internal helpers (treat as private)
├── config.py       # Constants / configuration (when applicable)
├── README.md       # Overview + usage
└── AGENTS.md       # Function signatures, dependencies, downstream callers
```

## Packages

| Package | Layer | Purpose | Docs |
|---|---|---|---|
| `shared` | 0 | Cross-cutting file and runtime helpers. | [`shared/AGENTS.md`](shared/AGENTS.md) |
| `module_organization` | 0 | Create and inspect course module folders. | [`module_organization/AGENTS.md`](module_organization/AGENTS.md) |
| `file_validation` | 0 | Per-file naming and structure checks. | [`file_validation/AGENTS.md`](file_validation/AGENTS.md) |
| `validation` | 0 | Output completeness checks for published courses. | [`validation/AGENTS.md`](validation/AGENTS.md) |
| `publish` | 0 | Copy generated artifacts into `PUBLISHED/`. | [`publish/AGENTS.md`](publish/AGENTS.md) |
| `legacy_import` | 0 | One-off importers for older lesson archives. | [`legacy_import/AGENTS.md`](legacy_import/AGENTS.md) |
| `content_processing` | 0 | Text transformations (question renumbering, normalization). | [`content_processing/AGENTS.md`](content_processing/AGENTS.md) |
| `markdown_to_pdf` | 1 | Markdown → PDF via WeasyPrint. | [`markdown_to_pdf/AGENTS.md`](markdown_to_pdf/AGENTS.md) |
| `text_to_speech` | 1 | Text → audio via local TTS and ffmpeg. | [`text_to_speech/AGENTS.md`](text_to_speech/AGENTS.md) |
| `speech_to_text` | 1 | Audio → text. | [`speech_to_text/AGENTS.md`](speech_to_text/AGENTS.md) |
| `lab_manual` | 1 | Lab manual rendering with fillable directives. | [`lab_manual/AGENTS.md`](lab_manual/AGENTS.md) |
| `format_conversion` | 2 | Cross-format dispatch (md ⇄ html ⇄ pdf ⇄ docx; pdf → txt; audio → txt). | [`format_conversion/AGENTS.md`](format_conversion/AGENTS.md) |
| `batch_processing` | 3 | Per-module fan-out across formats. | [`batch_processing/AGENTS.md`](batch_processing/AGENTS.md) |
| `schedule` | 3 | Schedule markdown → multi-format outputs. | [`schedule/AGENTS.md`](schedule/AGENTS.md) |
| `html_website` | 3 | Per-module HTML site with quizzes/audio. | [`html_website/AGENTS.md`](html_website/AGENTS.md) |
| `canvas_integration` | 4 | Canvas LMS upload and structure sync. | [`canvas_integration/AGENTS.md`](canvas_integration/AGENTS.md) |

Layer numbers indicate the dependency hierarchy used in `software/AGENTS.md`. A package may only import from packages at strictly lower layers (or `shared`).

## Interface contracts

When packages interact, they follow these conventions:

- **Public API lives in `main.py`.** Tests and other packages should import from there or from the package's `__init__.py`. `utils.py` is treated as private.
- **Type hints preferred for public APIs.** The current mypy profile permits legacy untyped internals while keeping source checks enabled.
- **Result dicts have stable shapes.** Where functions return summaries, the keys are documented in the package's `AGENTS.md` (typically `{"summary": dict, "errors": list[str], …}`).
- **Errors:** missing input → `FileNotFoundError`; bad input → `ValueError`; failed conversions → `OSError`. Network calls handle their own retries and surface meaningful messages.
- **Side effects are explicit.** File-writing functions take an explicit `output_path`/`output_dir`; nothing writes to surprising locations.

## Real-implementation policy

The repo runs against real libraries, local tools, and real files. Production code must remain mock-free. Tests use temp directories, real markdown samples, and real renderer calls by default; limited test doubles are allowed only for external services or expensive orchestration seams. External services such as Canvas and Google Speech are exercised only in explicitly marked tests; the default wrapper excludes `requires_internet`, `requires_api`, `audio`, and `slow`.

## Adding a new package

1. Create `software/src/<package>/` with `__init__.py`, `main.py`, `utils.py`, optional `config.py`.
2. Add `README.md` (purpose + usage) and `AGENTS.md` (signatures + dependencies).
3. Keep imports flowing only from lower layers; if you find yourself reaching back up, refactor instead.
4. Add tests under `software/tests/test_<package>_*.py`. Prefer content-asserting tests over file-existence checks.
5. Add the package to the table above and to `software/AGENTS.md`.
