# Manuscript - cr-bio

This directory is a template-format manuscript scaffold for:

**Biology at College of the Redwoods: Course Production System**

A private Biology course source and generation repository for College of the Redwoods, including BIOL-1 source material, generated public-ready outputs, and publishing automation.

## File Inventory

- `config.yaml`
- `preamble.md`
- `references.bib`
- `00_abstract.md`
- `01_introduction.md`
- `02_system_context.md`
- `03_methods.md`
- `04_artifacts_and_evidence.md`
- `05_reproducibility.md`
- `06_limitations_and_next_steps.md`
- `S01_source_surface.md`
- `98_symbols_glossary.md`
- `99_references.md`
- `AGENTS.md`
- `README.md`
- `SYNTAX.md`

## Source Surfaces

| Surface | Role |
|---|---|
| `course_development/` | Source directory to inspect before turning prose into claims. |
| `PUBLISHED/` | Source directory to inspect before turning prose into claims. |
| `archive/` | Source directory to inspect before turning prose into claims. |
| `software/` | Source directory to inspect before turning prose into claims. |
| `scripts/` | Source directory to inspect before turning prose into claims. |

## Verification

From the sibling template checkout, after `link-projects` has synced the sidecar:

```bash
uv run python -m infrastructure.orchestration link-projects
uv run python -m infrastructure.validation.cli markdown projects/working/cr-bio/manuscript/
```

Render only after replacing scaffold prose with project-bound evidence and checking any project-local gates documented in the repository root.
