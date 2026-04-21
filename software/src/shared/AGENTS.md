# Technical Documentation: `src/shared`

## Purpose

Small, dependency-free helpers shared across `src/` modules. Lives at the bottom of the dependency graph: `src/shared` imports nothing from sibling packages, so any other module may safely import from here.

## Module: `file_utils`

```python
def ensure_output_directory(output_path: Path) -> None
```
Create the directory that should contain `output_path`. If `output_path` has a file suffix (e.g. `.pdf`), creates `output_path.parent`; otherwise creates `output_path` itself. Idempotent (`exist_ok=True`).

```python
def read_markdown_file(file_path: Path) -> str
```
Read a UTF-8 markdown file. Raises `FileNotFoundError(f"Markdown file not found: {file_path}")` if missing. Returns the file content as a string.

```python
def find_files(directory: Path, patterns: list[str]) -> list[Path]
```
Recursive glob (`rglob`) over multiple patterns. Returns a sorted, deduped-by-order `list[Path]`. Note: identical paths matching more than one pattern will appear once per match — callers that need uniqueness should wrap with `sorted(set(...))`.

## Downstream callers

`format_conversion`, `text_to_speech`, `speech_to_text`, `markdown_to_pdf`, `lab_manual`, `html_website`, `batch_processing`, and `schedule` all import from `src.shared.file_utils`. Tests in `software/tests/` exercise these helpers indirectly through their callers.

## Conventions

- Add new helpers here only when at least two `src/` modules need them.
- Keep this package free of third-party imports; only `pathlib`/`typing`/stdlib.
- Type annotations required (`disallow_untyped_defs = true` in `pyproject.toml`).
