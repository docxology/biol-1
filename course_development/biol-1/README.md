# BIOL-1: General Biology

**College of the Redwoods | Pelican Bay | Fall 2026**

Introductory biology course covering the fundamental principles of life science, from the molecular level through evolution and ecology. This course is structured as **16** content modules with integrated study materials, laboratory protocols, and assessments.

---

## Directory Structure

```
biol-1/
├── course/              # All course content organized by module
│   ├── module-01 → 16/  # Content modules (module.toml → generated study materials)
│   ├── labs/            # Laboratory protocols and interactive dashboards
│   ├── exams/           # Exams and answer keys
│   ├── practice_tests/  # Practice tests
│   └── quizzes/         # Quiz templates
├── syllabus/            # Syllabus and schedule (multi-format outputs)
├── resources/           # Lecture slides (PDF)
├── private/             # Instructor-only materials
└── README.md            # ← You are here
```

---

## Modules

Each module contains two source files (`keys-to-success.md`, `questions.md`) and an `output/` directory with generated study guides (PDF, DOCX, MD in the current publish profile) and an interactive website (`index.html`).

| # | Module | Topic | Source |
|---|--------|-------|--------|
| 01 | [The Study of Life](course/module-01-study-of-life/) | Nature of science, scientific method, characteristics of life | [Keys](course/module-01-study-of-life/keys-to-success.md) · [Questions](course/module-01-study-of-life/questions.md) |
| 02 | [Basic Chemistry](course/module-02-basic-chemistry/) | Atoms, bonds, water, pH, chemical reactions | [Keys](course/module-02-basic-chemistry/keys-to-success.md) · [Questions](course/module-02-basic-chemistry/questions.md) |
| 03 | [Organic Molecules](course/module-03-organic-molecules/) | Carbohydrates, lipids, proteins, nucleic acids | [Keys](course/module-03-organic-molecules/keys-to-success.md) · [Questions](course/module-03-organic-molecules/questions.md) |
| 04 | [Cells](course/module-04-cells/) | Cell theory, prokaryotic/eukaryotic structure, organelles | [Keys](course/module-04-cells/keys-to-success.md) · [Questions](course/module-04-cells/questions.md) |
| 05 | [Membranes](course/module-05-membranes/) | Membrane structure, transport, osmosis, diffusion | [Keys](course/module-05-membranes/keys-to-success.md) · [Questions](course/module-05-membranes/questions.md) |
| 06 | [Metabolism](course/module-06-metabolism/) | Enzymes, energy, ATP, metabolic pathways | [Keys](course/module-06-metabolism/keys-to-success.md) · [Questions](course/module-06-metabolism/questions.md) |
| 07 | [Molecular Genetics](course/module-07-molecular-genetics/) | DNA structure, replication, transcription, translation, genetic code | [Keys](course/module-07-molecular-genetics/keys-to-success.md) · [Questions](course/module-07-molecular-genetics/questions.md) |
| 08 | [Cellular Genetics](course/module-08-cellular-genetics/) | Cell cycle, mitosis, meiosis, genetic variation | [Keys](course/module-08-cellular-genetics/keys-to-success.md) · [Questions](course/module-08-cellular-genetics/questions.md) |
| 09 | [Inheritance Genetics](course/module-09-inheritance-genetics/) | Mendelian genetics, Punnett squares, polygenic traits, pedigrees | [Keys](course/module-09-inheritance-genetics/keys-to-success.md) · [Questions](course/module-09-inheritance-genetics/questions.md) |
| 10 | [Epigenetics](course/module-10-epigenetics/) | Gene regulation, epigenetic mechanisms, methylation, histone modification | [Keys](course/module-10-epigenetics/keys-to-success.md) · [Questions](course/module-10-epigenetics/questions.md) |
| 11 | [Genomics & Biotechnology](course/module-11-genomics-biotechnology/) | PCR, gel electrophoresis, CRISPR, genomic applications | [Keys](course/module-11-genomics-biotechnology/keys-to-success.md) · [Questions](course/module-11-genomics-biotechnology/questions.md) |
| 12 | [Darwin & Evolution](course/module-12-darwin-evolution/) | Natural selection, evidence for evolution, Darwin's theory | [Keys](course/module-12-darwin-evolution/keys-to-success.md) · [Questions](course/module-12-darwin-evolution/questions.md) |
| 13 | [How Populations Evolve](course/module-13-how-populations-evolve/) | Microevolution, Hardy-Weinberg, genetic drift, gene flow | [Keys](course/module-13-how-populations-evolve/keys-to-success.md) · [Questions](course/module-13-how-populations-evolve/questions.md) |
| 14 | [Macroevolution](course/module-14-macroevolution/) | Species concepts, speciation, phylogenetics | [Keys](course/module-14-macroevolution/keys-to-success.md) · [Questions](course/module-14-macroevolution/questions.md) |
| 15 | [Population, Systems & Ecology](course/module-15-population-systems-ecology/) | Population dynamics, community interactions, ecosystems | [Keys](course/module-15-population-systems-ecology/keys-to-success.md) · [Questions](course/module-15-population-systems-ecology/questions.md) |
| 16 | [Capstone Systems Synthesis](course/module-16-capstone-systems-synthesis/) | Cross-scale synthesis, feedback loops, evidence-based explanations | [Keys](course/module-16-capstone-systems-synthesis/keys-to-success.md) · [Questions](course/module-16-capstone-systems-synthesis/questions.md) |

