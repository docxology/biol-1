# Software Technical Documentation

## Overview

Technical documentation for course management software utilities, including function signatures, module APIs, and code organization.

## Software Modules

### Markdown to PDF Rendering

**Purpose**: Convert Markdown course materials to PDF format

**Location**: `src/markdown_to_pdf/`

**Key Functions**:
- `render_markdown_to_pdf(input_path: str, output_path: str, css_content: Optional[str] = None, pdf_options: Optional[Dict[str, Any]] = None) -> None`
- `batch_render_markdown(directory: str, output_dir: str) -> List[str]`
- `configure_pdf_options(template: str, options: dict) -> dict`

**Dependencies**: WeasyPrint (PDF generation), Markdown parser

### Text-to-Speech Generation

**Purpose**: Generate audio content from text materials

**Location**: `src/text_to_speech/`

**Key Functions**:
- `generate_speech(text: str, output_path: str, voice: str = "default", lang: Optional[str] = None, slow: bool = False) -> None`
- `batch_generate_speech(input_dir: str, output_dir: str) -> List[str]`
- `configure_voice_settings(voice: str, speed: float, pitch: float) -> dict`

**Dependencies**: gTTS (Google Text-to-Speech), audio file handling

### Format Conversion

**Purpose**: Batch processing of file format conversions

**Location**: `src/format_conversion/`

**Key Functions**:
- `convert_file(input_path: str, output_format: str, output_path: str) -> None`
- `batch_convert(directory: str, input_format: str, output_format: str) -> List[str]`
- `get_supported_formats() -> dict`

**Dependencies**: File format conversion libraries

### Module Organization

**Purpose**: Automated structure creation for new modules

**Location**: `src/module_organization/`

**Key Functions**:
- `create_module_structure(course_path: str, module_number: int) -> str`
- `create_next_module(course_path: str) -> str` - Create next module in sequence
- `validate_module_structure(module_path: str) -> bool`
- `initialize_module_files(module_path: str, template: str) -> None`
- `list_course_modules(course_path: str) -> List[str]` - List all modules in course
- `get_module_statistics(module_path: str) -> dict` - Get module statistics

**Utility Functions**:
- `get_module_number_from_path(module_path: Path) -> int` - Extract module number
- `list_all_modules(course_path: Path) -> List[Path]` - List all module directories
- `get_next_module_number(course_path: Path) -> int` - Get next available module number

**Dependencies**: File system operations, template engine

### Canvas Integration

**Purpose**: Scripts for batch uploading module materials

**Location**: `src/canvas_integration/`

**Key Functions**:
- `upload_module_to_canvas(module_path: str, course_id: str, api_key: str, domain: str = "canvas.instructure.com") -> dict`
- `validate_upload_readiness(module_path: str) -> List[str]`
- `sync_module_structure(module_path: str, canvas_course_id: str, api_key: str, domain: str = "canvas.instructure.com") -> dict`

**Dependencies**: Canvas API client, authentication handling, requests library

### File Validation

**Purpose**: Checks for required files in each module

**Location**: `src/file_validation/`

**Key Functions**:
- `validate_module_files(module_path: str) -> dict`
- `check_naming_conventions(directory: str) -> List[str]`
- `verify_required_structure(module_path: str) -> bool`
- `validate_course_structure(course_path: str) -> dict` - Validate entire course
- `get_validation_report(module_path: str) -> dict` - Detailed validation report
- `find_missing_materials(module_path: str) -> dict` - Find missing materials
- `check_file_sizes(module_path: str, max_size: int) -> List[str]` - Check file sizes

**Utility Functions**:
- `get_file_type(file_name: str) -> str` - Determine file type (assignment, lecture, etc.)
- `extract_module_number_from_filename(file_name: str) -> int` - Extract module number from filename
- `validate_file_name_structure(file_name: str) -> dict` - Comprehensive file name validation

**Dependencies**: File system operations, validation rules

### Speech-to-Text

**Purpose**: Transcribe audio files to text

**Location**: `src/speech_to_text/`

**Key Functions**:
- `transcribe_audio(audio_path: str, output_path: str, language: str = "en") -> str`
- `batch_transcribe_audio(input_dir: str, output_dir: str) -> List[str]`
- `transcribe_from_markdown(markdown_path: str, output_path: str) -> str`

**Dependencies**: speech_recognition, pydub

### Batch Processing

**Purpose**: Process entire modules for multiple format conversions

**Location**: `src/batch_processing/`

**Key Functions**:
- `process_module_to_pdf(module_path: str, output_dir: str) -> List[str]`
- `process_module_to_audio(module_path: str, output_dir: str) -> List[str]`
- `process_module_to_text(module_path: str, output_dir: str) -> List[str]`
- `generate_module_media(module_path: str, output_dir: str) -> dict`
- `process_module_by_type(module_path: str, output_dir: str) -> dict` - Process by curriculum element type
- `process_syllabus(syllabus_path: str, output_dir: str) -> dict` - Process syllabus files
- `clear_all_outputs(repo_root: Path) -> dict` - Clear all output directories
- `process_module_website(module_path: str, output_dir: Optional[str] = None) -> str` - Generate module website

