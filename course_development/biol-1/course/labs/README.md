# BIOL-1 Laboratory Protocols

## Overview

This directory contains laboratory protocols for BIOL-1: Biology (Pelican Bay Prison, Spring 2026). Labs are designed to be hands-on, interactive exercises that reinforce concepts from the lecture modules.

## Lab Inventory

| Lab | Topic | Status | Related Module |
|-----|-------|--------|----------------|
| [Lab 01](lab-01_measurement-methods.md) | Introduction to Scientific Measurement | ✅ Complete | Module 01 |
| [Lab 02](lab-02_probability-statistics.md) | Probability and Statistics | ✅ Complete | Module 02 |
| [Lab 03](lab-03_organic-molecules.md) | Organic Molecules | 📝 Stub | Module 03 |
| [Lab 04](lab-04_cells.md) | Cells | 📝 Stub | Module 04 |
| [Lab 05](lab-05_membranes.md) | Membranes | 📝 Stub | Module 05 |
| [Lab 06](lab-06_metabolism.md) | Metabolism | 📝 Stub | Module 06 |
| [Lab 07](lab-07_photosynthesis.md) | Photosynthesis | 📝 Stub | Module 07 |
| [Lab 08](lab-08_cellular-respiration.md) | Cellular Respiration | 📝 Stub | Module 08 |
| [Lab 09](lab-09_cell-division-mitosis.md) | Cell Division: Mitosis | 📝 Stub | Module 09 |
| [Lab 10](lab-10_meiosis-reproduction.md) | Meiosis and Reproduction | 📝 Stub | Module 10 |
| [Lab 11](lab-11_mendelian-genetics.md) | Mendelian Genetics | 📝 Stub | Module 11 |
| [Lab 12](lab-12_gene-expression.md) | Gene Expression | 📝 Stub | Module 12 |
| [Lab 13](lab-13_gene-regulation.md) | Gene Regulation | 📝 Stub | Module 13 |
| [Lab 14](lab-14_biotechnology-genomics.md) | Biotechnology and Genomics | 📝 Stub | Module 14 |
| [Lab 15](lab-15_darwin-evolution.md) | Darwin and Evolution | 📝 Stub | Module 15 |
| [Lab 16](lab-16_microevolution.md) | Microevolution | 📝 Stub | Module 16 |
| [Lab 17](lab-17_speciation-macroevolution.md) | Speciation and Macroevolution | 📝 Stub | Module 17 |

**Status Summary:** 2 complete, 15 stubs

## Development Status

- ✅ **Complete**: Lab 01 (289 lines, fully developed with interactive elements)
- ✅ **Complete**: Lab 02 (probability and statistics, tear-apart paper randomizers)
- 📝 **Stubs**: Labs 03-17 (placeholder structure with learning objectives)

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
from src.lab_manual.main import render_lab_manual, batch_render_lab_manuals

# Generate single lab PDF
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-1: Biology'
)

# Generate single lab HTML (interactive)
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/lab-01_measurement-methods.html',
    'html',
    course_name='BIOL-1: Biology'
)

# Batch generate all labs
batch_render_lab_manuals(
    '../course_development/biol-1/course/labs',
    '../course_development/biol-1/course/labs/output',
    'pdf',
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
- [Lab 01 Template Reference](lab-01_measurement-methods.md) - Use as template for developing stubs

---

*Last Updated: 2026-01-28*
