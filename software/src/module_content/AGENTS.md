# Technical Documentation: `module_content`

## Overview

Typed BIOL-1 module-content loader, validator, and renderer. `module.toml` is the canonical Fall 2026 module source and generates student-facing Markdown plus deterministic high-design local SVG visual assets before the normal publish converters run.

## Public API

- `load_module_content(module_dir: Path | str) -> ModuleContent` - parse and validate `module.toml`.
- `validate_module_content(module: ModuleContent, module_dir: Path | None = None) -> list[str]` - return contract issues without writing files.
- `render_module_materials(module_dir: Path | str, dry_run: bool = False) -> dict[str, object]` - render generated module files.
- `render_course_module_materials(course_root: Path | str, module_filter: int | None = None, dry_run: bool = False) -> dict[str, object]` - render all module manifests for a course.
- `describe_course_module_materials(course_root: Path | str, module_filter: int | None = None) -> str` - dry-run report.

## Visualization contract

Each BIOL-1 module must have exactly three explicit generated-image specs: `concept-map`, `process-model`, and `retrieval-card`. The output names must be `resources/generated/module-NN-{kind}.svg`.

- `concept-map` requires `central_claim`, at least three `nodes`, and non-dangling `edges`.
- `process-model` requires at least three ordered `stages`, plus `inputs`, `outputs`, and `feedbacks`.
- `retrieval-card` requires at least four `prompts`, at least three `terms`, and a `lab_connection`.

The renderer wraps text, uses stable high-design palettes, embeds SVG accessibility metadata, and never calls external image services.

## Other contracts

- Module markdown and generated SVGs are regenerated; edit `module.toml` instead of generated outputs.
- AI image prompts may be stored as metadata, but this package does not call external image services.
- BIOL-1 does not use active `assignments/` module folders. Legacy import tooling may mention assignments only as archive/import compatibility.