**Dependencies**: All conversion modules

### HTML Website Generation

**Purpose**: Generate comprehensive HTML websites for modules with audio, quizzes, and interactive features

**Location**: `src/html_website/`

**Key Functions**:
- `generate_module_website(module_path: str, output_dir: Optional[str] = None, course_name: Optional[str] = None) -> str`

**Features**:
- Dark mode toggle with localStorage persistence
- Back to top button
- Collapsible sections
- Interactive quizzes (multiple choice, true/false, matching, free response)
- Embedded audio players
- Print-friendly layout
- Mobile responsive design

**Dependencies**: markdown2, batch_processing

### Schedule Processing

**Purpose**: Parse schedule markdown files and generate outputs in multiple formats

**Location**: `src/schedule/`

**Key Functions**:
- `parse_schedule_markdown(schedule_path: str) -> Dict[str, Any]`
- `process_schedule(schedule_path: str, output_dir: str, formats: Optional[List[str]] = None) -> Dict[str, Any]`
- `generate_schedule_outputs(schedule_data: Dict[str, Any], output_dir: Path, base_name: str, formats: List[str]) -> Dict[str, List[str]]`
- `batch_process_schedules(directory: str, output_dir: str, formats: Optional[List[str]] = None) -> Dict[str, Any]`

**Dependencies**: markdown_to_pdf, text_to_speech, format_conversion

### Publish Module

**Purpose**: Export finalized course materials to the public `PUBLISHED/` directory

**Location**: `src/publish/`

**Key Functions**:
- `publish_course(course_path: str, publish_root: str = None) -> Dict[str, Any]` - Main publishing logic
- `get_course_config(course_name: str) -> Dict[str, str]` - Get course-specific configuration
- `copy_directory_contents(src: Path, dst: Path, exclude_patterns: Optional[List[str]] = None) -> int` - Intelligent copy

**Dependencies**: shutil, path operations

## Code Organization

### Directory Structure

```
software/
├── src/              # Source code
│   ├── batch_processing/
│   ├── canvas_integration/
│   ├── file_validation/
│   ├── format_conversion/
│   ├── html_website/
│   ├── markdown_to_pdf/
│   ├── module_organization/
│   ├── schedule/
│   ├── speech_to_text/
│   └── text_to_speech/
├── tests/            # Test files
│   └── [mirrors src/ structure]
├── scripts/          # Generation scripts
└── docs/             # Documentation
    └── [module-specific docs]
```

### Module Structure

Each module in `src/` follows this structure:
- `__init__.py`: Module initialization and exports
- `main.py` or `[module_name].py`: Core functionality
- `utils.py`: Utility functions
- `config.py`: Configuration management

### Testing Structure

Test files in `tests/` mirror the source structure:
- `test_[module_name].py`: Unit tests for each module
- `test_integration.py`: Integration tests
- `test_utils.py`: Utility function tests

## Real Methods Policy

### Core Principle
**All code uses real methods and implementations - no mocks, stubs, or fake methods.**

### Implementation Standards
- All functions use real library implementations (weasyprint, gTTS, requests, etc.)
- All file operations use real file system operations
- All validation uses real validation logic
- All API integrations use real API clients (with proper error handling)

### Testing Standards
- Tests use real file operations and real library calls
- No mocks or stubs in test code
- External API tests validate structure/logic, not actual API calls
- Integration tests that require external services are clearly marked

### External Dependencies
- Real library calls for all functionality
- Proper error handling for network operations
- Graceful degradation when external services are unavailable
- Clear documentation of external service requirements

## Development Workflow

### Adding New Modules

1. Create module directory in `src/`
2. Implement core functionality following module structure using real methods
3. Write tests in `tests/` mirroring source structure using real implementations
4. Document in module-specific docs
5. Update this AGENTS.md with function signatures

### Testing

1. Run unit tests: `pytest tests/`
2. Run integration tests: `pytest tests/test_integration.py`
3. Validate code coverage: `pytest --cov=src tests/`
4. All tests must use real methods - no mocks or stubs

### Documentation

1. Update module README.md with usage examples
2. Document function signatures in module AGENTS.md
3. Update main software AGENTS.md with new module information

## Dependencies

### Core Dependencies
- Python 3.x
- Markdown parser
- PDF generation library
- Text-to-speech engine
- Canvas API client

### Development Dependencies
- pytest: Testing framework
- pytest-cov: Code coverage
- black: Code formatting
- mypy: Type checking

## Build and Deployment

### Build Process
- Automated compilation and packaging
- Dependency management
- Version control

### Deployment
- Package distribution
- Installation scripts
- Configuration management
