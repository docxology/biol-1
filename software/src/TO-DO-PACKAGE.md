# TO-DO-PACKAGE: `cr-bio-software` (`software/src`)

> **Navigation**: [← src/README.md](README.md) | [software/README.md](../README.md) | [software/AGENTS.md](../AGENTS.md)
>
> **Package**: `cr-bio-software` · **Current version**: `0.1.0` · **Date**: 2026-02-23
>
> **Scope**: Package-level engineering roadmap for all 15 modules under `software/src/`.  
> This is *not* a course-content to-do; it concerns the Python software package only.

---

## Versioning Policy

| Bump type | Criteria |
|-----------|----------|
| **Patch** (`0.x.y → 0.x.y+1`) | Bug fixes, test additions, doc corrections — no API change |
| **Minor** (`0.x.0 → 0.x+1.0`) | New public function / module / config key; backward-compatible |
| **Major** (`0.x → 1.0`) | Requires ≥90% test coverage, mypy strict-clean, full API stability, CI green |

---

## Current State (v0.1.0 baseline — 2026-02-23)

| Metric | Value |
|--------|-------|
| Modules | 15 across Layers 0–4 |
| Tests | 609 passed, 6 skipped |
| Coverage | 81% |
| Formats | PDF, DOCX, HTML, TXT, MD, MP3 |
| Features shipped | Selective Rendering, 6-stage pipeline, Lab dashboards, HTML websites with interactive quiz |
| Known gaps | mypy not enforced in CI, coverage < 90%, `canvas_integration` requires live API, `speech_to_text` lacks offline fallback |

---

## v0.1.x — Patch Series: Hardening (no API changes)

> **Graduation criterion**: all patches pass; coverage ≥ 83%; zero regressions.

### v0.1.1 — Test & Logging Hygiene

- [ ] Replace all bare `print()` calls in `batch_processing`, `speech_to_text`, `markdown_to_pdf` with `logging` calls
- [ ] Add `conftest.py` fixture for isolated `tmp_path` usage across all test modules
- [ ] Add missing tests for `validate_published_directory` edge cases (missing course dir, partial publish)
- [ ] Pin and document all `pyproject.toml` dependency lower bounds with rationale comments
- [ ] Fix skipped test root cause: document each of the 6 skipped tests with `@pytest.mark.skip(reason="…")`

### v0.1.2 — Type Safety Pass

- [ ] Run `mypy --strict` against all 15 modules; fix all errors in Layers 0–2
- [ ] Add `py.typed` marker file to `src/` to signal PEP 561 compliance
- [ ] Fix Any-typed return values in `batch_processing/main.py` (`generate_module_media`, `process_module_by_type`)
- [ ] Annotate `publish/main.py::publish_course` `publish_root` arg as `Optional[str]`

### v0.1.3 — Coverage Push to 85%

- [ ] Identify and fill gaps in `format_conversion` (conversion error paths)
- [ ] Add tests for `module_organization` edge cases: zero-module course, non-sequential module numbers
- [ ] Add tests for `html_website` quiz-rendering logic (matching, true/false branches)
- [ ] Add tests for `schedule` batch processing with malformed Markdown
- [ ] Achieve ≥ 85% total coverage (currently 81%)

---

## v0.2.0 — Minor: Offline & Resilience Layer

> **Graduation criterion**: all v0.1.x completed; coverage ≥ 85%; new features have ≥ 90% per-module coverage.

### New Public Functions

| Module | New Function | Purpose |
|--------|-------------|---------|
| `speech_to_text` | `transcribe_audio_offline(audio_path, model="tiny")` | Whisper-based local fallback when network unavailable |
| `format_conversion` | `convert_markdown_to_html(input_path, output_path)` | Direct MD→HTML shortcut (currently indirect via batch) |
| `validation` | `validate_published_directory(path)` | Alias for `validate_published` with cleaner name (public API) |
| `batch_processing` | `get_processing_status(repo_root)` | Returns per-course progress dict for dashboard/CI use |

### Infrastructure

- [ ] Add `offline` optional dependency group to `pyproject.toml` (`openai-whisper`, `torch`) gated by `[offline]` extra
- [ ] Add `canvas_integration` mock-mode flag (`dry_run=True`) so tests don't require live API
- [ ] Implement structured logging to `software/logs/` with rotating file handler in `batch_processing`
- [ ] Add `__version__` attribute to `src/__init__.py` sourced from `pyproject.toml`

---

## v0.3.0 — Minor: Multi-Course & Scheduling API

> **Graduation criterion**: v0.2.0 complete; both BIOL-1 and BIOL-8 pass full validation pipeline end-to-end.

### New Public Functions

| Module | New Function | Purpose |
|--------|-------------|---------|
| `schedule` | `export_schedule_to_ical(schedule_path, output_path)` | `.ics` calendar export for student import |
| `batch_processing` | `process_all_courses(repo_root, formats, max_module)` | Top-level orchestrator across all enabled courses |
| `module_organization` | `rename_module(course_path, old_num, new_num)` | Safe renumbering of a module and all its files |
| `content_processing` | `extract_learning_objectives(module_path)` | Parse `## Learning Objectives` blocks → structured list |

