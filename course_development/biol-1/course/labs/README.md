# BIOL-1 Laboratory Protocols

## Overview

This directory contains laboratory protocols for BIOL-1: General Biology (Pelican Bay, Fall 2026). Labs are designed to be hands-on, interactive exercises that reinforce concepts from the lecture modules.

## Lab Inventory

| Lab | Topic | Status | Related Module |
|-----|-------|--------|----------------|
| [Lab 01](lab-01_measurement-methods.md) | Introduction to Scientific Measurement | ✅ Complete | Module 01 |
| [Lab 02](lab-02_probability-statistics.md) | Probability and Statistics | ✅ Complete | Module 02 |
| [Lab 03](lab-03_microscopy.md) | Introduction to Microscopy | ✅ Complete | Module 03 |
| [Lab 04](lab-04_liquid-chemistry.md) | Liquid Chemistry | ✅ Complete | Module 05 |
| [Lab 05](lab-05_viewing-life.md) | Viewing Life | ✅ Complete | Module 06 |
| [Lab 06](lab-06_exam-review.md) | Exam 01 Review (Paper-based) | ✅ Complete | Review |
| [Lab 07](lab-07_molecular-genetics.md) | Molecular Genetics | ✅ Complete | Module 07 |
| [Lab 08](lab-08_cellular-genetics.md) | Cellular Genetics (Mitosis & Meiosis) | ✅ Complete | Module 08 |
| [Lab 09](lab-09_inheritance-genetics.md) | Inheritance Genetics | ✅ Complete | Module 09 |
| [Lab 10](lab-10_epigenetics.md) | Epigenetics | ✅ Complete | Module 10 |
| [Lab 11](lab-11_genomics-biotechnology.md) | Genomics & Biotechnology | ✅ Complete | Module 11 |
| [Lab 12](lab-12_exam-02-review.md) | Exam 02 Review | ✅ Complete | Review |
| [Lab 13](lab-13_darwin-evolution.md) | Darwin & Evolution | ✅ Complete | Module 12 |
| [Lab 14](lab-14_how-populations-evolve.md) | How Populations Evolve | ✅ Complete | Module 13 |
| [Lab 15](lab-15_macroevolution.md) | Macroevolution | ✅ Complete | Module 14 |
| [Lab 16](lab-16_population-systems-ecology.md) | Population and Systems Ecology | ✅ Complete | Module 15 |
| [Lab 17](lab-17_exam-03-review.md) | Exam 03 Review (Modules 12–15) | ✅ Complete | Review |

**Status Summary:** 17 complete, 0 stubs

## Development Status

- ✅ **Complete**: Labs 01–03 (measurement, statistics, microscopy)
- ✅ **Complete**: Labs 04–06 (liquid chemistry, viewing life, exam 01 review)
- ✅ **Complete**: Labs 07–12 (molecular genetics through exam 02 review)
- ✅ **Complete**: Labs 13–17 (evolution/ecology sequence and exam 03 review)

## Lab Format

Labs use specialized markdown directives for interactive elements:

- **Required front matter**: `# Lab N`, the BIOL-1 course subtitle, the exact `**Name:** {fill:text} **Date:** {fill:text}` line, then `## Learning Objectives`
- **Data Tables**: `<!-- lab:data-table -->` for fillable data collection
- **Reflection Boxes**: `<!-- lab:reflection -->` for open-ended responses
- **Object Selection**: `<!-- lab:object-selection -->` for choosing study subjects
- **Fillable Fields**: `{fill:text}`, `{fill:textarea rows=N}` for inline inputs

## Output Generation

Labs are processed through the `lab_manual` module to generate multi-format outputs:

```bash
cd software
uv run python -c "
from src.lab_manual.main import render_lab_manual, batch_render_lab_manuals

# Generate single lab PDF
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/pdf/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-1: General Biology'
)

# Generate single lab HTML (interactive)
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/html/lab-01_measurement-methods.html',
    'html',
    course_name='BIOL-1: General Biology'
)

# Batch generate all labs
batch_render_lab_manuals(
    '../course_development/biol-1/course/labs',
    '../course_development/biol-1/course/labs/output',
    'pdf',
    course_name='BIOL-1: General Biology'
)
"
```

## Output Directory

Generated files are stored in `output/`:

- `output/pdf/*.pdf` - Printable lab worksheets
- `output/html/*.html` - Interactive web versions with fillable fields when HTML lab rendering is requested

## Related Documentation

- [Course README](../README.md) - Course materials overview
- [Software Lab Manual Docs](../../../../software/src/lab_manual/README.md) - Technical documentation
- [Lab 01 Template Reference](lab-01_measurement-methods.md) - Use as template for future labs

---

*Last Updated: 2026-01-28*
