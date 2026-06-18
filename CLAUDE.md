# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository. See [software/docs/README.md](software/docs/README.md) for the full documentation map and architecture.

## Project Overview

CR-BIO is the private source and generation repository for College of the Redwoods biology materials. The active Fall 2026 course model is **BIOL-1: General Biology at Pelican Bay** with 16 content modules. Spring 2026 BIOL-1 and BIOL-8 materials are historical snapshots under `archive/spring-2026/` and are not active publish targets.

## Development Commands

All Python commands run from `software/` using `uv` unless noted.

```bash
cd software && uv sync --extra dev
uv run pytest
uv run ruff check .
uv run mypy src
uv run python scripts/validate_repo_contracts.py
```

`publish.py` auto-sets the macOS WeasyPrint runtime path; manual `DYLD_FALLBACK_LIBRARY_PATH` export is only needed for direct low-level experiments.

## Structured Module Source

BIOL-1 module authoring is centered on `course_development/biol-1/course/module-XX-*/module.toml`. This typed manifest is the source of truth for:

- module number, slug, title, and linked lab
- topics and content sequence
- learning objectives and key terms
- learning questions and generated practice quiz items
- module-local assets and deterministic generated SVG concept cards

Generated files include `keys-to-success.md`, `questions.md`, `practice-quiz.md`, and `resources/generated/*`. Edit `module.toml`, then regenerate. Do not hand-edit generated module Markdown as canonical source.

```bash
cd software
uv run python scripts/generate_module_materials.py --course biol-1
uv run python scripts/generate_module_materials.py --course biol-1 --module 13 --dry-run
```

## Publishing

```bash
# From repo root
python publish.py --dry-run
python publish.py --skip-git
python publish.py

# Direct generation from software/
cd software
uv run python scripts/generate_all_outputs.py --course biol-1
uv run python scripts/generate_all_outputs.py --course biol-1 --module 1
uv run python scripts/validate_outputs.py --course all
```

The publish flow regenerates structured module materials before format conversion, then writes tracked artifacts under `PUBLISHED/biol-1/` for subtree publishing to `github.com/docxology/biol-1`.

## Architecture

```text
course_development/biol-1/
  course/
    module-XX-topic/       # module.toml source; generated keys/questions/quiz/assets
    labs/                  # lab-XX_topic.md + dashboards/
    exams/, practice_tests/, quizzes/
  syllabus/
  resources/               # slides and shared assets
  private/                 # instructor-only, not published

archive/spring-2026/       # historical BIOL-1 and BIOL-8 snapshots
PUBLISHED/biol-1/          # generated tracked public subtree
software/src/              # module_content + renderers/converters/publish validation
```

## Conventions

- Python 3.11+, `uv`, Ruff, mypy, pytest.
- Public APIs live in package `main.py`; docs live in package `README.md` and `AGENTS.md`.
- Production code must stay mock-free; tests use real temp files and mark external/slow tests explicitly.
- BIOL-1 active modules do not use `assignments/` folders. Legacy import code may reference old assignment conventions only as archive/import compatibility.
