# format_conversion

Convert course materials between file formats: Markdown ⇄ HTML / PDF / DOCX, plus PDF → text and audio → text.

## Components

| File | Purpose |
|---|---|
| `main.py` | High-level API: `convert_file`, `batch_convert`, `get_supported_formats`. |
| `utils.py` | Per-pair conversion helpers (`convert_markdown_to_pdf`, `convert_markdown_to_docx`, …) and the `_MarkdownHtmlToDocx` HTML walker. |
| `config.py` | `SUPPORTED_CONVERSIONS` map (input format → list of supported output formats). |

## Supported conversions

| From | To |
|---|---|
| `md` / `markdown` | `pdf`, `html`, `docx` |
| `html` | `pdf` |
| `txt` | `pdf`, `html` |
| `pdf` | `txt` |
| `mp3` / `wav` / `m4a` | `txt` |

## DOCX from Markdown

`convert_markdown_to_docx` is the most commonly-exercised path (used for every `questions.md` and `keys-to-success.md`). It preserves headings, tight ordered lists, bullet lists, `**bold**`, `*italic*`, `` `code` ``, blockquotes, and tables. See `AGENTS.md` for the full feature/regression matrix.

## Usage

```python
from src.format_conversion.main import convert_file, batch_convert

convert_file("lesson.md", "docx", "lesson.docx")
output_paths = batch_convert("module-12/", "md", "pdf")
```

## Tests

`software/tests/test_format_conversion_utils.py` and `software/tests/test_format_conversion_main.py` cover both the per-pair helpers and the high-level dispatcher, with content-asserting tests for the DOCX path (lists, headings, emphasis, real module fixtures).
