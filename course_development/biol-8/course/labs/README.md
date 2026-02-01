# BIOL-8 Laboratory Protocols

## Overview

This directory contains laboratory protocols for BIOL-8: Human Biology (College of the Redwoods, Del Norte Campus, Spring 2026). Labs are designed to provide hands-on experience with biological concepts covered in the lecture modules.

## Lab Inventory

| Lab | Topic | Status | Related Module |
|-----|-------|--------|----------------|
| [Lab 01](lab-01_measurement-methods.md) | Introduction to Scientific Measurement | ✅ Complete | Module 01 |
| [Lab 02](lab-02_probability-statistics.md) | Probability and Statistics | ✅ Complete | Module 02 |
| [Lab 03](lab-03_measurement-techniques.md) | Measurement Techniques | ✅ Complete | Module 03 |
| [Lab 04](lab-04_introduction-to-microscopy.md) | Introduction to Microscopy | ✅ Complete | Module 04 |
| [Lab 05](lab-05_membranes.md) | Membranes | 📝 Stub | Module 05 |
| [Lab 06](lab-06_metabolism.md) | Metabolism | 📝 Stub | Module 06 |
| [Lab 07](lab-07_mitosis.md) | Mitosis | 📝 Stub | Module 07 |
| [Lab 08](lab-08_meiosis.md) | Meiosis | 📝 Stub | Module 08 |
| [Lab 09](lab-09_inheritance.md) | Inheritance | 📝 Stub | Module 09 |
| [Lab 10](lab-10_tissues.md) | Tissues | 📝 Stub | Module 10 |
| [Lab 11](lab-11_skeletal-system.md) | Skeletal System | 📝 Stub | Module 11 |
| [Lab 12](lab-12_muscular-system.md) | Muscular System | 📝 Stub | Module 12 |
| [Lab 13](lab-13_pathogens.md) | Pathogens | 📝 Stub | Module 13 |
| [Lab 14](lab-14_cardiovascular-system.md) | Cardiovascular System | 📝 Stub | Module 14 |
| [Lab 15](lab-15_respiratory-system.md) | Respiratory System | 📝 Stub | Module 15 |

## Lab Format

Labs use specialized markdown directives for interactive elements:

- **Data Tables**: `<!-- lab:data-table -->` for fillable data collection
- **Reflection Boxes**: `<!-- lab:reflection -->` for open-ended responses  
- **Object Selection**: `<!-- lab:object-selection -->` for choosing study subjects
- **Feasibility Analysis**: `<!-- lab:measurement-feasibility -->` for constraint evaluation
- **Calculation Boxes**: `<!-- lab:calculation -->` for formula and calculation areas
- **Fillable Fields**: `{fill:text}`, `{fill:number}`, `{fill:textarea rows=N}` for inline inputs

See [Lab 01](lab-01_measurement-methods.md) as the reference implementation for the full directive syntax.

## Output Generation

Labs are processed through the `lab_manual` module to generate multi-format outputs:

```bash
cd software
uv run python -c "
from src.lab_manual.main import render_lab_manual, batch_render_lab_manuals

# Generate single lab
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-8: Human Biology'
)

# Generate all labs (batch)
batch_render_lab_manuals(
    '../course_development/biol-8/course/labs',
    '../course_development/biol-8/course/labs/output',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"
```

## Output Directory

Generated files are stored in `output/`:

- `*.pdf` - Printable lab worksheets
- `*.html` - Interactive web versions with auto-saving fillable fields

## Naming Convention

Labs follow the pattern: `lab-XX_topic-name.md`

- `XX` = Two-digit lab number (01-15)
- `topic-name` = Hyphenated topic description

## Related Documentation

- [Course README](../README.md) - Course materials overview
- [Course AGENTS.md](../AGENTS.md) - Technical documentation
- [Software Lab Manual Docs](../../../software/src/lab_manual/README.md) - Lab manual module documentation
