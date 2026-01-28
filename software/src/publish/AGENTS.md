# Publish Module — Technical Documentation

## Overview

The publish module handles copying generated course materials from development directories to the published output directories.

## Module Interface

### Main Functions

#### `publish_course(course_path: str, publish_root: str = None) -> Dict[str, Any]`

Publishes course materials to the published directory.

**Args:**

- `course_path`: Path to the course directory (e.g., 'biol-1')
- `publish_root`: Root directory for publishing (default: PUBLISHED in repo root)

**Returns:**

- Dictionary with keys: `course`, `modules_published`, `syllabus_files`, `total_files`, `modules`, `errors`

### Utility Functions

#### `get_course_config(course_name: str) -> Dict[str, str]`

Get course-specific configuration (source directories, included content).

#### `clean_directory(path: Path) -> None`

Remove all contents from a directory or create if doesn't exist.

#### `copy_directory_contents(src: Path, dst: Path, exclude_patterns: List[str] = None) -> int`

Copy contents of source directory to destination, with exclusion patterns.

## Configuration

Course configurations in `config.py`:

| Course | Module Source | Syllabus Source | Include Syllabus |
|--------|--------------|-----------------|------------------|
| biol-1 | `output` | `output` | Yes |
| biol-8 | `output` | `output` | Yes |

## Usage

```python
from src.publish.main import publish_course

# Publish a course
results = publish_course("course_development/biol-8")
print(f"Published {results['modules_published']} modules")
```

## Integration Points

- **batch_processing**: Generates output files before publishing
- **format_conversion**: Creates multi-format outputs
- **PUBLISHED/**: Target directory for published content
