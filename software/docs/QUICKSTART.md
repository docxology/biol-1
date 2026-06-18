# Quick Start Guide

> **Navigation**: [← README](README.md) | [Architecture](ARCHITECTURE.md) | [Orchestration →](ORCHESTRATION.md) | [Standards](AGENTS.md) | [API Reference](../AGENTS.md)

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
brew install cairo pango gdk-pixbuf libffi glib ffmpeg
```

**Ubuntu/Debian**:

```bash
sudo apt-get install python3-cairo python3-pango libgdk-pixbuf2.0-dev libffi-dev
```

### 3. Install Python Dependencies

```bash
cd software
uv sync --extra dev   # runtime + pytest, black, ruff, mypy (recommended)
# uv sync             # runtime only — insufficient for pytest in this repo
```

### 4. Set Environment Variable (macOS only)

WeasyPrint loads Homebrew Cairo/Pango libraries using `DYLD_FALLBACK_LIBRARY_PATH` (the same variable [`publish.py`](../../publish.py) sets):

```bash
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
```

Add to `~/.zshrc` for persistence:

```bash
echo 'export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"' >> ~/.zshrc
source ~/.zshrc
```

### 5. Verify Installation

```bash
uv run python -c "from weasyprint import HTML; print('✓ WeasyPrint: OK')"
uv run python -c "from src.format_conversion.main import convert_file; print('✓ Format conversion: OK')"
```

---

## Project Configuration

### Configuration Files Overview

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, tool configuration |
| `.python-version` | Python version for uv (3.11) |
| `uv.lock` | Locked dependency versions for reproducibility |
| `.gitignore` | Git exclusion patterns |
| `.cursorrules` | Real Methods Policy for AI assistants |
| `software/run_tests.sh` | macOS-compatible test runner wrapper with fast/default and opt-in full/audio profiles |

### pyproject.toml

Defines project dependencies and tool configuration:

```toml
[project]
requires-python = ">=3.11"
dependencies = ["markdown", "weasyprint", "speechrecognition", "requests", ...]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "black", "mypy", "ruff"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--cov=src", "--cov-report=html", "-v"]
markers = ["requires_internet", "requires_api", "audio", "slow"]
```

### .python-version

Specifies Python 3.11 for uv package manager:

```text
3.11
```

### uv.lock

Auto-generated lock file ensuring reproducible builds. **Never edit manually** - regenerate with:

```bash
uv lock
```

### .cursorrules (Real Methods Policy)

Documents the core development principle: production code uses real implementations, and tests use real files/libraries by default with only documented boundary doubles.

### software/run_tests.sh

Wrapper script for macOS that sets `DYLD_FALLBACK_LIBRARY_PATH` for WeasyPrint (same convention as [`publish.py`](../../publish.py)). The default profile is fast and offline; audio, slow, network, and API tests are opt-in:

```bash
cd software
./run_tests.sh                          # Fast offline gate
./run_tests.sh --fast                   # Same fast offline gate, explicit profile
./run_tests.sh tests/test_imports.py -v # Fast gate scoped to a path
./run_tests.sh --audio                  # Local TTS/audio tests
./run_tests.sh --full                   # Full suite
```

---

## Check Version

```bash
# Check software version
uv run python -c "from src import __version__; print(f'cr-bio-software v{__version__}')"

# Check Python version
python --version

# Check key dependency versions
uv run python -c "import weasyprint; print(f'WeasyPrint: {weasyprint.__version__}')"
say --version 2>/dev/null || true
ffmpeg -version | head -1
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

**Module**: `markdown_to_pdf` (WeasyPrint + system Cairo/Pango; uses `shared` helpers)

```bash
uv run python -c "
from src.markdown_to_pdf.main import render_markdown_to_pdf
render_markdown_to_pdf('input.md', 'output.pdf')
"
```

### Generate Audio from Text {#generate-audio}

**Module**: `text_to_speech` (standalone; on macOS uses local `say` plus `ffmpeg`)

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

The primary entry point is the top-level `publish.py` script with configuration via [`publish.toml`](../../publish.toml). Generation is implemented in **Python** (`software/src/`: WeasyPrint, `python-docx`, `markdown2`, local TTS helpers, etc.); format toggles in the TOML are authoritative.

