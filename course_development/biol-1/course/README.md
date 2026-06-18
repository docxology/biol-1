# BIOL-1 Course Materials

## Overview

This directory contains all public course materials for **BIOL-1: General Biology** (Pelican Bay, Fall 2026), organized by module. All materials in this directory are suitable for distribution to students.

## Course Structure

The course covers **16** content modules progressing through foundational biology concepts:

### Modules

| Module | Topic | Directory |
| --- | --- | --- |
| 01 | Study of Life | [module-01-study-of-life](module-01-study-of-life/) |
| 02 | Basic Chemistry | [module-02-basic-chemistry](module-02-basic-chemistry/) |
| 03 | Organic Molecules | [module-03-organic-molecules](module-03-organic-molecules/) |
| 04 | Cells | [module-04-cells](module-04-cells/) |
| 05 | Membranes | [module-05-membranes](module-05-membranes/) |
| 06 | Metabolism | [module-06-metabolism](module-06-metabolism/) |
| 07 | Molecular Genetics | [module-07-molecular-genetics](module-07-molecular-genetics/) |
| 08 | Cellular Genetics | [module-08-cellular-genetics](module-08-cellular-genetics/) |
| 09 | Inheritance Genetics | [module-09-inheritance-genetics](module-09-inheritance-genetics/) |
| 10 | Epigenetics | [module-10-epigenetics](module-10-epigenetics/) |
| 11 | Genomics & Biotechnology | [module-11-genomics-biotechnology](module-11-genomics-biotechnology/) |
| 12 | Darwin & Evolution | [module-12-darwin-evolution](module-12-darwin-evolution/) |
| 13 | How Populations Evolve | [module-13-how-populations-evolve](module-13-how-populations-evolve/) |
| 14 | Macroevolution | [module-14-macroevolution](module-14-macroevolution/) |
| 15 | Population & Systems Ecology | [module-15-population-systems-ecology](module-15-population-systems-ecology/) |
| 16 | Capstone Systems Synthesis | [module-16-capstone-systems-synthesis](module-16-capstone-systems-synthesis/) |

## Directory Organization

```text
course/
├── README.md                    # This file
├── AGENTS.md                    # Technical documentation
│
├── exams/                       # Exam materials
├── labs/                        # 16 laboratory protocols (lab-NN_topic.md)
│   ├── lab-01_measurement-methods.md
│   ├── dashboards/              # lab-NN_*-dashboard.html (one per numbered lab)
│   └── output/                  # Generated lab outputs
├── practice_tests/              # Practice tests with answer keys
├── quizzes/                     # Quiz materials
├── review_materials/            # Non-primary exam review worksheets
│
└── module-XX-topic/             # Module directories
    ├── README.md
    ├── AGENTS.md
    ├── module.toml              # Canonical typed source
    ├── questions.md             # Generated learning questions
    ├── keys-to-success.md       # Generated study guide
    ├── practice-quiz.md         # Generated practice quiz
    ├── resources/               # Optional module-local assets
    └── output/                  # Generated — do not edit by hand
        ├── study-guides/        # PDF, DOCX, MD by default
        └── website/             # index.html
```

Lecture slide PDFs live under **[../resources/slides/](../resources/slides/)**, not inside each module.

## Module Contents

Each module directory contains:

- **module.toml**: Canonical typed source for topics, contents, terms, learning questions, quiz items, linked lab, and generated visuals
- **output/**: Generated multi-format outputs (PDF, DOCX, MD by default; HTML, TXT, and MP3 are opt-in) and `website/index.html`
- **resources/** (optional): Supplementary materials for that module only

## Related Documentation

- **[../README.md](../README.md)**: BIOL-1 course overview
- **[../AGENTS.md](../AGENTS.md)**: Course-level technical documentation
- **[../syllabus/](../syllabus/)**: Course syllabus in multiple formats
- **[../private/](../private/)**: Instructor-only materials
- **[../resources/](../resources/)**: Course-level resources
