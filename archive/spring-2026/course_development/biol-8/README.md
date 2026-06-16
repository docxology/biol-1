# BIOL-8: Human Biology

**College of the Redwoods | Del Norte Campus | Spring 2026**

Human biology course exploring the structure and function of the human body, from cellular foundations through organ systems, ecology, and evolution. This course is structured as **17** weekly modules with integrated study materials, laboratory protocols, assessments, and interactive dashboards.

---

## Directory Structure

```
biol-8/
├── course/              # All course content organized by module
│   ├── module-01 → 17/  # Weekly modules (keys-to-success + questions)
│   ├── labs/            # Laboratory protocols and interactive dashboards
│   ├── exams/           # 3 unit exams + keys (final when added)
│   └── quizzes/         # 17 module quizzes + 17 keys
├── syllabus/            # Syllabus and schedule (5 output formats)
├── resources/           # Textbook PDF
├── private/             # Instructor-only materials
└── README.md            # ← You are here
```

---

## Modules

Each module contains two source files (`keys-to-success.md`, `questions.md`) and an `output/` directory with generated study guides (PDF, DOCX, MD in the current publish profile) and an interactive website (`index.html`).

| # | Module | Topic | Source |
|---|--------|-------|--------|
| 01 | [Exploring Life Science](course/module-01-exploring-life-science/) | Scientific method, characteristics of life, levels of organization | [Keys](course/module-01-exploring-life-science/keys-to-success.md) · [Questions](course/module-01-exploring-life-science/questions.md) |
| 02 | [Chemistry of Life](course/module-02-chemistry-of-life/) | Atoms, bonds, water, pH, chemical reactions | [Keys](course/module-02-chemistry-of-life/keys-to-success.md) · [Questions](course/module-02-chemistry-of-life/questions.md) |
| 03 | [Biomolecules](course/module-03-biomolecules/) | Carbohydrates, lipids, proteins, nucleic acids | [Keys](course/module-03-biomolecules/keys-to-success.md) · [Questions](course/module-03-biomolecules/questions.md) |
| 04 | [Cellular Function](course/module-04-cellular-function/) | Cell structure, organelles, cell theory | [Keys](course/module-04-cellular-function/keys-to-success.md) · [Questions](course/module-04-cellular-function/questions.md) |
| 05 | [Membranes](course/module-05-membranes/) | Membrane structure, transport, osmosis, diffusion | [Keys](course/module-05-membranes/keys-to-success.md) · [Questions](course/module-05-membranes/questions.md) |
| 06 | [Metabolism](course/module-06-metabolism/) | Enzymes, energy, ATP, metabolic pathways | [Keys](course/module-06-metabolism/keys-to-success.md) · [Questions](course/module-06-metabolism/questions.md) |
| 07 | [Genetics & Central Dogma](course/module-07-genetics/) | DNA structure, transcription, translation, genetic code | [Keys](course/module-07-genetics/keys-to-success.md) · [Questions](course/module-07-genetics/questions.md) |
| 08 | [Cell Division: Mitosis & Meiosis](course/module-08-cell-division/) | Cell cycle, mitosis phases, meiosis I & II, genetic variation | [Keys](course/module-08-cell-division/keys-to-success.md) · [Questions](course/module-08-cell-division/questions.md) |
| 09 | [Tissues](course/module-09-tissues/) | Epithelial, connective, muscle, nervous tissue | [Keys](course/module-09-tissues/keys-to-success.md) · [Questions](course/module-09-tissues/questions.md) |
| 10 | [Inheritance](course/module-10-inheritance/) | Mendelian genetics, pedigrees, complex traits | [Keys](course/module-10-inheritance/keys-to-success.md) · [Questions](course/module-10-inheritance/questions.md) |
| 11 | [Skeletal System](course/module-11-skeletal-system/) | Bone structure, joints, skeletal divisions | [Keys](course/module-11-skeletal-system/keys-to-success.md) · [Questions](course/module-11-skeletal-system/questions.md) |
| 12 | [Muscular System](course/module-12-muscular-system/) | Muscle tissue, contraction, skeletal muscle | [Keys](course/module-12-muscular-system/keys-to-success.md) · [Questions](course/module-12-muscular-system/questions.md) |
| 13 | [Nervous System](course/module-13-nervous-system/) | Neurons, CNS/PNS, brain regions, autonomic division | [Keys](course/module-13-nervous-system/keys-to-success.md) · [Questions](course/module-13-nervous-system/questions.md) |
| 14 | [Microbiology](course/module-14-microbiology/) | Pathogens, microbiome, immunity, public health | [Keys](course/module-14-microbiology/keys-to-success.md) · [Questions](course/module-14-microbiology/questions.md) |
| 15 | [Cardiopulmonary System](course/module-15-cardiopulmonary-system/) | Heart, vessels, lungs, gas exchange | [Keys](course/module-15-cardiopulmonary-system/keys-to-success.md) · [Questions](course/module-15-cardiopulmonary-system/questions.md) |
| 16 | [Ecology](course/module-16-ecology/) | Populations, communities, ecosystems | [Keys](course/module-16-ecology/keys-to-success.md) · [Questions](course/module-16-ecology/questions.md) |
| 17 | [Evolution](course/module-17-evolution/) | Natural selection, evidence, human evolution | [Keys](course/module-17-evolution/keys-to-success.md) · [Questions](course/module-17-evolution/questions.md) |

