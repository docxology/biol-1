# Test Files

## Overview

This directory contains test files for validating software functionality. Test structure mirrors the source code organization in `src/`.

## Test Statistics

- **612 tests collected** (verify with `uv run pytest --collect-only`)
- Coverage measured via `uv run pytest --cov=src --cov-report=html`

## Test Organization

Tests are organized to mirror the source code structure:

### Module Tests

| Test File | Coverage For |
|-----------|--------------|
| `test_batch_processing_main.py` | Batch processing functionality |
| `test_batch_processing_orchestration.py` | Batch processing orchestration |
| `test_batch_processing_utils.py` | Batch processing utility functions |
| `test_canvas_integration_main.py` | Canvas LMS integration |
| `test_canvas_integration_utils.py` | Canvas utility functions |
| `test_content_processing_main.py` | Content processing functionality |
| `test_content_processing_utils.py` | Content processing utility functions |
| `test_content_processing_utils_extended.py` | Extended content processing utils |
| `test_file_validation_main.py` | File validation functionality |
| `test_file_validation_utils.py` | Validation utility functions |
| `test_format_conversion_main.py` | Format conversion functionality |
| `test_format_conversion_utils.py` | Format conversion utility functions |
| `test_html_website_features.py` | HTML website configuration |
| `test_html_website_utils.py` | HTML website utility functions |
| `test_lab_manual_main.py` | Lab manual rendering |
| `test_lab_manual_utils.py` | Lab manual utility functions |
| `test_legacy_import_main.py` | Legacy import functionality |
| `test_legacy_import_main_extended.py` | Extended legacy import tests |
| `test_legacy_import_utils.py` | Legacy import utility functions |
| `test_markdown_to_pdf_main.py` | PDF conversion |
| `test_module_organization_main.py` | Module structure creation |
| `test_module_organization_main_extended.py` | Extended module organization tests |
| `test_module_organization_utils.py` | Module organization utilities |
| `test_publish_main.py` | Publish functionality |
| `test_publish_utils.py` | Publish utility functions |
| `test_schedule_main.py` | Schedule processing functionality |
| `test_schedule_utils.py` | Schedule utility functions |
| `test_speech_to_text_main.py` | Speech-to-text functionality |
| `test_text_to_speech_main.py` | Text-to-speech functionality |
| `test_validation_main.py` | Validation functionality |
| `test_validation_utils.py` | Validation utility functions |

### Integration and Verification Tests

| Test File | Purpose |
|-----------|---------|
| `test_cli.py` | CLI argument parsing |
| `test_dependencies.py` | Dependency availability verification |
| `test_imports.py` | Import verification |
| `test_integration.py` | Cross-module integration tests |
| `test_orchestration.py` | Module orchestration patterns |
| `test_real_implementations.py` | Real implementation verification |

## Running Tests

**Important**: Always use `uv run pytest` to ensure tests run in the correct environment with all dependencies installed.

### All Tests

```bash
DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH" uv run pytest tests/ -v
```

### Specific Test File

```bash
uv run pytest tests/test_[module_name].py -v
```

### With Coverage

```bash
uv run pytest --cov=src --cov-report=html tests/
```

### Import Verification

```bash
uv run pytest tests/test_imports.py -v
```

### Dependency Verification

```bash
uv run pytest tests/test_dependencies.py -v
```

### Real Implementation Verification

```bash
uv run pytest tests/test_real_implementations.py -v
```

### Tests Requiring Internet

Some tests require internet connection for external APIs (gTTS, speech recognition). These tests will be skipped if internet is unavailable:

```bash
# Run all tests (skips internet-required tests if offline)
uv run pytest tests/

# Skip tests requiring internet
uv run pytest tests/ -m "not requires_internet"
```

## Test Standards

- Use pytest framework
- Follow AAA pattern (Arrange, Act, Assert)
- Include both unit and integration tests
- Maintain high test coverage (>70%)
- Use real implementations - no mocks

## Test Markers

| Marker | Description |
|--------|-------------|
| `requires_internet` | Tests requiring internet connection |
| `requires_api` | Tests requiring external API access |

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `temp_dir`: Temporary directory for test files
- `sample_markdown_file`: Sample markdown file for testing
- `sample_text_file`: Sample text file for testing
- `sample_module_structure`: Sample module directory structure
- `sample_curriculum_files`: Sample files for each curriculum type

## Documentation

- **[AGENTS.md](AGENTS.md)**: Test structure and testing processes documentation
