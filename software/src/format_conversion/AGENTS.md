# Format Conversion Technical Documentation

## Overview

File format conversion utilities supporting conversions between Markdown, PDF, HTML, DOCX, TXT, and audio formats.

## Module Purpose

Convert course materials between different file formats, supporting batch conversions and format chain operations.

## Function Signatures

### Main Functions

**File**: `src/format_conversion/main.py`

#### `convert_file(input_path: str, output_format: str, output_path: str) -> None`

Convert a file from one format to another.

**Args**:
- `input_path`: Path to input file
- `output_format`: Target format (e.g., "pdf", "docx")
- `output_path`: Path for output file

**Raises**:
- `ValueError`: If conversion is not supported
- `FileNotFoundError`: If input file doesn't exist
- `OSError`: If conversion fails

**Supported Conversions**:
- `md`/`markdown` -> `pdf`, `html`, `docx`
- `html` -> `pdf`
- `txt` -> `pdf`, `html`
- `pdf` -> `txt`
- `mp3`/`wav`/`m4a` -> `txt`

**Dependencies**:
- `markdown_to_pdf.main.render_markdown_to_pdf` (for md->pdf)
- Various utility conversion functions

#### `batch_convert(directory: str, input_format: str, output_format: str) -> List[str]`

Batch convert files in a directory.

**Args**:
- `directory`: Directory containing files to convert
- `input_format`: Source file format
- `output_format`: Target file format

**Returns**:
- List of output file paths

**Raises**:
- `ValueError`: If directory doesn't exist or conversion is not supported
- `OSError`: If conversion fails for any file

#### `get_supported_formats() -> Dict[str, list]`

Get list of supported file formats.

**Returns**:
- Dictionary mapping input formats to supported output formats

#### `get_conversion_path(input_path: str, output_format: str) -> str`

Generate output path for file conversion.

**Args**:
- `input_path`: Path to input file
- `output_format`: Target format (without dot)

**Returns**:
- Output file path with new extension

### Utility Functions

**File**: `src/format_conversion/utils.py`

#### `convert_markdown_to_pdf(input_file: Path, output_file: Path) -> None`

Convert Markdown file to PDF.

**Dependencies**:
- `markdown_to_pdf.main.render_markdown_to_pdf`

#### `convert_markdown_to_html(input_file: Path, output_file: Path) -> None`

Convert Markdown file to HTML.

#### `convert_markdown_to_docx(input_file: Path, output_file: Path) -> None`

Convert Markdown file to DOCX. Internally renders the markdown to HTML via `markdown_to_pdf.utils.markdown_to_html`, then walks the HTML with `_MarkdownHtmlToDocx` to emit a `python-docx` document.

**Supported markdown constructs:**
- Headings `#` … `######` → DOCX heading styles (level 1–6).
- Paragraphs (`<p>`) → standard paragraphs.
- Ordered lists (numbered `1. … 2. …`) — including tight lists with no blank lines between items — emit numbered paragraphs (`1. `, `2. `, …).
- Unordered lists (`- … * …`) emit bullet paragraphs (`• `).
- Inline emphasis: `**bold**` / `__bold__` → bold runs; `*em*` / `_em_` → italic runs; `` `code` `` → Courier New runs; `<u>` → underlined runs.
- Blockquotes (`> …`) → "Quote" style if available, otherwise plain paragraph.
- Fenced code blocks (`` ``` ``) → plain paragraph with each line preserved.
- Tables → DOCX tables (basic header + rows).

**Why this matters:** earlier versions only flushed paragraphs on `</p>` / `</hN>`, so tight ordered lists silently dropped every list item. See test `test_convert_markdown_to_docx_tight_ordered_list_preserves_items` for a regression guard.

### `_MarkdownHtmlToDocx(HTMLParser)`

Internal HTML-walker class driving `convert_markdown_to_docx`. Maintains:

- `_block_stack` — currently open block tags (`p`, `h1`–`h6`, `li`, `blockquote`, `pre`); a paragraph is flushed whenever a block tag closes.
- `_list_stack` — `[{"type": "ol"|"ul", "index": int}, …]`; supports nested lists and provides `_list_prefix()` for tight-list numbering.
- `_fmt` — counters for `bold`/`italic`/`code`/`underline` so nested emphasis stays correct.
- `_runs` — buffer of `(text, fmt_snapshot)` tuples for the current block, flushed by `_flush_block(tag)`.
- `_in_table` / `_table_rows` / `_current_row` / `_current_cell` — per-table buffers used by `_emit_table()`.

Public methods inherited from `HTMLParser`: `feed`, `close`. Add a final call to `finalize()` to flush any unterminated trailing block.

#### `convert_html_to_pdf(input_file: Path, output_file: Path) -> None`

Convert HTML file to PDF.

#### `convert_text_to_pdf(input_file: Path, output_file: Path) -> None`

Convert text file to PDF.

#### `convert_text_to_html(input_file: Path, output_file: Path) -> None`

Convert text file to HTML.

#### `convert_pdf_to_text(input_file: Path, output_file: Path) -> None`

Extract text from PDF file.

#### `convert_audio_to_text(input_file: Path, output_file: Path) -> None`

Transcribe audio file to text.

**Dependencies**:
- `speech_to_text.main.transcribe_audio`

#### `convert_docx_to_markdown(input_path: Path) -> str`

Convert DOCX file to Markdown format.

**Args**:
- `input_path`: Path to input DOCX file

**Returns**:
- Markdown content as string

**Features**:
- Preserves headings (H1-H6) based on paragraph styles
- Converts bold and italic formatting to Markdown
- Handles tables and converts to Markdown table format
- Preserves paragraph structure

**Dependencies**:
- `python-docx` library

#### `get_file_extension(file_path: Path) -> str`

Get file extension as a lowercase string **without** the leading dot (e.g. `"pdf"`, `"md"`).

#### `get_output_path(input_path: Path, output_format: str, output_dir: Optional[Path] = None) -> Path`

Generate an output file path by replacing the suffix on `input_path` with `output_format`. If `output_dir` is `None`, the file stays in `input_path.parent`.

> Note: `ensure_output_directory` is **not** defined in this module. It lives in `src.shared.file_utils` and is imported by `format_conversion.main` for use inside `convert_file()`.

## Configuration

**File**: `src/format_conversion/config.py`

- `SUPPORTED_CONVERSIONS`: Dictionary mapping input formats to supported output formats:
  - `md`/`markdown`: `["pdf", "html", "docx"]`
  - `html`: `["pdf"]`
  - `txt`: `["pdf", "html"]`
  - `pdf`: `["txt"]`
  - `mp3`/`wav`/`m4a`: `["txt"]`

- `CONVERSION_HANDLERS`: Dictionary mapping conversion keys to handler modules (legacy, not actively used)

## Integration Points

### Dependencies on Other Modules

- **markdown_to_pdf**: Markdown to PDF conversion
- **speech_to_text**: Audio to text transcription

### Used By

- **batch_processing**: Format conversions for module processing
- Test orchestration workflows
- Module processing scripts

## Error Handling

- Validates input file existence
- Validates conversion support before attempting
- Continues batch processing after individual file errors
- Raises appropriate exceptions for unsupported conversions

## Conversion Process

1. Validates input file exists
2. Checks conversion is supported
3. Ensures output directory exists
4. Routes to appropriate conversion handler
5. Performs conversion
6. Handles errors gracefully