### Module Output Formats

Each module's `output/` directory contains:

- **Study Guides** (`output/study-guides/`): PDF, DOCX, MD in the current publish profile; HTML, TXT, and MP3 are optional formats.
- **Interactive Website** (`output/website/index.html`): Self-contained HTML study portal

---

## Laboratory Protocols

Labs are located in [`course/labs/`](course/labs/). Each lab is a Markdown file using specialized directives for interactive elements. See the [Labs README](course/labs/README.md) for full directive syntax and generation instructions.

### Lab Directives

- `<!-- lab:data-table rows=N -->` - Fillable data collection tables
- `<!-- lab:object-selection -->` - Object selection fields
- `<!-- lab:measurement-feasibility -->` - Constraint evaluation
- `<!-- lab:calculation -->` - Formula and calculation areas
- `<!-- lab:reflection -->` - Open-ended response boxes
- `{fill:text}`, `{fill:number}`, `{fill:textarea rows=N}` - Inline fillable fields

### Lab Inventory

| # | Lab | Topic | Status |
|---|-----|-------|--------|
| 01 | [Lab 01](course/labs/lab-01_measurement-methods.md) | Introduction to Scientific Measurement | Complete |
| 02 | [Lab 02](course/labs/lab-02_probability-statistics.md) | Probability and Statistics | Complete |
| 03 | [Lab 03](course/labs/lab-03_microscopy.md) | Introduction to Microscopy | Complete |
| 04 | [Lab 04](course/labs/lab-04_diffusion-membranes.md) | Diffusion and Membranes | Complete |
| 05 | [Lab 05](course/labs/lab-05_ph-solutions.md) | pH and Solutions | Complete |
| 06 | [Lab 06](course/labs/lab-06_central-dogma.md) | Central Dogma: DNA → RNA → Protein | Complete |
| 07 | [Lab 07](course/labs/lab-07_cell-division.md) | Cell Division: Mitosis & Meiosis | Complete |
| 08 | [Lab 08](course/labs/lab-08_enzymes.md) | Chicken Liver Enzyme Activity | Complete |
| 09 | [Lab 09](course/labs/lab-09_inheritance.md) | Inheritance | Complete |
| 10 | [Lab 10](course/labs/lab-10_review.md) | Review | Complete |
| 11 | [Lab 11](course/labs/lab-11_skeletal-system.md) | Skeletal System | Complete |
| 12 | [Lab 12](course/labs/lab-12_muscular-system.md) | Muscular System | Complete |
| 13 | [Lab 13](course/labs/lab-13_nervous-system.md) | Nervous System | Complete |
| 14 | [Lab 14](course/labs/lab-14_microbiology.md) | Microbiology | Complete |
| 15 | [Lab 15](course/labs/lab-15_cardiopulmonary-system.md) | Cardiopulmonary System | Complete |
| 16 | [Lab 16](course/labs/lab-16_exam-03-review.md) | Exam 03 Review | Complete |
| 17 | [Lab 17](course/labs/lab-17_ecology.md) | Ecology | Complete |
| 18 | [Lab 18](course/labs/lab-18_evolution.md) | Evolution | Complete |

