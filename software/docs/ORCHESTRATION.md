# Module Orchestration Guide

## Overview

This guide demonstrates how to orchestrate multiple software modules to accomplish complex workflows for course material management.

## Common Orchestration Patterns

### 1. Complete Module Lifecycle

Create, validate, and process a module:

```python
from src.module_organization.main import create_module_structure
from src.file_validation.main import validate_module_files, get_validation_report
from src.batch_processing.main import generate_module_media

# Create module
module_path = create_module_structure("biol-1", 1)

# Validate before processing
validation = validate_module_files(module_path)
if validation["valid"]:
    # Generate all media formats
    results = generate_module_media(module_path, "output/")
    print(f"Generated {len(results['pdf_files'])} PDFs")
    print(f"Generated {len(results['audio_files'])} audio files")
```

### 2. Format Conversion Chains

Convert files through multiple formats:

```python
from src.format_conversion.main import convert_file, get_supported_formats

# Check available conversions
formats = get_supported_formats()
print(f"Can convert MD to: {formats['md']}")

# Chain: Markdown -> PDF -> Text
convert_file("document.md", "pdf", "document.pdf")
convert_file("document.pdf", "txt", "document.txt")
```

### 3. Text-to-Speech Round Trip

Generate audio and transcribe back:

```python
from src.text_to_speech.main import generate_speech
from src.speech_to_text.main import transcribe_audio

# Generate audio from text
generate_speech("Course content here", "lecture.mp3")

# Transcribe audio back to text
transcribed = transcribe_audio("lecture.mp3", "lecture.txt")
```

### 4. Validation-Driven Processing

Only process modules that pass validation:

```python
from src.file_validation.main import (
    validate_module_files,
    get_validation_report,
    validate_course_structure,
)
from src.batch_processing.main import process_module_to_pdf

# Validate entire course
course_validation = validate_course_structure("biol-1")
if course_validation["valid"]:
    # Process each valid module
    for module_info in course_validation["modules"]:
        if module_info["validation"]["valid"]:
            process_module_to_pdf(module_info["module_path"], "output/")
```

### 5. Statistics-Based Decisions

Use module statistics to make processing decisions:

```python
from src.module_organization.main import get_module_statistics
from src.batch_processing.main import generate_module_media

stats = get_module_statistics("biol-1/course/module-1")

# Only process if module has content
if stats["total_files"] > 2:  # More than just README/AGENTS
    if stats["assignment_count"] > 0:
        # Process assignments
        generate_module_media("biol-1/course/module-1", "output/")
```

### 6. Error Handling in Orchestration

Handle errors gracefully across modules:

```python
from src.batch_processing.main import generate_module_media
from src.file_validation.main import validate_module_files

try:
    # Validate first
    validation = validate_module_files(module_path)
    if not validation["valid"]:
        print(f"Validation issues: {validation['missing_files']}")
        return
    
    # Process with error collection
    results = generate_module_media(module_path, output_dir)
    
    # Check for errors
    if results["errors"]:
        print(f"Processing errors: {results['errors']}")
    else:
        print("All processing completed successfully")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except OSError as e:
    print(f"File system error: {e}")
```

## Best Practices

### 1. Always Validate Before Processing

```python
# Good: Validate first
validation = validate_module_files(module_path)
if validation["valid"]:
    process_module(module_path)

# Bad: Process without validation
process_module(module_path)  # May fail on invalid modules
```

### 2. Use Statistics for Planning

```python
# Check module state before processing
stats = get_module_statistics(module_path)
if stats["total_files"] == 0:
    print("Module has no content to process")
    return
```

### 3. Handle Errors Gracefully

```python
# Collect errors, don't fail immediately
results = generate_module_media(module_path, output_dir)
if results["errors"]:
    # Log errors but continue
    for error in results["errors"]:
        log_error(error)
```

### 4. Chain Operations Efficiently

```python
# Efficient: Check formats before converting
formats = get_supported_formats()
if "docx" in formats.get("md", []):
    convert_file("file.md", "docx", "file.docx")
```

## Module Dependencies

Understanding module dependencies helps with orchestration:

- **batch_processing** depends on: markdown_to_pdf, text_to_speech, speech_to_text, format_conversion
- **format_conversion** depends on: markdown_to_pdf, speech_to_text
- **file_validation** is independent (can be used anywhere)
- **module_organization** is independent (creates structure)
- **canvas_integration** depends on: file_validation (for validation)

## Example: Complete Course Setup

```python
from src.module_organization.main import create_module_structure, list_course_modules
from src.file_validation.main import validate_course_structure
from src.batch_processing.main import generate_module_media

# Setup course
course_path = "biol-1"

# Create modules
for i in range(1, 4):
    create_module_structure(course_path, i)

# Validate course
course_validation = validate_course_structure(course_path)
if course_validation["valid"]:
    # Process all modules
    modules = list_course_modules(course_path)
    for module_path in modules:
        generate_module_media(module_path, f"output/{Path(module_path).name}")
```

## Testing Orchestration

See `tests/test_orchestration.py` for comprehensive orchestration test examples.
