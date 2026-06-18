"""Configuration for module organization."""

from typing import List

# Required files in each active BIOL-1-style module
REQUIRED_FILES: List[str] = [
    "README.md",
    "AGENTS.md",
    "questions.md",
    "keys-to-success.md",
]

# BIOL-1 modules do not require module-local subdirectories.
REQUIRED_DIRECTORIES: List[str] = []

# Template content for README.md
README_TEMPLATE: str = """# Module {module_number}

## Overview

Module {module_number} course materials.

## Contents

### Course Materials

This module includes:
- **questions.md**: Practice questions and self-check prompts
- **keys-to-success.md**: Study guide and key ideas for the module
- Optional **resources/**: Module-local datasets or images
- Generated **output/**: Rendered study guide and website artifacts

## Documentation

- **[AGENTS.md](AGENTS.md)**: Technical documentation for module structure and file management
"""

# Template content for AGENTS.md
AGENTS_TEMPLATE: str = """# Module {module_number} Technical Documentation

## Module Structure

### Directory Organization

```
module-{module_number}/
├── README.md             # Module overview
├── AGENTS.md             # This file
├── questions.md          # Practice questions
├── keys-to-success.md    # Study guide / keys
├── resources/            # Optional module-local assets
└── output/               # Generated artifacts
```

### File Types

- **Practice Questions**: `questions.md`
- **Study Guide**: `keys-to-success.md`
- **Resources**: Optional module-local datasets and images
- **Generated Output**: Created by the publish pipeline, not edited by hand

## File Naming Conventions

- Source files use stable names: `README.md`, `AGENTS.md`, `questions.md`, and `keys-to-success.md`.
- Generated output filenames are prefixed with the module folder name by the publish pipeline.
- Optional resource filenames should use lowercase kebab-case.

## File Management

### Material Updates
- Maintain version control for major revisions
- Update README.md when adding new materials
- Document file changes in this AGENTS.md

## Canvas Upload

### Preparation
- Verify all required files are present
- Check file naming conventions
- Ensure generated output is refreshed before upload
- Validate that no private materials are included

### Upload Process
- Upload entire module folder to Canvas
- Maintain folder structure
- Update Canvas links after upload
"""

# Template content for keys-to-success.md
KEYS_TO_SUCCESS_TEMPLATE: str = """# Module {module_number}: Keys to Success

## Learning Objectives

By the end of this module, you should be able to:

1. Describe the central concepts for Module {module_number}.
2. Apply those concepts to representative BIOL-1 examples.
3. Explain how the module connects to earlier course material.

## Introduction and Big Picture

Add the module overview here.

## Key Information and Concepts

Add numbered concept sections here.

## Strategic Tips for Studying

Add study tips here.
"""

# Template content for questions.md
QUESTIONS_TEMPLATE: str = """# Module {module_number}: Practice Questions

## Multiple Choice

1. Add a module-aligned multiple-choice question here.

A. Option A
B. Option B
C. Option C
D. Option D

## Fill in the Blank

2. Add a concise fill-in prompt here: ________

## Free Response

3. Add a short free-response prompt here.
"""
