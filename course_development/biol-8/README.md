# BIOL-8: Human Biology

**College of the Redwoods | Del Norte Campus | Spring 2026**

Human biology course exploring the structure and function of the human body, from cellular foundations through organ systems. This course is structured as 15 weekly modules with integrated study materials, laboratory protocols, assessments, and interactive dashboards.

---

## Directory Structure

```
biol-8/
├── course/              # All course content organized by module
│   ├── module-01 → 15/  # Weekly modules (keys-to-success + questions)
│   ├── labs/            # Laboratory protocols and interactive dashboards
│   ├── exams/           # 4 exams with answer keys
│   └── quizzes/         # 15 module quizzes with answer keys
├── syllabus/            # Syllabus and schedule (5 output formats)
├── resources/           # Textbook PDF
├── private/             # Instructor-only materials
└── README.md            # ← You are here
```

---

## Modules

Each module contains two source files (`keys-to-success.md`, `questions.md`) and an `output/` directory with generated study guides (PDF, DOCX, HTML, TXT, MP3) and an interactive website (`index.html`).

| # | Module | Topic | Source |
|---|--------|-------|--------|
| 01 | [Exploring Life Science](course/module-01-exploring-life-science/) | Scientific method, characteristics of life, levels of organization | [Keys](course/module-01-exploring-life-science/keys-to-success.md) · [Questions](course/module-01-exploring-life-science/questions.md) |
| 02 | [Chemistry of Life](course/module-02-chemistry-of-life/) | Atoms, bonds, water, pH, chemical reactions | [Keys](course/module-02-chemistry-of-life/keys-to-success.md) · [Questions](course/module-02-chemistry-of-life/questions.md) |
| 03 | [Biomolecules](course/module-03-biomolecules/) | Carbohydrates, lipids, proteins, nucleic acids | [Keys](course/module-03-biomolecules/keys-to-success.md) · [Questions](course/module-03-biomolecules/questions.md) |
| 04 | [Cellular Function](course/module-04-cellular-function/) | Cell structure, organelles, cell theory | [Keys](course/module-04-cellular-function/keys-to-success.md) · [Questions](course/module-04-cellular-function/questions.md) |
| 05 | [Membranes](course/module-05-membranes/) | Membrane structure, transport, osmosis, diffusion | [Keys](course/module-05-membranes/keys-to-success.md) · [Questions](course/module-05-membranes/questions.md) |
| 06 | [Metabolism](course/module-06-metabolism/) | Enzymes, energy, ATP, metabolic pathways | [Keys](course/module-06-metabolism/keys-to-success.md) · [Questions](course/module-06-metabolism/questions.md) |
| 07 | [Mitosis](course/module-07-mitosis/) | Cell cycle, mitosis phases, cytokinesis, regulation | [Keys](course/module-07-mitosis/keys-to-success.md) · [Questions](course/module-07-mitosis/questions.md) |
| 08 | [Meiosis](course/module-08-meiosis/) | Meiosis, gamete formation, genetic variation | [Keys](course/module-08-meiosis/keys-to-success.md) · [Questions](course/module-08-meiosis/questions.md) |
| 09 | [Inheritance](course/module-09-inheritance/) | Mendel's laws, Punnett squares, inheritance patterns | [Keys](course/module-09-inheritance/keys-to-success.md) · [Questions](course/module-09-inheritance/questions.md) |
| 10 | [Tissues](course/module-10-tissues/) | Epithelial, connective, muscle, nervous tissue types | [Keys](course/module-10-tissues/keys-to-success.md) · [Questions](course/module-10-tissues/questions.md) |
| 11 | [Skeletal System](course/module-11-skeletal-system/) | Bone structure, joints, skeletal divisions | [Keys](course/module-11-skeletal-system/keys-to-success.md) · [Questions](course/module-11-skeletal-system/questions.md) |
| 12 | [Muscular System](course/module-12-muscular-system/) | Muscle types, contraction, skeletal muscle anatomy | [Keys](course/module-12-muscular-system/keys-to-success.md) · [Questions](course/module-12-muscular-system/questions.md) |
| 13 | [Pathogens](course/module-13-pathogens/) | Bacteria, viruses, fungi, immune response | [Keys](course/module-13-pathogens/keys-to-success.md) · [Questions](course/module-13-pathogens/questions.md) |
| 14 | [Cardiovascular System](course/module-14-cardiovascular-system/) | Heart, blood vessels, blood, circulation | [Keys](course/module-14-cardiovascular-system/keys-to-success.md) · [Questions](course/module-14-cardiovascular-system/questions.md) |
| 15 | [Respiratory System](course/module-15-respiratory-system/) | Lungs, gas exchange, breathing mechanics | [Keys](course/module-15-respiratory-system/keys-to-success.md) · [Questions](course/module-15-respiratory-system/questions.md) |

### Module Output Formats

Each module's `output/` directory contains:

