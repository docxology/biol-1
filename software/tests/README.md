# Test Files

## Overview

This directory contains test files for validating software functionality. Test structure mirrors the source code organization in `src/`.

## Test Organization

Tests are organized to mirror the source code structure:
- `test_markdown_to_pdf.py`: Tests for Markdown to PDF conversion
- `test_text_to_speech.py`: Tests for text-to-speech generation
- `test_format_conversion.py`: Tests for format conversion utilities
- `test_module_organization.py`: Tests for module structure creation
- `test_canvas_integration.py`: Tests for Canvas integration
- `test_file_validation.py`: Tests for file validation
- `test_integration.py`: Integration tests across modules

## Running Tests

**Important**: Always use `uv run pytest` to ensure tests run in the correct environment with all dependencies installed.

### All Tests
```bash
uv run pytest tests/
```

### Specific Test File
```bash
uv run pytest tests/test_[module_name].py
```

### With Coverage
```bash
uv run pytest --cov=src tests/
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
- Maintain high test coverage

## Documentation

- **[AGENTS.md](AGENTS.md)**: Test structure and testing processes documentation
