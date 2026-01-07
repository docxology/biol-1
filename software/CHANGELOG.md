# Changelog

## New Methods and Features

### Module Organization Module

**New Functions Added**:
- `create_next_module(course_path: str) -> str` - Automatically creates the next module in sequence
- `list_course_modules(course_path: str) -> List[str]` - Lists all modules in a course, sorted by number
- `get_module_statistics(module_path: str) -> dict` - Returns comprehensive statistics about a module

**New Utility Functions**:
- `get_module_number_from_path(module_path: Path) -> int` - Extracts module number from path
- `list_all_modules(course_path: Path) -> List[Path]` - Lists all module directories
- `get_next_module_number(course_path: Path) -> int` - Gets next available module number

### File Validation Module

**New Utility Functions**:
- `get_file_type(file_name: str) -> str` - Identifies file type (assignment, lecture, lab, study_guide, quiz)
- `extract_module_number_from_filename(file_name: str) -> int` - Extracts module number from filename
- `validate_file_name_structure(file_name: str) -> dict` - Comprehensive file name validation with detailed results

### Testing

**New Test Files**:
- `test_module_organization_utils.py` - Tests for utility functions (6 tests)
- `test_module_organization_main_extended.py` - Extended tests for main functions (8 tests)
- `test_file_validation_utils.py` - Tests for validation utility functions (12 tests)

**Total Tests**: 69 tests (up from 43)

### Documentation

**Updated Files**:
- `software/AGENTS.md` - Added new function signatures and utility functions
- `software/src/AGENTS.md` - Updated with complete function signatures for all new methods
- All documentation emphasizes real methods policy

## Test Coverage

**Overall Coverage**: 78% (667 statements, 144 missed)

**Module Coverage**:
- `module_organization`: 91% (main.py), 91% (utils.py)
- `file_validation`: 84% (main.py), 86% (utils.py)
- `markdown_to_pdf`: 92% (main.py), 90% (utils.py)
- `format_conversion`: 74% (main.py), 67% (utils.py)
- `text_to_speech`: 89% (main.py), 50% (utils.py)
- `canvas_integration`: 40% (main.py), 46% (utils.py) - API upload functions require credentials

## All Methods Use Real Implementations

- No mocks or stubs
- All file operations use real file system
- All library calls use real implementations
- All validation uses real validation logic
