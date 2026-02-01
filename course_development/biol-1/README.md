# BIOL-1: General Biology

**College of the Redwoods | Pelican Bay | Spring 2026**

Introductory biology course covering the fundamental principles of life science, from the molecular level through evolution. This course is structured as 17 weekly modules with integrated study materials, laboratory protocols, and assessments.

---

## Directory Structure

```
biol-1/
├── course/              # All course content organized by module
│   ├── module-01 → 17/  # Weekly modules (keys-to-success + questions)
│   ├── labs/            # Laboratory protocols and interactive dashboards
│   ├── exams/           # Exam templates
│   └── quizzes/         # Quiz templates
├── syllabus/            # Syllabus and schedule (5 output formats)
├── resources/           # Lecture slides (PDF)
├── private/             # Instructor-only materials
└── README.md            # ← You are here
```

---

## Modules

Each module contains two source files (`keys-to-success.md`, `questions.md`) and an `output/` directory with generated study guides (PDF, DOCX, HTML, TXT, MP3) and an interactive website (`index.html`).

| # | Module | Topic | Source |
|---|--------|-------|--------|
| 01 | [The Study of Life](course/module-01-study-of-life/) | Nature of science, scientific method, characteristics of life | [Keys](course/module-01-study-of-life/keys-to-success.md) · [Questions](course/module-01-study-of-life/questions.md) |
| 02 | [Basic Chemistry](course/module-02-basic-chemistry/) | Atoms, bonds, water, pH, chemical reactions | [Keys](course/module-02-basic-chemistry/keys-to-success.md) · [Questions](course/module-02-basic-chemistry/questions.md) |
| 03 | [Organic Molecules](course/module-03-organic-molecules/) | Carbohydrates, lipids, proteins, nucleic acids | [Keys](course/module-03-organic-molecules/keys-to-success.md) · [Questions](course/module-03-organic-molecules/questions.md) |
| 04 | [Cells](course/module-04-cells/) | Cell theory, prokaryotic/eukaryotic structure, organelles | [Keys](course/module-04-cells/keys-to-success.md) · [Questions](course/module-04-cells/questions.md) |
| 05 | [Membranes](course/module-05-membranes/) | Membrane structure, transport, osmosis, diffusion | [Keys](course/module-05-membranes/keys-to-success.md) · [Questions](course/module-05-membranes/questions.md) |
| 06 | [Metabolism](course/module-06-metabolism/) | Enzymes, energy, ATP, metabolic pathways | [Keys](course/module-06-metabolism/keys-to-success.md) · [Questions](course/module-06-metabolism/questions.md) |
| 07 | [Photosynthesis](course/module-07-photosynthesis/) | Light reactions, Calvin cycle, chloroplast structure | [Keys](course/module-07-photosynthesis/keys-to-success.md) · [Questions](course/module-07-photosynthesis/questions.md) |
| 08 | [Cellular Respiration](course/module-08-cellular-respiration/) | Glycolysis, Krebs cycle, electron transport, fermentation | [Keys](course/module-08-cellular-respiration/keys-to-success.md) · [Questions](course/module-08-cellular-respiration/questions.md) |
| 09 | [Cell Division & Mitosis](course/module-09-cell-division-mitosis/) | Cell cycle, mitosis phases, cytokinesis, regulation | [Keys](course/module-09-cell-division-mitosis/keys-to-success.md) · [Questions](course/module-09-cell-division-mitosis/questions.md) |
| 10 | [Meiosis & Reproduction](course/module-10-meiosis-reproduction/) | Meiosis, gamete formation, genetic variation | [Keys](course/module-10-meiosis-reproduction/keys-to-success.md) · [Questions](course/module-10-meiosis-reproduction/questions.md) |
| 11 | [Mendelian Genetics](course/module-11-mendelian-genetics/) | Mendel's laws, Punnett squares, inheritance patterns | [Keys](course/module-11-mendelian-genetics/keys-to-success.md) · [Questions](course/module-11-mendelian-genetics/questions.md) |
| 12 | [Gene Expression](course/module-12-gene-expression/) | DNA replication, transcription, translation, genetic code | [Keys](course/module-12-gene-expression/keys-to-success.md) · [Questions](course/module-12-gene-expression/questions.md) |
| 13 | [Gene Regulation](course/module-13-gene-regulation/) | Operons, epigenetics, gene expression control | [Keys](course/module-13-gene-regulation/keys-to-success.md) · [Questions](course/module-13-gene-regulation/questions.md) |
| 14 | [Biotechnology & Genomics](course/module-14-biotechnology-genomics/) | PCR, gel electrophoresis, CRISPR, genomic applications | [Keys](course/module-14-biotechnology-genomics/keys-to-success.md) · [Questions](course/module-14-biotechnology-genomics/questions.md) |
| 15 | [Darwin & Evolution](course/module-15-darwin-evolution/) | Natural selection, evidence for evolution, Darwin's theory | [Keys](course/module-15-darwin-evolution/keys-to-success.md) · [Questions](course/module-15-darwin-evolution/questions.md) |
| 16 | [Microevolution](course/module-16-microevolution/) | Population genetics, Hardy-Weinberg, genetic drift, gene flow | [Keys](course/module-16-microevolution/keys-to-success.md) · [Questions](course/module-16-microevolution/questions.md) |
| 17 | [Speciation & Macroevolution](course/module-17-speciation-macroevolution/) | Species concepts, speciation mechanisms, phylogenetics | [Keys](course/module-17-speciation-macroevolution/keys-to-success.md) · [Questions](course/module-17-speciation-macroevolution/questions.md) |

