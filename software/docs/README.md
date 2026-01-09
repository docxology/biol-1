# Software Documentation

> **Quick Navigation**: [Quick Start](QUICKSTART.md) | [Architecture](ARCHITECTURE.md) | [Orchestration](ORCHESTRATION.md) | [API Reference](../AGENTS.md)

## Overview

Comprehensive documentation for the **cr-bio course management software**. This software automates the generation of educational materials in multiple formats (PDF, MP3, HTML, DOCX, TXT) from Markdown source files.

---

## 📊 Project Statistics

| Metric | Value | Last Updated |
|--------|-------|--------------|
| **Total Tests** | 334 | 2026-01-09 |
| **Pass Rate** | 100% | 2026-01-09 |
| **Code Coverage** | 87% | 2026-01-09 |
| **Modules** | 10 | - |
| **Skipped Tests** | 6 | - |

### Supported Courses
- **BIOL-1**: 17 modules (Spring 2026)
- **BIOL-8**: 3 modules (Spring 2026)

---

## 📚 Documentation Index

### Getting Started
| Document | Description | Audience |
|----------|-------------|----------|
| **[QUICKSTART.md](QUICKSTART.md)** | Installation, setup, quick commands | New users |
| **[../README.md](../README.md)** | Project overview and setup | All users |

### Technical Reference
| Document | Description | Audience |
|----------|-------------|----------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design, module diagrams | Developers |
| **[ORCHESTRATION.md](ORCHESTRATION.md)** | Multi-module workflow patterns | Developers |
| **[AGENTS.md](AGENTS.md)** | Documentation standards | Contributors |
| **[../AGENTS.md](../AGENTS.md)** | API reference (all functions) | Developers |

### Source and Tests
| Document | Description | Audience |
|----------|-------------|----------|
| **[../src/README.md](../src/README.md)** | Source code overview | Developers |
| **[../src/AGENTS.md](../src/AGENTS.md)** | Module-level docs | Developers |
| **[../tests/README.md](../tests/README.md)** | Test suite overview | Contributors |
| **[../tests/AGENTS.md](../tests/AGENTS.md)** | Testing standards | Contributors |

---

## 🔧 Module Reference

### Content Generation (7 modules)

| Module | Purpose | Key Function | Coverage |
|--------|---------|--------------|----------|
| [markdown_to_pdf](../src/markdown_to_pdf/) | Markdown → PDF via WeasyPrint | `render_markdown_to_pdf()` | 92% |
| [text_to_speech](../src/text_to_speech/) | Text → MP3 via gTTS | `generate_speech()` | 97% |
| [speech_to_text](../src/speech_to_text/) | Audio → Text transcription | `transcribe_audio()` | 98% |
| [format_conversion](../src/format_conversion/) | Multi-format conversion | `convert_file()` | 85% |
| [batch_processing](../src/batch_processing/) | Batch module processing | `process_module_by_type()` | 75% |
| [html_website](../src/html_website/) | Interactive HTML websites | `generate_module_website()` | 92% |
| [schedule](../src/schedule/) | Schedule file processing | `process_schedule()` | 93% |

### Course Management (3 modules)

| Module | Purpose | Key Function | Coverage |
|--------|---------|--------------|----------|
| [module_organization](../src/module_organization/) | Create module structures | `create_module_structure()` | 93% |
| [file_validation](../src/file_validation/) | Validate content | `validate_module_files()` | 92% |
| [canvas_integration](../src/canvas_integration/) | Upload to Canvas LMS | `upload_module_to_canvas()` | 73% |

---

## 🗺️ Documentation Map

```
software/
├── README.md              ← Project entry point
├── AGENTS.md              ← API reference (function signatures)
├── docs/
│   ├── README.md          ← YOU ARE HERE
│   ├── QUICKSTART.md      → Installation and quick commands
│   ├── ARCHITECTURE.md    → System design diagrams
│   ├── ORCHESTRATION.md   → Multi-module workflows
│   └── AGENTS.md          → Documentation standards
├── src/
│   ├── README.md          → Source code overview
│   └── AGENTS.md          → Module implementations
├── tests/
│   ├── README.md          → Test suite overview
│   └── AGENTS.md          → Testing standards
└── scripts/
    ├── generate_all_outputs.py   → Generate all course outputs
    └── generate_module_website.py → Generate single module website
```

---

## 🔗 Quick Links

### By Task

| I want to... | Go to... |
|--------------|----------|
| **Install the software** | [QUICKSTART.md#prerequisites](QUICKSTART.md#-prerequisites) |
| **Convert Markdown to PDF** | [QUICKSTART.md#convert-markdown-to-pdf](QUICKSTART.md#convert-markdown-to-pdf) |
| **Generate audio from text** | [QUICKSTART.md#generate-audio](QUICKSTART.md#generate-audio) |
| **Process schedule files** | [ORCHESTRATION.md#schedule-processing-pipeline](ORCHESTRATION.md#3-schedule-processing-pipeline-schedule-processing-pipeline) |
| **Generate HTML website** | [ORCHESTRATION.md#html-website-generation](ORCHESTRATION.md#4-html-website-generation-html-website-generation) |
| **Combine modules in workflows** | [ORCHESTRATION.md](ORCHESTRATION.md) |
| **Understand the architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **Run tests** | [QUICKSTART.md#-running-tests](QUICKSTART.md#-running-tests) |
| **Look up a function** | [../AGENTS.md](../AGENTS.md) |

### By Module

| Module | Quick Start | API | Tests |
|--------|-------------|-----|-------|
| markdown_to_pdf | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#markdown-to-pdf-rendering) | [Tests](../tests/test_markdown_to_pdf_main.py) |
| text_to_speech | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#text-to-speech-generation) | [Tests](../tests/test_text_to_speech_main.py) |
| schedule | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#schedule-processing) | [Tests](../tests/test_schedule_main.py) |
| html_website | [QUICKSTART](QUICKSTART.md) | [API](../AGENTS.md#html-website-generation) | [Tests](../tests/test_html_website_features.py) |
| batch_processing | [ORCHESTRATION](ORCHESTRATION.md) | [API](../AGENTS.md#batch-processing) | [Tests](../tests/test_batch_processing_main.py) |
| format_conversion | [ORCHESTRATION](ORCHESTRATION.md) | [API](../AGENTS.md#format-conversion) | [Tests](../tests/test_format_conversion_utils.py) |

---

## 📋 Documentation Standards

1. **Navigation Headers**: Every doc links to related docs
2. **Consistent Structure**: Standardized sections across all docs
3. **Working Code Examples**: All examples are tested and runnable
4. **Current Statistics**: Test counts and coverage updated regularly
5. **Cross-References**: Links between related content

See [AGENTS.md](AGENTS.md) for complete documentation standards.

---

## 🔄 Version History

| Date | Changes |
|------|---------|
| 2026-01-09 | Updated to 334 tests, 87% coverage, removed bio_1_2025 legacy |
| 2026-01-08 | Enhanced documentation modularity and signposting |
| 2026-01-01 | Initial comprehensive documentation |