- **Study Guides** (`output/study-guides/`): PDF, DOCX, HTML, TXT, MP3
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
| 03 | [Lab 03](course/labs/lab-03_measurement-techniques.md) | Measurement Techniques | Complete |
| 04 | [Lab 04](course/labs/lab-04_introduction-to-microscopy.md) | Introduction to Microscopy | Complete |
| 05 | [Lab 05](course/labs/lab-05_membranes.md) | Membranes | Stub |
| 06 | [Lab 06](course/labs/lab-06_metabolism.md) | Metabolism | Stub |
| 07 | [Lab 07](course/labs/lab-07_mitosis.md) | Mitosis | Stub |
| 08 | [Lab 08](course/labs/lab-08_meiosis.md) | Meiosis | Stub |
| 09 | [Lab 09](course/labs/lab-09_inheritance.md) | Inheritance | Stub |
| 10 | [Lab 10](course/labs/lab-10_tissues.md) | Tissues | Stub |
| 11 | [Lab 11](course/labs/lab-11_skeletal-system.md) | Skeletal System | Stub |
| 12 | [Lab 12](course/labs/lab-12_muscular-system.md) | Muscular System | Stub |
| 13 | [Lab 13](course/labs/lab-13_pathogens.md) | Pathogens | Stub |
| 14 | [Lab 14](course/labs/lab-14_cardiovascular-system.md) | Cardiovascular System | Stub |
| 15 | [Lab 15](course/labs/lab-15_respiratory-system.md) | Respiratory System | Stub |

### Lab Output

Generated lab outputs are in [`course/labs/output/`](course/labs/output/):

- [Lab 02 PDF](course/labs/output/lab-02_probability-statistics.pdf) · [Lab 02 HTML](course/labs/output/lab-02_probability-statistics.html)

### Interactive Dashboards

Each lab has a companion interactive HTML dashboard in [`course/labs/dashboards/`](course/labs/dashboards/). Dashboards are self-contained HTML files with inline CSS/JS, canvas-based charting, and auto-saving fillable fields.

| # | Dashboard |
|---|-----------|
| 01 | [Measurement Methods](course/labs/dashboards/lab-01_measurement-methods-dashboard.html) |
| 02 | [Probability & Statistics](course/labs/dashboards/lab-02_probability-statistics-dashboard.html) |
| 03 | [Measurement Techniques](course/labs/dashboards/lab-03_measurement-techniques-dashboard.html) |
| 04 | [Introduction to Microscopy](course/labs/dashboards/lab-04_introduction-to-microscopy-dashboard.html) |
| 05 | [Membranes](course/labs/dashboards/lab-05_membranes-dashboard.html) |
| 06 | [Metabolism](course/labs/dashboards/lab-06_metabolism-dashboard.html) |
| 07 | [Mitosis](course/labs/dashboards/lab-07_mitosis-dashboard.html) |
| 08 | [Meiosis](course/labs/dashboards/lab-08_meiosis-dashboard.html) |
| 09 | [Inheritance](course/labs/dashboards/lab-09_inheritance-dashboard.html) |
| 10 | [Tissues](course/labs/dashboards/lab-10_tissues-dashboard.html) |
| 11 | [Skeletal System](course/labs/dashboards/lab-11_skeletal-system-dashboard.html) |
| 12 | [Muscular System](course/labs/dashboards/lab-12_muscular-system-dashboard.html) |
| 13 | [Pathogens](course/labs/dashboards/lab-13_pathogens-dashboard.html) |
| 14 | [Cardiovascular System](course/labs/dashboards/lab-14_cardiovascular-system-dashboard.html) |
| 15 | [Respiratory System](course/labs/dashboards/lab-15_respiratory-system-dashboard.html) |

---

## Assessments

### Exams

Four exams with answer keys are in [`course/exams/`](course/exams/):

| Exam | Questions | Answer Key |
|------|-----------|------------|
| Exam 1 | [exam-01.md](course/exams/exam-01.md) | [exam-01_key.md](course/exams/exam-01_key.md) |
| Exam 2 | [exam-02.md](course/exams/exam-02.md) | [exam-02_key.md](course/exams/exam-02_key.md) |
| Exam 3 | [exam-03.md](course/exams/exam-03.md) | [exam-03_key.md](course/exams/exam-03_key.md) |
| Final Exam | [final-exam.md](course/exams/final-exam.md) | [final-exam_key.md](course/exams/final-exam_key.md) |

### Quizzes

Fifteen module quizzes with answer keys are in [`course/quizzes/`](course/quizzes/):

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

---

## Syllabus & Schedule

Source files and multi-format outputs are in [`syllabus/`](syllabus/).

| Document | Source | PDF | DOCX | HTML | TXT | MP3 |
|----------|--------|-----|------|------|-----|-----|
| Syllabus | [Source](syllabus/BIOL-8_Spring-2026_Syllabus.md) | [PDF](syllabus/output/BIOL-8_Spring-2026_Syllabus.pdf) | [DOCX](syllabus/output/BIOL-8_Spring-2026_Syllabus.docx) | [HTML](syllabus/output/BIOL-8_Spring-2026_Syllabus.html) | [TXT](syllabus/output/BIOL-8_Spring-2026_Syllabus.txt) | [MP3](syllabus/output/BIOL-8_Spring-2026_Syllabus.mp3) |
| Schedule | [Source](syllabus/Schedule.md) | [PDF](syllabus/output/Schedule.pdf) | [DOCX](syllabus/output/Schedule.docx) | [HTML](syllabus/output/Schedule.html) | [TXT](syllabus/output/Schedule.txt) | [MP3](syllabus/output/Schedule.mp3) |

---

## Resources

- [Concepts of Biology (Textbook PDF)](resources/ConceptsofBiology-WEB.pdf) - OpenStax textbook

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
