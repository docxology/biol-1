# Test Structure and Testing Processes

## Test Organization

### Test File Structure

Test files mirror the source code structure:

```text
tests/
├── conftest.py                                     # Shared fixtures
├── canvas_stub_server.py                           # Local HTTP stub for Canvas API upload flows
├── test_imports.py                                 # Import verification
├── test_dependencies.py                            # Dependency version tests
├── test_real_implementations.py                    # Real implementation verification
├── test_integration.py                             # Cross-module integration
├── test_orchestration.py                           # Pipeline orchestration tests
├── test_cli.py                                     # CLI interface tests
├── test_batch_processing_main.py                   # batch_processing module
├── test_batch_processing_orchestration.py
├── test_batch_processing_utils.py
├── test_canvas_integration_main.py                 # canvas_integration module
├── test_canvas_integration_utils.py
├── test_content_processing_main.py                 # content_processing module
├── test_content_processing_utils.py
├── test_content_processing_utils_extended.py
├── test_file_validation_main.py                    # file_validation module
├── test_file_validation_utils.py
├── test_format_conversion_main.py                  # format_conversion module
├── test_format_conversion_utils.py
├── test_html_website_features.py                   # html_website module
├── test_html_website_utils.py
├── test_lab_manual_main.py                         # lab_manual module
├── test_lab_manual_utils.py
├── test_legacy_import_main.py                      # legacy_import module
├── test_legacy_import_main_extended.py
├── test_legacy_import_utils.py
├── test_markdown_to_pdf_main.py                    # markdown_to_pdf module
├── test_module_organization_main.py                # module_organization module
├── test_module_organization_main_extended.py
├── test_module_organization_utils.py
├── test_publish_main.py                            # publish module
├── test_publish_utils.py
├── test_schedule_main.py                           # schedule module
├── test_schedule_utils.py
├── test_speech_to_text_main.py                     # speech_to_text module
├── test_text_to_speech_main.py                     # text_to_speech module
├── test_validation_main.py                         # validation module
└── test_validation_utils.py
```

### Test Function Naming

- Format: `test_[function_name]_[scenario]`
- Example: `test_render_markdown_to_pdf_success()`
- Example: `test_render_markdown_to_pdf_invalid_input()`

## Testing Processes

### Unit Testing

**Purpose**: Test individual functions in isolation

**Structure**:

```python
def test_function_name_scenario():
    # Arrange: Set up test data
    # Act: Execute function
    # Assert: Verify results
```

**Coverage**: All public functions should have unit tests

### Integration Testing

**Purpose**: Test interactions between modules

**Location**: `test_integration.py`

**Focus Areas**:

- Module interactions
- End-to-end workflows
- Error handling across modules

### Test Data Management

**Fixtures**: Use pytest fixtures for reusable test data
**Location**: `conftest.py` for shared fixtures

**Test Files**: Store test data files in `tests/data/` directory

## Test Execution

### Running Tests

**Important**: Always use `uv run pytest` to ensure tests run in the correct environment.

**All Tests**:

```bash
uv run pytest tests/
```

**Specific Module**:

```bash
uv run pytest tests/test_[module_name].py
```

**With Verbose Output**:

```bash
uv run pytest -v tests/
```

**With Coverage**:

```bash
uv run pytest --cov=src --cov-report=html tests/
```

**Import Verification**:

```bash
uv run pytest tests/test_imports.py -v
```

**Dependency Verification**:

```bash
uv run pytest tests/test_dependencies.py -v
```

**Real Implementation Verification**:

```bash
uv run pytest tests/test_real_implementations.py -v
```

### Continuous Integration

Tests should run automatically on:

- Pull requests
- Commits to main branch
- Scheduled runs

## Test Quality Standards

### Coverage Targets

- Overall coverage: > 80% (as measured by full test run against the live modules)
- Critical functions: > 90%
- Utility functions: > 70%

> **Note**: Run `bash run_tests.sh` (or `uv run pytest`) from `software/` to generate a fresh `.coverage` report. The `uv run coverage report` against the last `.coverage` snapshot reflects only the subset exercised in that run.

### Test Quality

- Clear test names describing scenario
- Isolated tests (no dependencies between tests)
- Fast execution (< 1 second per test)
- Deterministic results (no flaky tests)

### Documentation

- Test functions include docstrings explaining purpose
- Complex test scenarios documented
- Edge cases explicitly tested

## Real Methods Policy

### Core Principle

**All tests use real methods and implementations - no mocks, stubs, or fake methods.**

### Real Implementations

- All file operations use real file system operations
- All library calls use real library implementations (gTTS, weasyprint, etc.)
- All validation logic uses real validation functions
- All module operations use real module creation and validation

### External API Testing

- For external APIs (e.g., Canvas API), tests validate the logic and structure validation
- Tests verify that validation works correctly before API calls
- `test_canvas_integration_main.py` includes `test_upload_module_to_canvas_uses_real_http_through_local_stub`, which monkeypatches the API base URL to a threaded `HTTPServer` in `canvas_stub_server.py` (real HTTP, real `requests`, no mocking of HTTP clients)
- `test_optional_upload_module_to_canvas_requires_env_credentials` (`@pytest.mark.requires_api`) runs only when `CANVAS_API_KEY` and `CANVAS_COURSE_ID` are set for a live sandbox
- `test_convert_audio_to_text` (`@pytest.mark.requires_internet`) uses real gTTS and Google Speech; if recognition returns “could not understand” for the generated clip, pytest skips rather than failing the suite

### Test Isolation

- Each test should be independent
- No shared state between tests
- Clean up test artifacts
- Use temporary directories for file operations

## Test Maintenance

### Regular Tasks

- Review test coverage reports
- Update tests when functions change
- Remove obsolete tests
- Refactor duplicate test code

### Validation

- All tests pass before merging
- Coverage targets maintained
- Test execution time monitored
- Flaky tests identified and fixed
