# Source Code

## Overview

Source code for course management software utilities.

## Modular Design Principles

Each module follows these principles for maximum modularity:

### Self-Contained Modules

Each module directory contains all code, configuration, and logic needed for its purpose:
- `main.py`: Public API functions (imported by users and other modules)
- `utils.py`: Internal helper functions (private to module)
- `config.py`: Constants and configuration
- `__init__.py`: Exports public functions from `main.py`

### Clear Boundaries

- **Public Interface**: Only functions in `main.py` should be imported by other modules
- **Internal Implementation**: Functions in `utils.py` are private and not imported externally
- **Configuration**: `config.py` exposes constants but not implementation details

### Minimal Dependencies

Modules are organized in layers to minimize inter-module dependencies:
- **Layer 0**: Independent modules (no dependencies)
- **Layer 1**: Core modules (depend only on external libraries)
- **Layer 2+**: Higher layers (depend only on lower layers)

### Module Independence

All modules can be used independently. Even modules that depend on others can be used directly if their dependencies are satisfied:

```python
# Use any module independently
from src.markdown_to_pdf.main import render_markdown_to_pdf
from src.file_validation.main import validate_module_files
```

### Composable Design

Modules can be combined in various ways:
- Sequential: Output of one feeds into another
- Parallel: Multiple modules process different inputs
- Conditional: Modules invoked based on conditions

See [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for detailed architecture and [../docs/ORCHESTRATION.md](../docs/ORCHESTRATION.md) for composition patterns.

## Module Organization

Source code is organized into modular subdirectories, each containing functionality for a specific purpose:

- **markdown_to_pdf/**: Markdown to PDF conversion (standalone, Layer 1)
- **text_to_speech/**: Text-to-speech generation (standalone, Layer 1)
- **speech_to_text/**: Speech-to-text transcription (standalone, Layer 1)
- **format_conversion/**: File format conversion tools (Layer 2, depends on core)
- **batch_processing/**: Batch process entire modules (Layer 3, composes multiple modules)
- **html_website/**: Generate HTML websites (Layer 3, composes multiple modules)
- **schedule/**: Schedule file processing (Layer 3, composes multiple modules)
- **module_organization/**: Automated module structure creation (standalone, Layer 0)
- **canvas_integration/**: Canvas LMS integration (Layer 4, uses validation)
- **file_validation/**: File and structure validation (standalone, Layer 0)
- **publish/**: Export course materials (standalone, Layer 0)

## Module Boundaries

Each module maintains clear boundaries:

- **What it does**: Primary responsibility and core functionality
- **What it doesn't do**: Responsibilities handled by other modules
- **Dependencies**: Explicit list of required modules or libraries
- **Interface**: Public API contract documented in `AGENTS.md`

See each module's `AGENTS.md` for detailed boundaries and dependencies.

## Module Orchestration

Modules can be used independently or composed together. Example workflows:

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
- Use real implementations (no mocks or stubs)

## Documentation

- **[AGENTS.md](AGENTS.md)**: Function signatures, modules, and code structure documentation
