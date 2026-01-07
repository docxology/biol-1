# Source Code

## Overview

This directory contains the source code for all course management software utilities.

## Module Organization

Source code is organized into modular subdirectories, each containing functionality for a specific purpose:

- **markdown_to_pdf/**: Markdown to PDF conversion utilities
- **text_to_speech/**: Text-to-speech generation
- **speech_to_text/**: Speech-to-text transcription
- **format_conversion/**: File format conversion tools (MD, PDF, DOCX, HTML, TXT, Audio)
- **batch_processing/**: Batch process entire modules for multiple format conversions
- **html_website/**: Generate comprehensive HTML websites for modules with audio, text, and interactive quizzes
- **module_organization/**: Automated module structure creation
- **canvas_integration/**: Canvas LMS integration scripts
- **file_validation/**: File and structure validation tools

## Module Orchestration

Modules are designed to work together seamlessly. Example workflows:

### Complete Module Processing Workflow

```python
from src.module_organization.main import create_module_structure
from src.file_validation.main import validate_module_files, get_validation_report
from src.batch_processing.main import generate_module_media
from src.format_conversion.main import convert_file

# 1. Create module structure
module_path = create_module_structure("biol-1", 1)

# 2. Validate module
validation = validate_module_files(module_path)
if validation["valid"]:
    # 3. Generate all media formats
    results = generate_module_media(module_path, "output/")
    print(f"Generated {len(results['pdf_files'])} PDFs")
    print(f"Generated {len(results['audio_files'])} audio files")
```

### Text-to-Speech to Speech-to-Text Round Trip

```python
from src.text_to_speech.main import generate_speech
from src.speech_to_text.main import transcribe_audio

# Generate audio from text
generate_speech("Hello world", "output.mp3")

# Transcribe audio back to text
text = transcribe_audio("output.mp3", "output.txt")
```

### Format Conversion Chain

```python
from src.format_conversion.main import convert_file

# Markdown -> PDF -> Text
convert_file("document.md", "pdf", "document.pdf")
convert_file("document.pdf", "txt", "document.txt")
```

## Code Standards

- Follow Python PEP 8 style guidelines
- Use type hints for function signatures
- Include docstrings for all functions and classes
- Maintain modular, reusable code structure

## Documentation

- **[AGENTS.md](AGENTS.md)**: Function signatures, modules, and code structure documentation