### Module Output Formats

Each module's `output/` directory contains:

- **Study Guides** (`output/study-guides/`): PDF, DOCX, HTML, TXT, MP3
- **Interactive Website** (`output/website/index.html`): Self-contained HTML study portal

---

## Laboratory Protocols

Labs are located in [`course/labs/`](course/labs/). Each lab is a Markdown file using specialized directives for interactive elements (data tables, fillable fields, reflection boxes, calculation areas). See the [Labs README](course/labs/README.md) for full directive syntax.

| # | Lab | Topic | Status |
|---|-----|-------|--------|
| 01 | [Lab 01](course/labs/lab-01_measurement-methods.md) | Introduction to Scientific Measurement | Complete |
| 02 | [Lab 02](course/labs/lab-02_probability-statistics.md) | Probability and Statistics | Complete |
| 03 | [Lab 03](course/labs/lab-03_organic-molecules.md) | Organic Molecules | Stub |
| 04 | [Lab 04](course/labs/lab-04_cells.md) | Cells | Stub |
| 05 | [Lab 05](course/labs/lab-05_membranes.md) | Membranes | Stub |
| 06 | [Lab 06](course/labs/lab-06_metabolism.md) | Metabolism | Stub |
| 07 | [Lab 07](course/labs/lab-07_photosynthesis.md) | Photosynthesis | Stub |
| 08 | [Lab 08](course/labs/lab-08_cellular-respiration.md) | Cellular Respiration | Stub |
| 09 | [Lab 09](course/labs/lab-09_cell-division-mitosis.md) | Cell Division & Mitosis | Stub |
| 10 | [Lab 10](course/labs/lab-10_meiosis-reproduction.md) | Meiosis & Reproduction | Stub |
| 11 | [Lab 11](course/labs/lab-11_mendelian-genetics.md) | Mendelian Genetics | Stub |
| 12 | [Lab 12](course/labs/lab-12_gene-expression.md) | Gene Expression | Stub |
| 13 | [Lab 13](course/labs/lab-13_gene-regulation.md) | Gene Regulation | Stub |
| 14 | [Lab 14](course/labs/lab-14_biotechnology-genomics.md) | Biotechnology & Genomics | Stub |
| 15 | [Lab 15](course/labs/lab-15_darwin-evolution.md) | Darwin & Evolution | Stub |
| 16 | [Lab 16](course/labs/lab-16_microevolution.md) | Microevolution | Stub |
| 17 | [Lab 17](course/labs/lab-17_speciation-macroevolution.md) | Speciation & Macroevolution | Stub |

### Lab Output

Generated lab outputs are in [`course/labs/output/`](course/labs/output/):

- [Lab 01 PDF](course/labs/output/lab-01_measurement-methods.pdf) · [Lab 01 HTML](course/labs/output/lab-01_measurement-methods.html)
- [Lab 02 PDF](course/labs/output/lab-02_probability-statistics.pdf) · [Lab 02 HTML](course/labs/output/lab-02_probability-statistics.html)

### Interactive Dashboards

Each lab has a companion interactive HTML dashboard in [`course/labs/dashboards/`](course/labs/dashboards/). Dashboards are self-contained HTML files with inline CSS/JS, canvas-based charting, and auto-saving fillable fields.

