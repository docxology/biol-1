# Quick Start Guide

> **Navigation**: [← README](README.md) | [Architecture](ARCHITECTURE.md) | [Orchestration →](ORCHESTRATION.md) | [API Reference](../AGENTS.md)

Get started with cr-bio course management software.

---

## 📦 Prerequisites

### 1. Install uv (Python Package Manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install System Dependencies

**macOS (Homebrew)**:

```bash
brew install cairo pango gdk-pixbuf libffi glib
```

**Ubuntu/Debian**:

```bash
sudo apt-get install python3-cairo python3-pango libgdk-pixbuf2.0-dev libffi-dev
```

### 3. Install Python Dependencies

```bash
cd software
uv sync
```

### 4. Set Environment Variable (macOS only)

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

Add to `~/.zshrc` for persistence:

```bash
echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 5. Verify Installation

```bash
uv run python -c "from weasyprint import HTML; print('✓ WeasyPrint: OK')"
uv run python -c "from src.format_conversion.main import convert_file; print('✓ Format conversion: OK')"
```

---

## Using Modules Independently

All modules can be imported and used independently. Each module has a self-contained public API in its `main.py` file.

### Standalone Module Usage

Each module can be used without importing other modules:

```python
# Use markdown_to_pdf independently
from src.markdown_to_pdf.main import render_markdown_to_pdf
render_markdown_to_pdf("input.md", "output.pdf")

# Use text_to_speech independently
from src.text_to_speech.main import generate_speech
generate_speech("Hello world", "output.mp3")

# Use file_validation independently
from src.file_validation.main import validate_module_files
result = validate_module_files("/path/to/module")
```

### Module Import Pattern

All modules follow the same import pattern:

```python
from src.module_name.main import function_name
```

### No Orchestration Required

The quick commands below use single modules. No orchestration or composition is required for basic usage. See [ORCHESTRATION.md](ORCHESTRATION.md) for combining modules.

---

## Quick Commands

### Convert Markdown to PDF {#convert-markdown-to-pdf}

**Module**: `markdown_to_pdf` (standalone, no dependencies)

```bash
uv run python -c "
from src.markdown_to_pdf.main import render_markdown_to_pdf
render_markdown_to_pdf('input.md', 'output.pdf')
"
```

### Generate Audio from Text {#generate-audio}

**Module**: `text_to_speech` (standalone, requires internet for gTTS)

```bash
uv run python -c "
from src.text_to_speech.main import generate_speech
generate_speech('Hello world! This is a test.', 'output.mp3')
"
```

### Process Schedule File

```bash
uv run python -c "
from src.schedule.main import process_schedule
result = process_schedule('Schedule.md', './output', formats=['pdf', 'html', 'txt'])
print(f'Generated {sum(result[\"summary\"].values())} files')
"
```

### Generate HTML Website

```bash
uv run python -c "
from src.html_website.main import generate_module_website
generate_module_website('/path/to/module', './output/website', course_name='BIOL-101')
"
```

### Validate Module Structure

**Module**: `file_validation` (standalone, no dependencies)

```bash
uv run python -c "
from src.file_validation.main import validate_module_files
result = validate_module_files('/path/to/module')
print('Valid:', result['valid'])
if not result['valid']:
    print('Errors:', result.get('errors', []))
"
```

### Convert Between Formats

```bash
uv run python -c "
from src.format_conversion.main import convert_file
convert_file('input.md', 'docx', 'output.docx')
convert_file('input.md', 'html', 'output.html')
"
```

---

## Full Publish Pipeline (Recommended)

The primary entry point is the top-level `publish.py` script with configuration via `publish.toml`:

```bash
# From the repository root (not software/)
cd /path/to/cr-bio

# Full publish pipeline
python publish.py

# Dry run to see what would be generated
python publish.py --dry-run

# Override formats on command line
python publish.py --override-formats pdf,html

# Include MP3 audio generation (slower, ~30s per file)
python publish.py --override-formats pdf,docx,html,txt,mp3
```

**Configuration** (`publish.toml`):

| Setting | Description |
|---------|-------------|
| `publish.formats.mp3` | Enable/disable audio generation |
| `publish.clean` | Clear outputs before generation |
| `publish.courses.*.enabled` | Enable/disable specific courses |
| `publish.pipeline.*` | Toggle pipeline stages |

---

## Generation Scripts

### Generate All Course Outputs

```bash
cd software

