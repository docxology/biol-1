# Module Orchestration Guide

> **Navigation**: [← Quick Start](QUICKSTART.md) | [README](README.md) | [Architecture](ARCHITECTURE.md) | [API Reference](../AGENTS.md)

This guide demonstrates how to combine multiple modules for complex workflows.

---

## Modular Composition

### Core Principle

Each module in the system can be used independently. Orchestration is the act of composing multiple independent modules to create more complex workflows. This composition is explicit and documented.

### Composition Patterns

#### Sequential Composition

Modules are called in sequence, where the output of one module feeds into another:

```python
# Sequential: Validate → Process → Generate
from src.file_validation.main import validate_module_files
from src.batch_processing.main import process_module_by_type

validation = validate_module_files(module_path)
if validation["valid"]:
    results = process_module_by_type(module_path, output_dir)
```

#### Parallel Composition

Multiple modules process different inputs or aspects simultaneously:

```python
# Parallel: Generate multiple formats at once
from src.markdown_to_pdf.main import render_markdown_to_pdf
from src.format_conversion.main import convert_file
from src.text_to_speech.main import generate_speech

# All can run independently
render_markdown_to_pdf("file.md", "file.pdf")
convert_file("file.md", "html", "file.html")
generate_speech("text", "file.mp3")
```

#### Conditional Composition

Modules are invoked based on conditions or validation results:

```python
# Conditional: Only process if validation passes
from src.file_validation.main import validate_module_files
from src.batch_processing.main import process_module_by_type

validation = validate_module_files(module_path)
if validation["valid"]:
    process_module_by_type(module_path, output_dir)
else:
    print("Skipping: validation failed")
```

### Module Swapping and Extension

Because modules have clear interfaces, they can be swapped or extended:

- **Swapping**: Replace one module with another that has the same interface
- **Extending**: Add new modules to a workflow without modifying existing ones
- **Testing**: Test modules independently before composing them

### Required Modules

Each orchestration pattern documents which modules are required:

- **Required**: Modules that must be present for the pattern to work
- **Optional**: Modules that enhance the pattern but aren't required
- **Dependencies**: External dependencies (libraries, system tools)

---

## Orchestration Patterns

### 1. Complete Module Lifecycle

Create, validate, and generate all outputs for a module:

**Required Modules**: `module_organization`, `file_validation`, `batch_processing`, `html_website`

**Module Dependencies**:
- `batch_processing` depends on: `markdown_to_pdf`, `text_to_speech`, `format_conversion`
- `html_website` depends on: `batch_processing`, `format_conversion`

**Can be used independently**: Each module can be used separately; this pattern composes them.

```python
from src.module_organization.main import create_module_structure
from src.file_validation.main import validate_module_files
from src.batch_processing.main import generate_module_media, process_module_by_type
from src.html_website.main import generate_module_website

# Step 1: Create module structure
module_path = create_module_structure(
    course_path="/path/to/biol-8",
    module_number=4
)
print(f"Created: {module_path}")

# Step 2: Add content files manually or programmatically
# ...

# Step 3: Validate module structure
validation = validate_module_files(module_path)
if not validation["valid"]:
    print(f"Validation errors: {validation['errors']}")
    raise ValueError("Module validation failed")

# Step 4: Generate all format outputs
results = process_module_by_type(module_path, f"{module_path}/output")
print(f"Generated: {results['summary']}")

# Step 5: Generate interactive website
website = generate_module_website(module_path, f"{module_path}/output/website")
print(f"Website: {website}")
```

---

### 2. Format Conversion Chain

Convert a single Markdown file to multiple formats:

**Required Modules**: `markdown_to_pdf`, `format_conversion`, `text_to_speech`

**Module Dependencies**: None (all are Layer 1 core modules)

**Can be used independently**: Each conversion can be done separately; this pattern shows combining them.

```python
from src.markdown_to_pdf.main import render_markdown_to_pdf
from src.format_conversion.main import convert_file
from src.text_to_speech.main import generate_speech
from src.text_to_speech.utils import extract_text_from_markdown
from pathlib import Path

input_file = "/path/to/content.md"
output_dir = "/path/to/output"

# Markdown → PDF
render_markdown_to_pdf(input_file, f"{output_dir}/content.pdf")

# Markdown → HTML
convert_file(input_file, "html", f"{output_dir}/content.html")

# Markdown → DOCX
convert_file(input_file, "docx", f"{output_dir}/content.docx")

# Markdown → Plain Text
content = Path(input_file).read_text()
text = extract_text_from_markdown(content)
Path(f"{output_dir}/content.txt").write_text(text)

# Text → Audio (MP3)
generate_speech(text, f"{output_dir}/content.mp3")

print(f"Generated 5 files in {output_dir}")
```

