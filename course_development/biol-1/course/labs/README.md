# BIOL-1 Laboratory Protocols

## Overview

This directory contains laboratory protocols for BIOL-1: Biology (Pelican Bay Prison, Spring 2026). Labs are designed to be hands-on, interactive exercises that reinforce concepts from the lecture modules.

## Lab Inventory

| Lab | Topic | Status | Related Module |
|-----|-------|--------|----------------|
| [Lab 01](lab-01_measurement-methods.md) | Introduction to Scientific Measurement | ✅ Complete | Module 1 |

*Additional labs will be added as the course develops.*

## Lab Format

Labs use specialized markdown directives for interactive elements:

- **Data Tables**: `<!-- lab:data-table -->` for fillable data collection
- **Reflection Boxes**: `<!-- lab:reflection -->` for open-ended responses
- **Object Selection**: `<!-- lab:object-selection -->` for choosing study subjects
- **Fillable Fields**: `{fill:text}`, `{fill:textarea rows=N}` for inline inputs

## Output Generation

Labs are processed through the `lab_manual` module to generate multi-format outputs:

```bash
cd software
uv run python -c "
from src.lab_manual.main import render_lab_manual

# Generate PDF
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-1: Biology'
)

# Generate HTML (interactive)
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/lab-01_measurement-methods.html',
    'html',
    course_name='BIOL-1: Biology'
)
"
```

## Output Directory

Generated files are stored in `output/`:

- `*.pdf` - Printable lab worksheets
- `*.html` - Interactive web versions with fillable fields

## Related Documentation

- [Course README](../README.md) - Course materials overview
- [Software Lab Manual Docs](../../../software/src/lab_manual/README.md) - Technical documentation
