# Output Formats — Technical Documentation

> **Navigation**: [← README](README.md) | [docs/](../README.md) | [AGENTS.md](../AGENTS.md)

## Purpose

This subfolder documents all six output formats produced by the cr-bio
publish pipeline: PDF, DOCX, HTML, Markdown, Text, and Audio (MP3).
Each format has a dedicated spec covering generation pipeline, styling,
usage examples, and troubleshooting.

## File Inventory

| File | Format | Status |
|------|--------|--------|
| [README.md](README.md) | Index + decision tree | — |
| [PDF.md](PDF.md) | `.pdf` via WeasyPrint | Active |
| [DOCX.md](DOCX.md) | `.docx` via python-docx | Active |
| [HTML.md](HTML.md) | `.html` via markdown2 | Opt-in |
| [MARKDOWN.md](MARKDOWN.md) | `.md` copy + rename | Opt-in |
| [TEXT.md](TEXT.md) | `.txt` via markdown strip | Opt-in |
| [AUDIO.md](AUDIO.md) | `.mp3` via local TTS + ffmpeg | Opt-in |
| [COMPARISON.md](COMPARISON.md) | Cross-format matrix | — |

## Configuration

Format toggles live in [`publish.toml`](../../../publish.toml) under
`[publish.formats]`. See [../reference/CONFIG_REFERENCE.md](../reference/CONFIG_REFERENCE.md)
for the full configuration reference.

## Related Documentation

| Document | Description |
|----------|-------------|
| [../AGENTS.md](../AGENTS.md) | Output format API reference |
| [../pipeline/GENERATION_FLOW.md](../pipeline/GENERATION_FLOW.md) | Internal generation mechanics |
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | System architecture |