### Module Output Formats

Each module's `output/` directory contains:

- **Study Guides** (`output/study-guides/`): PDF, DOCX, MD in the current publish profile; HTML, TXT, and MP3 are optional formats.
- **Interactive Website** (`output/website/index.html`): Self-contained HTML study portal

---

## Laboratory Protocols

Labs are located in [`course/labs/`](course/labs/). Each lab is a Markdown file using specialized directives for interactive elements (data tables, fillable fields, reflection boxes, calculation areas). See the [Labs README](course/labs/README.md) for full directive syntax.

| # | Lab | Topic | Status |
|---|-----|-------|--------|
| 01 | [Lab 01](course/labs/lab-01_measurement-methods.md) | Introduction to Scientific Measurement | Complete |
| 02 | [Lab 02](course/labs/lab-02_probability-statistics.md) | Probability and Statistics | Complete |
| 03 | [Lab 03](course/labs/lab-03_microscopy.md) | Introduction to Microscopy | Complete |
| 04 | [Lab 04](course/labs/lab-04_liquid-chemistry.md) | Liquid Chemistry | Complete |
| 05 | [Lab 05](course/labs/lab-05_viewing-life.md) | Viewing Life | Complete |
| 06 | [Lab 06](course/labs/lab-06_metabolism.md) | Metabolism | Complete |
| 07 | [Lab 07](course/labs/lab-07_molecular-genetics.md) | Molecular Genetics | Complete |
| 08 | [Lab 08](course/labs/lab-08_cellular-genetics.md) | Cellular Genetics (Mitosis & Meiosis) | Complete |
| 09 | [Lab 09](course/labs/lab-09_inheritance-genetics.md) | Inheritance Genetics | Complete |
| 10 | [Lab 10](course/labs/lab-10_epigenetics.md) | Epigenetics | Complete |
| 11 | [Lab 11](course/labs/lab-11_genomics-biotechnology.md) | Genomics & Biotechnology | Complete |
| 12 | [Lab 12](course/labs/lab-12_darwin-evolution.md) | Darwin & Evolution | Complete |
| 13 | [Lab 13](course/labs/lab-13_how-populations-evolve.md) | How Populations Evolve | Complete |
| 14 | [Lab 14](course/labs/lab-14_macroevolution.md) | Macroevolution | Complete |
| 15 | [Lab 15](course/labs/lab-15_population-systems-ecology.md) | Population, Systems & Ecology | Complete |
| 16 | [Lab 16](course/labs/lab-16_capstone-systems-synthesis.md) | Capstone Systems Synthesis | Complete |

### Lab Output

Generated lab outputs are in [`course/labs/output/`](course/labs/output/):

- [Lab 01 PDF](course/labs/output/pdf/lab-01_measurement-methods.pdf)
- [Lab 02 PDF](course/labs/output/pdf/lab-02_probability-statistics.pdf)

### Interactive Dashboards

Each lab has a companion interactive HTML dashboard in [`course/labs/dashboards/`](course/labs/dashboards/). Dashboards are self-contained HTML files with inline CSS/JS, canvas-based charting, and auto-saving fillable fields.

| # | Dashboard |
|---|-----------|
| 01 | [Measurement Methods](course/labs/dashboards/lab-01_measurement-methods-dashboard.html) |
| 02 | [Probability & Statistics](course/labs/dashboards/lab-02_probability-statistics-dashboard.html) |
| 03 | [Microscopy](course/labs/dashboards/lab-03_microscopy-dashboard.html) |
| 04 | [Liquid Chemistry](course/labs/dashboards/lab-04_liquid-chemistry-dashboard.html) |
| 05 | [Viewing Life](course/labs/dashboards/lab-05_viewing-life-dashboard.html) |
| 06 | [Metabolism](course/labs/dashboards/lab-06_metabolism-dashboard.html) |
| 07 | [Molecular Genetics](course/labs/dashboards/lab-07_molecular-genetics-dashboard.html) |
| 08 | [Cellular Genetics](course/labs/dashboards/lab-08_cellular-genetics-dashboard.html) |
| 09 | [Inheritance Genetics](course/labs/dashboards/lab-09_inheritance-genetics-dashboard.html) |
| 10 | [Epigenetics](course/labs/dashboards/lab-10_epigenetics-dashboard.html) |
| 11 | [Genomics & Biotechnology](course/labs/dashboards/lab-11_genomics-biotechnology-dashboard.html) |
| 12 | [Darwin & Evolution](course/labs/dashboards/lab-12_darwin-evolution-dashboard.html) |
| 13 | [How Populations Evolve](course/labs/dashboards/lab-13_how-populations-evolve-dashboard.html) |
| 14 | [Macroevolution](course/labs/dashboards/lab-14_macroevolution-dashboard.html) |
| 15 | [Population and Systems Ecology](course/labs/dashboards/lab-15_population-systems-ecology-dashboard.html) |
| 16 | [Capstone Systems Synthesis](course/labs/dashboards/lab-16_capstone-systems-synthesis-dashboard.html) |

