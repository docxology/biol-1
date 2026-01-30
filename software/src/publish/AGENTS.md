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

**File**: `src/publish/utils.py`

#### `get_course_config(course_name: str) -> Dict[str, str]`

Get configuration for a specific course.

**Args:**

- `course_name`: Name of the course directory (e.g., 'biol-1')

**Returns:**

- Dictionary with configuration options

#### `clean_directory(path: Path) -> None`

Clean a directory (remove all contents) or create if doesn't exist.

**Args:**

- `path`: Path to the directory to clean

#### `copy_directory_contents(src: Path, dst: Path, exclude_patterns: Optional[List[str]] = None) -> int`

Copy contents of source directory to destination.

**Args:**

- `src`: Source directory path
- `dst`: Destination directory path
- `exclude_patterns`: List of glob patterns to exclude

**Returns:**

- Number of files copied

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
