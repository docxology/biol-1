# Content Processing Module

> **Navigation**: [← README](../README.md) | [ARCHITECTURE](../../docs/ARCHITECTURE.md)

This module provides content transformation functions for processing course materials.

---

## Purpose

Transform and normalize course content files, including:

- Question renumbering (sectioned → continuous format)
- Future: other content processing tasks

## Public API

### Main Functions

```python
from src.content_processing import (
    process_questions_file,      # Process single questions.md file
    renumber_questions_in_course # Process all questions in a course
)
```

### Utility Functions

```python
from src.content_processing import (
    extract_questions_from_sectioned,  # Extract questions from bullet format
    format_as_continuous               # Format questions as numbered list
)
```

## Usage Examples

```python
from pathlib import Path
from src.content_processing import process_questions_file, renumber_questions_in_course

# Process a single file
was_changed, count = process_questions_file(
    Path("module-01/questions.md"),
    dry_run=False,
    verbose=True
)

# Process all questions in a course
results = renumber_questions_in_course(
    repo_root=Path("/path/to/repo"),
    courses=["biol-1"],
    dry_run=True
)
```

## Module Structure

```
content_processing/
├── __init__.py      # Public exports
├── config.py        # Configuration constants
├── main.py          # High-level processing functions
├── utils.py         # Low-level utility functions
└── AGENTS.md        # This file
```
