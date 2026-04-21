# Technical Documentation: Module 13 Nervous System

## Structure

This directory follows the standard `cr-bio` BIOL-8 module layout. Source markdown lives at the module root; rendered outputs are written to `output/` by the publish pipeline.

| Source file | Rendered to | Formats |
|---|---|---|
| `questions.md` | `output/study-guides/module-13-nervous-system-questions.*` | `md`, `pdf`, `docx` |
| `keys-to-success.md` | `output/study-guides/module-13-nervous-system-keys-to-success.*` | `md`, `pdf`, `docx` |

## Processing

No special processing rules apply beyond the standard automated multi-format export pipeline driven by `software/scripts/generate_all_outputs.py` and `publish.py`. After generation, files are flattened into `PUBLISHED/biol-8/homework/`, `PUBLISHED/biol-8/module_keys/`, and `PUBLISHED/biol-8/ALL_FILES/`.

## Conventions

- Tight ordered lists in `questions.md` (no blank lines between numbered items) are supported by the DOCX/PDF/MD pipeline; see `software/src/format_conversion/utils.py::_MarkdownHtmlToDocx`.
- Do not commit anything inside `output/`; it is regenerated on every publish.
