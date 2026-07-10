# Interface Contracts

> **Navigation**: [← README](README.md) | [Layers](LAYERS.md) | [Modular Design](MODULAR_DESIGN.md) | [../AGENTS.md](../AGENTS.md)

Documented contracts between packages — how they interact, what they
guarantee, and what side effects they have.

---

## Public API Convention

**Public API lives in `main.py`.** Tests and other packages import from
`main.py` or the package's `__init__.py`. `utils.py` is treated as private.

```python
# Correct — import from main
from src.markdown_to_pdf.main import render_markdown_to_pdf

# Correct — import from package
from src.markdown_to_pdf import render_markdown_to_pdf

# Wrong — importing from utils (private)
from src.markdown_to_pdf.utils import html_to_pdf  # DON'T DO THIS
```

---

## Return Value Conventions

Functions that return summaries use consistent dict shapes:

| Context | Keys |
|---------|------|
| Batch processing | `summary` (format counts), `errors` (list), `by_type` or `by_format` |
| Publishing | `course`, `modules_published`, `total_files`, `modules`, `errors` |
| Validation | `valid`, `issues`, `modules_checked`, `modules_valid` |
| Module organization | `module_number`, `total_files`, `has_readme`, `is_valid` |

---

## Error Handling Conventions

| Error type | When raised | Example |
|------------|-------------|---------|
| `FileNotFoundError` | Input file doesn't exist | Missing module path |
| `ValueError` | Invalid input argument | Non-existent course, bad template name |
| `OSError` | Conversion/rendering failure | WeasyPrint can't load library |
| `ModuleContentError` | Invalid module.toml | Missing required manifest field |

- Batch functions **collect errors** in a list and continue processing
- Individual functions **raise** on failure
- Error messages include the file path that caused the issue

---

## Side Effect Rules

- **File-writing functions** take an explicit `output_path` / `output_dir`
- **No hidden writes**: Nothing writes to surprising locations
- **Directory creation**: Functions create output directories as needed
- **No external calls** unless explicitly documented (Canvas API, TTS)

---

## Type Hint Convention

All public API functions have complete type annotations. The codebase
passes `mypy --strict` with zero errors.

```python
def render_markdown_to_pdf(
    input_path: str,
    output_path: str,
    css_content: Optional[str] = None,
    pdf_options: Optional[Dict[str, Any]] = None,
) -> None:
```

---

## Result Dict Shapes

### batch_processing

```python
{
    "by_type": {"study-guides": [...], "lab-protocols": [...]},
    "summary": {"pdf": 16, "docx": 16, "md": 16},
    "errors": ["file.md: conversion failed: ..."],
}
```

### publish

```python
{
    "course": "biol-1",
    "modules_published": 16,
    "syllabus_files": 6,
    "total_files": 48,
    "modules": [{"name": "module-01-...", "files": 3}],
    "errors": [],
}
```

### validation

```python
{
    "valid": True,
    "formats_validated": ["pdf", "docx", "md"],
    "modules_checked": 16,
    "modules_valid": 16,
    "modules": [...],
    "issues": [],
}
```

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [MODULAR_DESIGN.md](MODULAR_DESIGN.md) | Design principles |
| [LAYERS.md](LAYERS.md) | Layer architecture |
| [../../src/AGENTS.md](../../src/AGENTS.md) | Package index |
| [../AGENTS.md](../AGENTS.md) | API reference |