# Generate all outputs for a course
uv run python scripts/generate_all_outputs.py --course biol-8

# Dry run (preview only)
uv run python scripts/generate_all_outputs.py --course biol-8 --dry-run

# All courses
uv run python scripts/generate_all_outputs.py --course all
```

| Option | Description |
|--------|-------------|
| `--course` | Course: `biol-1`, `biol-8`, or `all` |
| `--module` | Specific module number (optional) |
| `--formats` | Output formats: pdf, html, docx, mp3 |
| `--dry-run` | Preview without generating files |
| `--skip-clear` | Don't clear existing outputs |
| `--no-website` | Skip website generation |

### Generate Module Website

```bash
uv run python scripts/generate_module_website.py /path/to/module
```

### Generate Syllabus Renderings

```bash
uv run python scripts/generate_syllabus_renderings.py /path/to/syllabus.md
```

---

## Running Tests

### Run All Tests

```bash
./run_tests.sh
```

Or manually:

```bash
DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH" uv run pytest
```

### Run with Coverage

```bash
uv run pytest --cov=src --cov-report=html tests/
# View report: open htmlcov/index.html
```

### Run Specific Tests

```bash
# Single file
uv run pytest tests/test_schedule_main.py -v

# Single test
uv run pytest tests/test_schedule_main.py::TestProcessSchedule::test_process_schedule_pdf_format -v
```

### Current Statistics

- **Tests**: 414 passed, 6 skipped
- **Coverage**: 74% overall (measure with `uv run pytest --cov=src --cov-report=html`)

---

## Expected Output Structure

After running `generate_all_outputs.py`:

```
module-1/
├── output/
│   ├── assignments/
│   │   ├── assignment-1.pdf
│   │   ├── assignment-1.mp3
│   │   ├── assignment-1.docx
│   │   ├── assignment-1.html
│   │   └── assignment-1.txt
│   ├── lecture-content/
│   │   ├── lecture.pdf
│   │   ├── lecture.mp3
│   │   └── lecture.docx
│   ├── study-guides/
│   │   └── study-guide.pdf
│   └── website/
│       └── index.html
```

---

## Troubleshooting

### PDF Generation Fails

**Error**: `OSError: cannot load library 'pangocairo'`

**Solution**:

```bash
# Install dependencies
brew install cairo pango gdk-pixbuf glib

# Set library path
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from the `software` directory:

```bash
cd /path/to/cr-bio/software
uv run python scripts/generate_all_outputs.py
```

### Audio Generation Fails

**Error**: `gTTSError: 429 (Too Many Requests)`

**Solution**:

- Wait a few minutes and retry
- Use `--skip-audio` flag if available
- Process smaller batches

### Audio Generation Requires Internet

**Note**: gTTS requires an active internet connection to generate audio files.

---

## Next Steps

| I want to... | Go to... |
|--------------|----------|
| Combine multiple modules in workflows | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Understand the system architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Look up a specific function | [../AGENTS.md](../AGENTS.md) |
| View all test documentation | [../tests/README.md](../tests/README.md) |
| Contribute to documentation | [AGENTS.md](AGENTS.md) |

---

## Quick Reference Card

| Task | Function |
|------|----------|
| Markdown → PDF | `render_markdown_to_pdf(input, output)` |
| Text → Audio | `generate_speech(text, output)` |
| Audio → Text | `transcribe_audio(input, output)` |
| Any → Any | `convert_file(input, format, output)` |
| Process schedule | `process_schedule(path, output_dir, formats)` |
| Generate website | `generate_module_website(module_path, output_dir)` |
| Validate module | `validate_module_files(module_path)` |
| Batch process | `process_module_by_type(module_path, output_dir)` |

| Script | Purpose |
|--------|---------|
| `generate_all_outputs.py` | Generate all course outputs |
| `generate_module_website.py` | Single module website |
| `run_tests.sh` | Run test suite |