```bash
# From the repository root (not software/)
cd /path/to/cr-bio

# Full publish pipeline
python publish.py

# Dry run to see what would be generated
python publish.py --dry-run

# Override formats on command line
python publish.py --override-formats pdf,html,md

# Include MP3 audio generation (slower; local TTS/ffmpeg)
python publish.py --override-formats pdf,docx,html,txt,md,mp3
```

After a successful run, root [`publish.py`](../../publish.py) may also build per-course **`ALL_FILES/`** duplicates and perform git operations—see [ORCHESTRATION.md#the-publish-pipeline](ORCHESTRATION.md#the-publish-pipeline).

**Configuration** (`publish.toml`):

| Setting | Description |
|---------|-------------|
| `publish.formats.*` | pdf, docx, html, txt, **md** (normalized copies), mp3 |
| `publish.formats.mp3` | Enable/disable audio generation |
| `publish.clean` | Clear outputs before generation |
| `publish.courses.*.enabled` | Enable/disable specific courses |
| `publish.pipeline.*` | Stages including `strict_dashboards`, `all_files`, `git_push` |

Defaults for `html` / `txt` / `md` change over time—read the repo’s `publish.toml` after pull.

---

## Generation Scripts

### Generate All Course Outputs

```bash
cd software

# Generate all outputs for a course
uv run python scripts/generate_all_outputs.py --course biol-1

# Dry run (preview only)
uv run python scripts/generate_all_outputs.py --course biol-1 --dry-run

# All courses
uv run python scripts/generate_all_outputs.py --course all
```

| Option | Description |
|--------|-------------|
| `--course` | Course: `biol-1`, `biol-8`, or `all` |
| `--module` | Specific module number (optional) |
| `--formats` | Output formats: pdf, mp3, docx, html, txt, **md** (default: all supported) |
| `--dry-run` | Preview without generating files |
| `--skip-clear` | Don't clear existing outputs |
| `--no-website` | Skip website generation |
| `--skip-labs` | Skip lab manual rendering |

### Generate Module Website

```bash
uv run python scripts/generate_module_website.py --course biol-1 --module 1
```

### Generate Syllabus Renderings

```bash
uv run python scripts/generate_syllabus_renderings.py --course biol-1
```

---

## Running Tests

### Run All Tests

```bash
cd software && ./run_tests.sh
```

Or manually:

```bash
DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}" uv run pytest
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

### Verify test count and coverage

Run from `software/`; numbers change over time:

```bash
uv run pytest --collect-only -q
uv run pytest -q --no-cov
uv run pytest --cov=src --cov-report=html tests/
```

---

## Expected output structure

After running `generate_all_outputs.py` for a course module (e.g. `module-12-darwin-evolution/`):

```
module-12-darwin-evolution/
├── questions.md
├── keys-to-success.md
└── output/
    ├── study-guides/
    │   ├── module-12-darwin-evolution-questions.{pdf,docx,html,txt,md,mp3}
    │   └── module-12-darwin-evolution-keys-to-success.{pdf,docx,html,txt,md,mp3}
    └── website/
        └── index.html
```

Which formats appear depends on `publish.toml` / CLI (`--formats`, MP3 optional). Lab manuals render under `course/labs/output/` instead.

> **Lab counting note**: BIOL-8 ships **18 numbered lab protocols** (`lab-01_*` … `lab-18_*`) plus an optional **follow-up** page (`lab-14_microbiology-followup.md`) for reading the microbiology plates after incubation. Validation reports both counts separately, e.g. `Labs (source tree): 19 markdown (18 numbered + 1 supplemental)`. BIOL-1 has **16 numbered primary labs** today; exam-review worksheets live under `review_materials/`.

---

## Troubleshooting

### PDF Generation Fails

**Error**: `OSError: cannot load library 'pangocairo'`

**Solution**:

```bash
# Install dependencies
brew install cairo pango gdk-pixbuf glib

# Set library search path for Homebrew dylibs (same variable as publish.py)
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from the `software` directory:

```bash
cd /path/to/cr-bio/software
uv run python scripts/generate_all_outputs.py
```

### Audio Generation Fails

**Error**: local TTS or `ffmpeg` command fails or times out

**Solution**:

- Confirm `say` is available on macOS and `ffmpeg` is installed
- Set `mp3 = false` in `publish.toml` for routine local/publish gates
- Process smaller batches

### Audio Tests Are Opt-In

**Note**: MP3 generation is intentionally excluded from the fast local test gate.

### WeasyPrint CSS Warnings

**Error**: `WARNING:weasyprint:Ignored property...`

**Solution**: These are cosmetic warnings and can be safely ignored. Output PDFs are still generated correctly.

### Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:

```bash
# Check file ownership
ls -la /path/to/file

# Fix permissions if needed
chmod 644 /path/to/file
```

### Memory Issues with Large Files

**Error**: Process killed or out of memory

**Solution**:

- Process modules one at a time: `--module X`
- Disable audio generation: set `mp3 = false` in `publish.toml`
- Close other applications

---

## Environment Verification Checklist

Run these commands to verify your environment is set up correctly:

```bash
cd /path/to/cr-bio/software

# 1. Python version (should be 3.11+)
python --version

# 2. uv installed
uv --version

# 3. Dependencies synced
uv sync

# 4. WeasyPrint working
uv run python -c "from weasyprint import HTML; print('✓ WeasyPrint OK')"

# 5. Local audio tooling available
say --version 2>/dev/null || true
ffmpeg -version | head -1

# 6. All modules importable
uv run python -c "from src import __version__; print(f'✓ cr-bio v{__version__}')"

# 7. Tests passing (quick check)
uv run pytest tests/ -x -q --tb=no
```

**Expected Output**: All checks should show ✓

---

## Copy-Paste Commands

### Full Course Generation

```bash
# BIOL-1: Generate all outputs
cd software && uv run python scripts/generate_all_outputs.py --course biol-1

# All active courses
cd software && uv run python scripts/generate_all_outputs.py --course all
```

### Single Module Quick Test

```bash
# Generate single module (fast iteration)
cd software && uv run python scripts/generate_module_renderings.py --course biol-1 --module 1

# Generate website for module
cd software && uv run python scripts/generate_module_website.py --course biol-1 --module 1
```

### Full Publish Pipeline (Recommended)

```bash
# From repository root (reads publish.toml for configuration)
python publish.py                          # Full pipeline
python publish.py --dry-run                # Preview without executing
python publish.py --override-formats pdf,docx,md  # Override formats
python publish.py --git-only               # Skip generation, just push
python publish.py --skip-git               # Run pipeline but skip push
```

### Selective Generation

```bash
# Generate specific formats only
cd software && uv run python scripts/generate_all_outputs.py --formats pdf,docx,md

# Generate specific course only
cd software && uv run python scripts/generate_all_outputs.py --course biol-1

# Limit modules for testing
cd software && uv run python scripts/generate_all_outputs.py --course biol-1 --max-module 3
```

### Lab Manual Generation

```bash
# Full course run includes lab manuals unless you pass --skip-labs
cd software && uv run python scripts/generate_all_outputs.py --course biol-1

# Omit lab manuals (faster iteration on modules/syllabus)
cd software && uv run python scripts/generate_all_outputs.py --course biol-1 --skip-labs

# Limit numbered labs rendered (combine with --formats if needed)
cd software && uv run python scripts/generate_all_outputs.py --course biol-1 --max-lab biol-1:5
```

`generate_all_outputs.py` does **not** support `--labs-only` / `--include-labs`; use the Python API in [ORCHESTRATION.md#lab-manual-generation](ORCHESTRATION.md#lab-manual-generation) for single-file renders.

---

## Next Steps

| I want to... | Go to... |
|--------------|----------|
| Run the full publish pipeline | [ORCHESTRATION.md#the-publish-pipeline](ORCHESTRATION.md#the-publish-pipeline) |
| Generate lab manuals | [ORCHESTRATION.md#lab-manual-generation](ORCHESTRATION.md#lab-manual-generation) |
| Combine modules in workflows | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Understand the architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| See all document types | [ARCHITECTURE.md#document-types](ARCHITECTURE.md#document-types) |
| Look up a specific function | [../AGENTS.md](../AGENTS.md) |
| View test documentation | [../tests/README.md](../tests/README.md) |
| Review documentation standards | [AGENTS.md](AGENTS.md) |

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
| `software/run_tests.sh` | Run fast, full, or audio test profiles |