### Infrastructure

- [ ] Extend `publish.toml` schema to support per-format toggle at module granularity
- [ ] Add `schedule` test coverage for `.ics` export (RFC 5545 compliance)
- [ ] Document `process_all_courses` in `software/docs/ORCHESTRATION.md`

---

## v0.4.0 — Minor: Canvas LMS Full Integration

> **Graduation criterion**: v0.3.0 complete; `canvas_integration` has ≥ 90% coverage with `dry_run` mode.

### New Public Functions

| Module | New Function | Purpose |
|--------|-------------|---------|
| `canvas_integration` | `publish_course_to_canvas(course_path, course_id, api_key)` | End-to-end: validate → batch-generate → upload |
| `canvas_integration` | `sync_all_modules(course_path, course_id, api_key)` | Delta-sync: only upload changed files |
| `canvas_integration` | `get_canvas_course_status(course_id, api_key)` | Fetch current Canvas module/folder inventory |

### Infrastructure

- [ ] Add VCR/cassette-style HTTP mocking to `test_canvas_integration_main.py` (replace live calls)
- [ ] Add retry logic with exponential back-off to `canvas_integration/utils.py::make_canvas_request`
- [ ] Document Canvas API key setup in `software/docs/QUICKSTART.md`

---

## v0.5.0 — Minor: Reporting & Metrics API

> **Graduation criterion**: v0.4.0 complete; coverage ≥ 88%.

### New Public Functions

| Module | New Function | Purpose |
|--------|-------------|---------|
| `validation` | `generate_html_report(course_name, output_path)` | Human-readable HTML validation report |
| `batch_processing` | `generate_processing_manifest(repo_root, output_path)` | JSON manifest of all generated files with hashes |
| `content_processing` | `build_course_glossary(course_path, output_path)` | Aggregate glossary from all modules |

### Infrastructure

- [ ] Add GitHub Actions CI workflow (`.github/workflows/test.yml`): run `pytest` on push/PR
- [ ] Add coverage badge to `software/README.md`
- [ ] Integrate `ruff` linting step in CI

---

## v1.0.0 — Stable Release: Full API Stability

> **Graduation criteria** (all must be met):
>
> - [ ] Coverage ≥ 90% across all 15 modules
> - [ ] `mypy --strict` passes with zero errors across all modules
> - [ ] CI (GitHub Actions) green on Python 3.11 and 3.12
> - [ ] All public APIs documented with full docstrings + examples
> - [ ] `CHANGELOG.md` populated from v0.1.0 through v1.0.0
> - [ ] `software/docs/API.md` auto-generated from docstrings (e.g. via `pydoc-markdown`)
> - [ ] `canvas_integration` tested with dry-run mode (100% module coverage)
> - [ ] `speech_to_text` offline mode functional and tested
> - [ ] No open critical issues in GitHub Issues

### Final Structural Milestones

- [ ] Freeze and document the public API surface: only functions in `main.py` are guaranteed stable
- [ ] Add `BREAKING_CHANGES.md` policy for future v2.x
- [ ] Publish package metadata to confirm `hatchling` build produces installable wheel
- [ ] Add `software/docs/CHANGELOG.md` with semantic versioning entries from v0.1.0

---

## Module-Level Gap Summary

| Module | Layer | Known Gap | Target Version |
|--------|-------|-----------|---------------|
| `speech_to_text` | 1 | No offline fallback; print() calls | v0.2.0 |
| `canvas_integration` | 4 | Live API needed for tests; no retry | v0.4.0 |
| `format_conversion` | 2 | Missing error-path tests | v0.1.3 |
| `html_website` | 3 | Quiz matching validation is placeholder | v0.1.3 |
| `batch_processing` | 3 | print() calls; no course-level status API | v0.2.0 |
| `schedule` | 3 | No calendar export | v0.3.0 |
| `module_organization` | 0 | No rename/renumber utility | v0.3.0 |
| `content_processing` | 0 | No learning-objective extractor | v0.3.0 |
| `validation` | 0 | `validate_published_directory` naming inconsistency | v0.2.0 |
| `markdown_to_pdf` | 1 | print() calls in batch loop | v0.1.1 |

---

## Completed (v0.1.0)

- [x] 15-module layered architecture (Layers 0–4) with clean public interfaces
- [x] 609 tests at 81% coverage across all modules
- [x] 6-stage publish pipeline (Clean → Generate → Publish → Extras → Flatten → Validate)
- [x] Selective Rendering Boundaries (`max_module`, `max_lab`) in pipeline and validation
- [x] 6 output formats: PDF, DOCX, HTML, TXT, MD, MP3
- [x] Interactive HTML module websites with quiz engine
- [x] Lab dashboard HTML generation for BIOL-8
- [x] Canvas LMS upload (basic, requires live API)
- [x] `publish.toml`-driven configuration for per-course, per-format control
- [x] Consistent module structure: `__init__.py`, `main.py`, `utils.py`, `config.py`, `AGENTS.md`