---

### 3. Schedule Processing Pipeline

Process schedule files into multiple formats:

```python
from src.schedule.main import process_schedule, batch_process_schedules

# Single schedule file → all formats
results = process_schedule(
    schedule_path="/path/to/biol-8/syllabus/Schedule.md",
    output_dir="/path/to/biol-8/syllabus/output",
    formats=["pdf", "html", "docx", "txt", "mp3"]
)

print(f"Generated files:")
for fmt, count in results["summary"].items():
    print(f"  {fmt}: {count}")

if results["errors"]:
    print(f"Errors: {results['errors']}")

# Batch process all schedules in a directory
batch_results = batch_process_schedules(
    directory="/path/to/all-schedules",
    output_dir="/path/to/output",
    formats=["pdf", "html"]
)

print(f"Processed {len(batch_results['processed_files'])} schedule files")
```

---

### 4. HTML Website Generation

Generate interactive HTML websites with embedded audio and quizzes:

```python
from src.html_website.main import generate_module_website
from src.batch_processing.main import process_module_by_type

module_path = "/path/to/biol-8/course/module-1"

# Step 1: Generate all format outputs (including audio)
results = process_module_by_type(
    module_path,
    output_dir=f"{module_path}/output"
)
print(f"Generated: {sum(results['summary'].values())} files")

# Step 2: Generate website with embedded content
website_path = generate_module_website(
    module_path,
    output_dir=f"{module_path}/output/website",
    course_name="BIOL-8"
)
print(f"Website: {website_path}")

# Website includes:
# - Dark mode toggle
# - Collapsible sections
# - Embedded audio players
# - Interactive quizzes (from questions/ folder)
# - Mobile responsive design
```

---

### 5. Validation-Driven Processing

Only process modules that pass validation:

```python
from src.file_validation.main import validate_module_files
from src.batch_processing.main import process_module_by_type
from pathlib import Path

course_path = Path("/path/to/biol-8/course")
results = {"processed": [], "skipped": [], "errors": []}

for module_path in sorted(course_path.glob("module-*")):
    # Validate first
    validation = validate_module_files(str(module_path))
    
    if validation["valid"]:
        try:
            output = process_module_by_type(
                str(module_path),
                f"{module_path}/output"
            )
            results["processed"].append(module_path.name)
            print(f"✓ {module_path.name}: {sum(output['summary'].values())} files")
        except Exception as e:
            results["errors"].append((module_path.name, str(e)))
            print(f"✗ {module_path.name}: {e}")
    else:
        results["skipped"].append((module_path.name, validation.get("errors", [])))
        print(f"⊘ {module_path.name}: Skipped (validation failed)")

print(f"\nSummary: {len(results['processed'])} processed, {len(results['skipped'])} skipped")
```

---

### 6. Text-to-Speech Round Trip

Generate audio and transcribe back for verification:

```python
from src.text_to_speech.main import generate_speech
from src.speech_to_text.main import transcribe_audio
import tempfile
from pathlib import Path

original_text = "This is a sample lecture about cell biology."

# Generate audio
with tempfile.TemporaryDirectory() as tmpdir:
    audio_file = Path(tmpdir) / "lecture.mp3"
    text_file = Path(tmpdir) / "transcription.txt"
    
    # Text → Audio
    generate_speech(original_text, str(audio_file))
    print(f"Audio generated: {audio_file.stat().st_size} bytes")
    
    # Audio → Text
    transcribed = transcribe_audio(str(audio_file), str(text_file))
    print(f"Transcribed: {transcribed}")
    
    # Compare
    print(f"\nOriginal:    {original_text}")
    print(f"Transcribed: {text_file.read_text()}")
```

---

### 7. Course-Wide Generation

Generate outputs for an entire course:

```python
from pathlib import Path
from src.batch_processing.main import (
    process_module_by_type,
    process_syllabus,
    clear_all_outputs
)
from src.html_website.main import generate_module_website

course_path = Path("/path/to/biol-8")

# Step 1: Clear existing outputs
clear_results = clear_all_outputs(course_path)
print(f"Cleared {clear_results['total_files_removed']} files")

# Step 2: Process all modules
for module_path in sorted((course_path / "course").glob("module-*")):
    output_dir = module_path / "output"
    
    # Generate all formats
    results = process_module_by_type(str(module_path), str(output_dir))
    print(f"{module_path.name}: {sum(results['summary'].values())} files")
    
    # Generate website
    generate_module_website(str(module_path), str(output_dir / "website"))

# Step 3: Process syllabus
syllabus_path = course_path / "syllabus"
if syllabus_path.exists():
    results = process_syllabus(str(syllabus_path), str(syllabus_path / "output"))
    print(f"Syllabus: {sum(results['summary'].values())} files")
```