| # | Dashboard |
|---|-----------|
| 01 | [Measurement Methods](course/labs/dashboards/lab-01_measurement-methods-dashboard.html) |
| 02 | [Probability & Statistics](course/labs/dashboards/lab-02_probability-statistics-dashboard.html) |
| 03 | [Organic Molecules](course/labs/dashboards/lab-03_organic-molecules-dashboard.html) |
| 04 | [Cells](course/labs/dashboards/lab-04_cells-dashboard.html) |
| 05 | [Membranes](course/labs/dashboards/lab-05_membranes-dashboard.html) |
| 06 | [Metabolism](course/labs/dashboards/lab-06_metabolism-dashboard.html) |
| 07 | [Photosynthesis](course/labs/dashboards/lab-07_photosynthesis-dashboard.html) |
| 08 | [Cellular Respiration](course/labs/dashboards/lab-08_cellular-respiration-dashboard.html) |
| 09 | [Cell Division & Mitosis](course/labs/dashboards/lab-09_cell-division-mitosis-dashboard.html) |
| 10 | [Meiosis & Reproduction](course/labs/dashboards/lab-10_meiosis-reproduction-dashboard.html) |
| 11 | [Mendelian Genetics](course/labs/dashboards/lab-11_mendelian-genetics-dashboard.html) |
| 12 | [Gene Expression](course/labs/dashboards/lab-12_gene-expression-dashboard.html) |
| 13 | [Gene Regulation](course/labs/dashboards/lab-13_gene-regulation-dashboard.html) |
| 14 | [Biotechnology & Genomics](course/labs/dashboards/lab-14_biotechnology-genomics-dashboard.html) |
| 15 | [Darwin & Evolution](course/labs/dashboards/lab-15_darwin-evolution-dashboard.html) |
| 16 | [Microevolution](course/labs/dashboards/lab-16_microevolution-dashboard.html) |
| 17 | [Speciation & Macroevolution](course/labs/dashboards/lab-17_speciation-macroevolution-dashboard.html) |

---

## Assessments

### Exams

Exam templates are in [`course/exams/`](course/exams/):

- [Exam Template](course/exams/exam-template.md)

### Quizzes

Quiz templates are in [`course/quizzes/`](course/quizzes/):

- [Quiz Template](course/quizzes/quiz-template.md)

---

## Syllabus & Schedule

Source files and multi-format outputs are in [`syllabus/`](syllabus/).

| Document | Source | PDF | DOCX | HTML | TXT | MP3 |
|----------|--------|-----|------|------|-----|-----|
| Syllabus | [Source](syllabus/BIOL-1_Spring-2026_Syllabus.md) | [PDF](syllabus/output/BIOL-1_Spring-2026_Syllabus.pdf) | [DOCX](syllabus/output/BIOL-1_Spring-2026_Syllabus.docx) | [HTML](syllabus/output/BIOL-1_Spring-2026_Syllabus.html) | [TXT](syllabus/output/BIOL-1_Spring-2026_Syllabus.txt) | [MP3](syllabus/output/BIOL-1_Spring-2026_Syllabus.mp3) |
| Schedule | [Source](syllabus/Schedule.md) | [PDF](syllabus/output/Schedule.pdf) | [DOCX](syllabus/output/Schedule.docx) | [HTML](syllabus/output/Schedule.html) | [TXT](syllabus/output/Schedule.txt) | [MP3](syllabus/output/Schedule.mp3) |

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
| 08 | [Full](resources/slides/module-8-slides-full.pdf) | [Notes](resources/slides/module-8-slides-notes.pdf) |
| 10 | [Full](resources/slides/module-10-slides-full.pdf) | [Notes](resources/slides/module-10-slides-notes.pdf) |
| 11 | [Full](resources/slides/module-11-slides-full.pdf) | [Notes](resources/slides/module-11-slides-notes.pdf) |
| 12 | [Full](resources/slides/module-12-slides-full.pdf) | [Notes](resources/slides/module-12-slides-notes.pdf) |
| 13 | [Full](resources/slides/module-13-slides-full.pdf) | [Notes](resources/slides/module-13-slides-notes.pdf) |
| 14 | [Full](resources/slides/module-14-slides-full.pdf) | [Notes](resources/slides/module-14-slides-notes.pdf) |
| 15 | [Full](resources/slides/module-15-slides-full.pdf) | [Notes](resources/slides/module-15-slides-notes.pdf) |
| 16 | [Full](resources/slides/module-16-slides-full.pdf) | [Notes](resources/slides/module-16-slides-notes.pdf) |

> Slides for modules 09 and 17 are not yet available.

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
