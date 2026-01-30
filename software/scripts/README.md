# Scripts

Thin CLI orchestrators for course material generation and publishing.

## Naming Convention

Output files are prefixed with module name for unique identification:

- `module-01-questions.pdf` (not `questions.pdf`)
- `module-01-keys-to-success.mp3` (not `keys-to-success.mp3`)

## Primary Scripts

| Script | Purpose |
|--------|---------|
| `publish_all.py` | **Top-level pipeline** - generate, publish, validate |
| `generate_all_outputs.py` | Generate all outputs for all modules |
| `publish_course.py` | Publish module outputs to PUBLISHED/ |
| `validate_outputs.py` | Validate generated outputs |

## Usage

### Full Publishing Pipeline

```bash
cd software

# Full publish with all formats (~17 min)
uv run python scripts/publish_all.py --clean --verbose

# Skip MP3 for faster iteration (~5 min)
uv run python scripts/publish_all.py --clean --skip-mp3

# PDF-only for quick testing
uv run python scripts/publish_all.py --clean --formats pdf
```

### Individual Scripts

```bash
# Generate outputs
uv run python scripts/generate_all_outputs.py --course biol-1 --module 1

# Publish to PUBLISHED/
uv run python scripts/publish_course.py --course all

# Validate
uv run python scripts/validate_outputs.py --course all
```

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `flatten_published.py` | Flatten PUBLISHED/ directory structure |
| `renumber_questions.py` | Convert section-based to continuous numbering |

## Single-Item Scripts

| Script | Purpose |
|--------|---------|
| `generate_module_renderings.py` | Generate outputs for one module |
| `generate_module_website.py` | Generate website for one module |
| `generate_syllabus_renderings.py` | Generate syllabus outputs |

## Migration Scripts

| Script | Purpose |
|--------|---------|
| `import_legacy_materials.py` | Import from legacy bio_1_2025 format |

## Output Formats

| Format | Description |
|--------|-------------|
| PDF | Print-ready document |
| DOCX | Microsoft Word format |
| HTML | Web page |
| MP3 | Audio narration |
| TXT | Plain text extraction |

## Dependencies

```bash
# macOS system libraries for PDF/DOCX
brew install cairo pango gdk-pixbuf glib
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

## Logging

Logs are written to `software/logs/generation_YYYY-MM-DD_HH-MM-SS.log`.
