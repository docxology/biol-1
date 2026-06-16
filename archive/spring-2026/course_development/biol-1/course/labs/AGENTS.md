# Technical Documentation: BIOL-1 Labs

## Overview

Technical documentation for the BIOL-1 laboratory protocol directory. Labs are Markdown source files processed through the `lab_manual` module to generate PDF and HTML outputs.

## Lab File Inventory

| File | Topic | Status |
|------|-------|--------|
| `lab-01_measurement-methods.md` | Introduction to Scientific Measurement | ✅ Complete |
| `lab-02_probability-statistics.md` | Probability and Statistics | ✅ Complete |
| `lab-03_microscopy.md` | Introduction to Microscopy | ✅ Complete |
| `lab-04_liquid-chemistry.md` | Liquid Chemistry | 📝 Stub |
| `lab-05_viewing-life.md` | Viewing Life | ✅ Complete |
| `lab-06_exam-review.md` | Exam 01 Review (Paper-based) | ✅ Complete |
| `lab-07_molecular-genetics.md` | Molecular Genetics | ✅ Complete |
| `lab-08_cellular-genetics.md` | Cellular Genetics (Mitosis & Meiosis) | ✅ Complete |
| `lab-09_inheritance-genetics.md` | Inheritance Genetics | ✅ Complete |
| `lab-10_epigenetics.md` | Epigenetics | ✅ Complete |
| `lab-11_genomics-biotechnology.md` | Genomics & Biotechnology | ✅ Complete |
| `lab-12_exam-02-review.md` | Exam 02 Review | ✅ Complete |
| `lab-13_darwin-evolution.md` | Darwin & Evolution (Module 12) | ✅ Complete |
| `lab-14_how-populations-evolve.md` | How Populations Evolve (Module 13) | ✅ Complete |
| `lab-15_macroevolution.md` | Macroevolution (Module 14) | ✅ Complete |
| `lab-16_population-systems-ecology.md` | Population & Systems Ecology (Module 15) | ✅ Complete |
| `lab-17_exam-03-review.md` | Exam 03 Review (Modules 12–15) | ✅ Complete |

**Status:** 16 complete, 1 stub (`lab-04_liquid-chemistry.md`)

## Lab Naming Convention

Files follow the pattern: `lab-XX_topic-name.md`

- `XX` = Zero-padded lab number (01–17)
- `topic-name` = Hyphenated topic description (matches module topic)

## Lab Markdown Directive Syntax

Labs use specialized HTML comment directives for interactive elements processed by the `lab_manual` module:

| Directive | Purpose |
|-----------|---------|
| `<!-- lab:data-table rows=N -->` | Fillable data collection table |
| `<!-- lab:reflection -->` | Open-ended response box |
| `<!-- lab:object-selection -->` | Object or specimen selection field |
| `<!-- lab:calculation -->` | Formula and calculation area |
| `{fill:text}` | Inline short text field |
| `{fill:number}` | Inline numeric field |
| `{fill:textarea rows=N}` | Multi-line fillable area |
| `**Name:** {fill:text} **Date:** {fill:text}` | Standard identification block (stripped from PDF header) |

See `lab-01_measurement-methods.md` as the reference implementation.

## Output Generation

Labs are processed via the `lab_manual` module:

```bash
cd software

# Generate single lab PDF
uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual(
    '../course_development/biol-1/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-1/course/labs/output/pdf/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-1: Biology'
)
"

# Batch generate all labs
uv run python -c "
from src.lab_manual.main import batch_render_lab_manuals
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

- `output/pdf/*.pdf` — Printable lab worksheets
- `output/html/*.html` — Interactive web versions with auto-saving fillable fields when HTML lab rendering is requested

## Related Documentation

| Document | Description |
|----------|-------------|
| [../README.md](../README.md) | Course materials overview |
| [../AGENTS.md](../AGENTS.md) | Course-level technical documentation |
| [../../../../software/src/lab_manual/README.md](../../../../software/src/lab_manual/README.md) | Lab manual module technical docs |