### Lab Output

Generated lab outputs are in [`course/labs/output/`](course/labs/output/):

- [Lab 01 PDF](course/labs/output/pdf/lab-01_measurement-methods.pdf)
- [Lab 02 PDF](course/labs/output/pdf/lab-02_probability-statistics.pdf)

### Interactive Dashboards

Most labs have one companion interactive HTML dashboard in [`course/labs/dashboards/`](course/labs/dashboards/); **Lab 15** has two (cardiovascular and respiratory) for the single cardiopulmonary protocol. Dashboards are self-contained HTML with inline CSS/JS and canvas sections where noted.

| # | Dashboard |
|---|-----------|
| 01 | [Measurement Methods](course/labs/dashboards/lab-01_measurement-methods-dashboard.html) |
| 02 | [Probability & Statistics](course/labs/dashboards/lab-02_probability-statistics-dashboard.html) |
| 03 | [Microscopy](course/labs/dashboards/lab-03_microscopy-dashboard.html) |
| 04 | [Diffusion and Membranes](course/labs/dashboards/lab-04_diffusion-membranes-dashboard.html) |
| 05 | [pH and Solutions](course/labs/dashboards/lab-05_ph-solutions-dashboard.html) |
| 06 | [Central Dogma](course/labs/dashboards/lab-06_central-dogma-dashboard.html) |
| 07 | [Cell Division](course/labs/dashboards/lab-07_cell-division-dashboard.html) |
| 08 | [Enzymes](course/labs/dashboards/lab-08_enzymes-dashboard.html) |
| 09 | [Inheritance](course/labs/dashboards/lab-09_inheritance-dashboard.html) |
| 10 | [Modules 07–10 Review](course/labs/dashboards/lab-10_review-dashboard.html) |
| 11 | [Skeletal System](course/labs/dashboards/lab-11_skeletal-system-dashboard.html) |
| 12 | [Muscular System](course/labs/dashboards/lab-12_muscular-system-dashboard.html) |
| 13 | [Nervous System](course/labs/dashboards/lab-13_nervous-system-dashboard.html) |
| 14 | [Microbiology](course/labs/dashboards/lab-14_microbiology-dashboard.html) |
| 15 | [Cardiovascular](course/labs/dashboards/lab-15_cardiovascular-system-dashboard.html) (pairs with [Lab 15](course/labs/lab-15_cardiopulmonary-system.md)) |
| 15 | [Respiratory](course/labs/dashboards/lab-15_respiratory-system-dashboard.html) (pairs with [Lab 15](course/labs/lab-15_cardiopulmonary-system.md)) |
| 16 | [Exam 03 Review](course/labs/dashboards/lab-16_exam-03-review-dashboard.html) |
| 17 | [Ecology](course/labs/dashboards/lab-17_ecology-dashboard.html) |
| 18 | [Evolution](course/labs/dashboards/lab-18_evolution-dashboard.html) |

---

## Assessments

### Exams

Three unit exams with answer keys are in [`course/exams/`](course/exams/). A comprehensive final may be added later.

| Exam | Questions | Answer Key |
|------|-----------|------------|
| Exam 1 | [exam-01.md](course/exams/exam-01.md) | [exam-01_key.md](course/exams/exam-01_key.md) |
| Exam 2 | [exam-02.md](course/exams/exam-02.md) | [exam-02_key.md](course/exams/exam-02_key.md) |
| Exam 3 | [exam-03.md](course/exams/exam-03.md) | [exam-03_key.md](course/exams/exam-03_key.md) |

### Quizzes

Seventeen module quizzes with answer keys are in [`course/quizzes/`](course/quizzes/):