---

## Best Practices

### Error Handling Pattern

```python
def safe_process_module(module_path: str, output_dir: str) -> dict:
    """Process module with comprehensive error handling."""
    try:
        results = process_module_by_type(module_path, output_dir)
        return {
            "success": True,
            "results": results,
            "errors": results.get("errors", [])
        }
    except FileNotFoundError as e:
        return {"success": False, "error": f"Path not found: {e}"}
    except ValueError as e:
        return {"success": False, "error": f"Invalid input: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}
```

### Validate-First Pattern

```python
def process_with_validation(module_path: str, output_dir: str) -> dict:
    """Always validate before processing."""
    from src.file_validation.main import validate_module_files
    
    validation = validate_module_files(module_path)
    if not validation["valid"]:
        return {
            "success": False,
            "validation_errors": validation.get("errors", []),
            "missing_files": validation.get("missing_files", [])
        }
    
    return safe_process_module(module_path, output_dir)
```

### Progress Reporting Pattern

```python
def process_with_progress(course_path: str) -> None:
    """Process course with progress updates."""
    from pathlib import Path
    
    modules = list(Path(course_path).glob("course/module-*"))
    total = len(modules)
    
    for i, module in enumerate(sorted(modules), 1):
        print(f"[{i}/{total}] Processing {module.name}...")
        result = safe_process_module(str(module), f"{module}/output")
        status = "✓" if result["success"] else "✗"
        print(f"  {status} {result.get('error', 'Complete')}")
```

---

## Module Dependency Graph

```mermaid
graph TD
    subgraph core[Core]
        M2P["markdown_to_pdf"]
        TTS["text_to_speech"]
        STT["speech_to_text"]
    end
    
    subgraph format[Format]
        FC["format_conversion"]
    end
    
    subgraph orchestration[Orchestration]
        BP["batch_processing"]
        HW["html_website"]
        SCH["schedule"]
    end
    
    subgraph management[Management]
        FV["file_validation"]
        CI["canvas_integration"]
    end
    
    M2P --> FC
    TTS --> FC
    
    FC --> BP
    FC --> SCH
    
    BP --> HW
    
    FV --> BP
    FV --> CI
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| PDF generation fails | Missing WeasyPrint deps | `brew install cairo pango gdk-pixbuf glib` |
| Audio generation fails | gTTS rate limit | Wait a few minutes, process smaller batches |
| Module not found | Wrong directory | Run from `software/` directory |
| Validation errors | Missing files | Check required files in module structure |
| Website missing audio | Audio not generated first | Run `process_module_by_type` before `generate_module_website` |

---

## Module Isolation

### Testing Modules Independently

Each module can be tested in isolation without requiring other modules:

```python
# Test markdown_to_pdf independently
def test_markdown_to_pdf_standalone():
    from src.markdown_to_pdf.main import render_markdown_to_pdf
    render_markdown_to_pdf("test.md", "test.pdf")
    assert Path("test.pdf").exists()

# Test file_validation independently
def test_file_validation_standalone():
    from src.file_validation.main import validate_module_files
    result = validate_module_files("/path/to/module")
    assert isinstance(result, dict)
    assert "valid" in result
```

### Integration Testing

When testing module interactions, use real implementations (no mocks):

```python
# Integration test: validation + processing
def test_validation_then_processing():
    from src.file_validation.main import validate_module_files
    from src.batch_processing.main import process_module_by_type
    
    # Both modules use real implementations
    validation = validate_module_files(module_path)
    if validation["valid"]:
        results = process_module_by_type(module_path, output_dir)
        assert results["summary"]["pdf"] > 0
```

### Module Boundary Testing

Test that modules maintain their boundaries:

```python
# Verify module doesn't access internal implementation of another
def test_module_boundaries():
    # Should only import from main.py, not utils.py
    from src.batch_processing.main import process_module_by_type
    # This should work without importing utils directly
    result = process_module_by_type(module_path, output_dir)
    assert result is not None
```

### Testing Patterns

1. **Unit Tests**: Test each module's functions independently
2. **Integration Tests**: Test module interactions with real implementations
3. **Boundary Tests**: Verify modules don't break encapsulation
4. **Composition Tests**: Test orchestration patterns with real modules

See [../tests/README.md](../tests/README.md) for test organization and [../tests/AGENTS.md](../tests/AGENTS.md) for testing standards.

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Basic setup and commands |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design diagrams |
| [../AGENTS.md](../AGENTS.md) | Complete API reference |
| [../tests/README.md](../tests/README.md) | Test suite documentation |