---

## Assessments

### Exams

Exams and answer keys are in [`course/exams/`](course/exams/):

- [Exam 01](course/exams/exam-01.md) · [Key](course/exams/exam-01_key.md)
- [Exam 02](course/exams/exam-02.md) · [Key](course/exams/exam-02_key.md)
- [Exam 03](course/exams/exam-03.md) · [Key](course/exams/exam-03_key.md)
- [Comprehensive final](course/exams/final-exam.md) · [Key](course/exams/final-exam_key.md)
- [Exam Template](course/exams/exam-template.md)

### Quizzes

Quiz templates are in [`course/quizzes/`](course/quizzes/):

- [Quiz Template](course/quizzes/quiz-template.md)

---

## Syllabus & Schedule

Source files and multi-format outputs are in [`syllabus/`](syllabus/).

| Document | Source | PDF | DOCX | MD |
|----------|--------|-----|------|----|
| Syllabus | [Source](syllabus/BIOL-1_Fall-2026_Syllabus.md) | [PDF](syllabus/output/BIOL-1_Fall-2026_Syllabus.pdf) | [DOCX](syllabus/output/BIOL-1_Fall-2026_Syllabus.docx) | [MD](syllabus/output/BIOL-1_Fall-2026_Syllabus.md) |
| Schedule | [Source](syllabus/Schedule.md) | [PDF](syllabus/output/Schedule.pdf) | [DOCX](syllabus/output/Schedule.docx) | [MD](syllabus/output/Schedule.md) |

---

## Resources

### Lecture Slides

Slides are in [`resources/slides/`](resources/slides/) as PDF files in two formats: full-page and with speaker notes.

| Module | Full Slides | With Notes |
|--------|-------------|------------|
| 01 | [Full](resources/slides/module-1-slides-full.pdf) | [Notes](resources/slides/module-1-slides-notes.pdf) |
| 02 | [Full](resources/slides/module-2-slides-full.pdf) | [Notes](resources/slides/module-2-slides-notes.pdf) |
| 03 | [Full](resources/slides/module-3-slides-full.pdf) | [Notes](resources/slides/module-3-slides-notes.pdf) |
| 04 | [Full](resources/slides/module-4-slides-full.pdf) | [Notes](resources/slides/module-4-slides-notes.pdf) |
| 05 | [Full](resources/slides/module-5-slides-full.pdf) | [Notes](resources/slides/module-5-slides-notes.pdf) |
| 06 | [Full](resources/slides/module-6-slides-full.pdf) | [Notes](resources/slides/module-6-slides-notes.pdf) |
| 07 | [Full](resources/slides/module-7-slides-full.pdf) | [Notes](resources/slides/module-7-slides-notes.pdf) |
| 08 | [Cell cycle full](resources/slides/module-8-slides-cell-cycle-full.pdf) | [Cell cycle notes](resources/slides/module-8-slides-cell-cycle-notes.pdf) |
| 08 | [Meiosis full](resources/slides/module-8-slides-meiosis-full.pdf) | [Meiosis notes](resources/slides/module-8-slides-meiosis-notes.pdf) |
| 09 | [Full](resources/slides/module-9-slides-full.pdf) | [Notes](resources/slides/module-9-slides-notes.pdf) |
| 10 | [Full](resources/slides/module-10-slides-full.pdf) | [Notes](resources/slides/module-10-slides-notes.pdf) |
| 11 | [Full](resources/slides/module-11-slides-full.pdf) | [Notes](resources/slides/module-11-slides-notes.pdf) |
| 12 | Not available | Not available |
| 13 | Not available | Not available |
| 14 | [Full](resources/slides/module-14-slides-full.pdf) | [Notes](resources/slides/module-14-slides-notes.pdf) |
| 15 | Not available | Not available |
| 16 | Not available | Not available |

---

## Output Generation

All course outputs are generated by the [`software/`](../../software/) module. See the [Software README](../../software/README.md) for build instructions.

```bash
cd software

# Generate all BIOL-1 outputs
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate a single module
uv run python scripts/generate_module_renderings.py --course biol-1 --module 1

# Publish to PUBLISHED/ directory
uv run python scripts/publish_course.py --course biol-1
```

---

## Documentation

- [Course AGENTS.md](AGENTS.md) - Technical documentation for course structure and management
- [Course Content README](course/README.md) - Course-level content overview
- [Labs README](course/labs/README.md) - Lab directive syntax and generation instructions
- [Syllabus README](syllabus/README.md) - Syllabus document details
- [Resources README](resources/README.md) - Supplementary materials index