| Module | Quiz | Answer Key |
|--------|------|------------|
| 01 | [module-01_quiz.md](course/quizzes/module-01_quiz.md) | [module-01_quiz_key.md](course/quizzes/module-01_quiz_key.md) |
| 02 | [module-02_quiz.md](course/quizzes/module-02_quiz.md) | [module-02_quiz_key.md](course/quizzes/module-02_quiz_key.md) |
| 03 | [module-03_quiz.md](course/quizzes/module-03_quiz.md) | [module-03_quiz_key.md](course/quizzes/module-03_quiz_key.md) |
| 04 | [module-04_quiz.md](course/quizzes/module-04_quiz.md) | [module-04_quiz_key.md](course/quizzes/module-04_quiz_key.md) |
| 05 | [module-05_quiz.md](course/quizzes/module-05_quiz.md) | [module-05_quiz_key.md](course/quizzes/module-05_quiz_key.md) |
| 06 | [module-06_quiz.md](course/quizzes/module-06_quiz.md) | [module-06_quiz_key.md](course/quizzes/module-06_quiz_key.md) |
| 07 | [module-07_quiz.md](course/quizzes/module-07_quiz.md) | [module-07_quiz_key.md](course/quizzes/module-07_quiz_key.md) |
| 08 | [module-08_quiz.md](course/quizzes/module-08_quiz.md) | [module-08_quiz_key.md](course/quizzes/module-08_quiz_key.md) |
| 09 | [module-09_quiz.md](course/quizzes/module-09_quiz.md) | [module-09_quiz_key.md](course/quizzes/module-09_quiz_key.md) |
| 10 | [module-10_quiz.md](course/quizzes/module-10_quiz.md) | [module-10_quiz_key.md](course/quizzes/module-10_quiz_key.md) |
| 11 | [module-11_quiz.md](course/quizzes/module-11_quiz.md) | [module-11_quiz_key.md](course/quizzes/module-11_quiz_key.md) |
| 12 | [module-12_quiz.md](course/quizzes/module-12_quiz.md) | [module-12_quiz_key.md](course/quizzes/module-12_quiz_key.md) |
| 13 | [module-13_quiz.md](course/quizzes/module-13_quiz.md) | [module-13_quiz_key.md](course/quizzes/module-13_quiz_key.md) |
| 14 | [module-14_quiz.md](course/quizzes/module-14_quiz.md) | [module-14_quiz_key.md](course/quizzes/module-14_quiz_key.md) |
| 15 | [module-15_quiz.md](course/quizzes/module-15_quiz.md) | [module-15_quiz_key.md](course/quizzes/module-15_quiz_key.md) |
| 16 | [module-16_quiz.md](course/quizzes/module-16_quiz.md) | [module-16_quiz_key.md](course/quizzes/module-16_quiz_key.md) |
| 17 | [module-17_quiz.md](course/quizzes/module-17_quiz.md) | [module-17_quiz_key.md](course/quizzes/module-17_quiz_key.md) |

---

## Syllabus & Schedule

Source files and multi-format outputs are in [`syllabus/`](syllabus/).

| Document | Source | PDF | DOCX | MD |
|----------|--------|-----|------|----|
| Syllabus | [Source](syllabus/BIOL-8_Spring-2026_Syllabus.md) | [PDF](syllabus/output/BIOL-8_Spring-2026_Syllabus.pdf) | [DOCX](syllabus/output/BIOL-8_Spring-2026_Syllabus.docx) | [MD](syllabus/output/BIOL-8_Spring-2026_Syllabus.md) |
| Schedule | [Source](syllabus/Schedule.md) | [PDF](syllabus/output/Schedule.pdf) | [DOCX](syllabus/output/Schedule.docx) | [MD](syllabus/output/Schedule.md) |

---

## Resources

- Lecture slides and supporting course resources are listed in [`resources/README.md`](resources/README.md).

---

## Output Generation

All course outputs are generated by the [`software/`](../../software/) module. See the [Software README](../../software/README.md) for build instructions.

```bash
cd software

# Generate all BIOL-8 outputs
uv run python scripts/generate_all_outputs.py --course biol-8

# Generate a single module
uv run python scripts/generate_module_renderings.py --course biol-8 --module 1

# Generate a single lab
uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-01_measurement-methods.md',
    '../course_development/biol-8/course/labs/output/lab-01_measurement-methods.pdf',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"

# Publish to PUBLISHED/ directory
uv run python scripts/publish_course.py --course biol-8
```

---

## Documentation

- [Course AGENTS.md](AGENTS.md) - Technical documentation for course structure and management
- [Course Content README](course/README.md) - Course-level content overview
- [Labs README](course/labs/README.md) - Lab directive syntax and generation instructions
- [Syllabus README](syllabus/README.md) - Syllabus document details
- [Resources README](resources/README.md) - Supplementary materials index
