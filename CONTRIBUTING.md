# Contributing to CR-BIO Course Development

This guide covers active Fall 2026 BIOL-1 authoring. Historical BIOL-8 and Spring 2026 materials live under `archive/spring-2026/` and should not be treated as active templates.

## Quick Start

1. Install dependencies: `cd software && uv sync --extra dev`.
2. Edit BIOL-1 source in `course_development/biol-1/`.
3. For module content, edit the module's `module.toml`, not generated Markdown.
4. Regenerate structured module materials: `uv run python scripts/generate_module_materials.py --course biol-1`.
5. Validate locally: `uv run pytest`, `uv run ruff check .`, `uv run mypy src`, and `uv run python scripts/validate_repo_contracts.py`.

## Module Content

Each module folder contains a typed manifest:

```text
module-XX-topic/
├── module.toml           # canonical source
├── keys-to-success.md    # generated from module.toml
├── questions.md          # generated from module.toml
├── practice-quiz.md      # generated from module.toml
├── resources/
│   └── generated/        # deterministic SVG cards + asset docs
├── README.md
└── AGENTS.md
```

A manifest must define module number, slug, title, linked lab, topics, contents, learning objectives, key terms, study tips, learning questions, practice quiz items, and generated SVG specs. Keep practice quiz answers balanced across A-D for the first four questions.

## Labs

BIOL-1 labs live in `course_development/biol-1/course/labs/` and use the standard front matter:

```markdown
# Lab N: Topic

**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay

**Name:** {fill:text} **Date:** {fill:text}

---

## Learning Objectives
```

Use clear instructions, disclose numeric parameters for simulations, and prefer compact tables when repeated trials would otherwise sprawl.

## Practice Quizzes

Per-module practice quiz material is generated as `practice-quiz.md` from `module.toml`. The central `course/quizzes/` folder remains template/ad hoc only unless course policy changes.

## Publishing

```bash
# From repo root
python publish.py --dry-run
python publish.py --skip-git

# From software/ for focused work
uv run python scripts/generate_module_materials.py --course biol-1 --module 13
uv run python scripts/generate_all_outputs.py --course biol-1 --module 13
uv run python scripts/validate_repo_contracts.py
```

Never edit `PUBLISHED/` directly. Edit typed/course source and regenerate.
