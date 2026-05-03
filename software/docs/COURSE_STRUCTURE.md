# Course Structure Reference

> **Navigation**: [← README](README.md) | [Lab Format](LAB_FORMAT.md) | [Dashboard Format](DASHBOARD_FORMAT.md) | [Architecture](ARCHITECTURE.md)

Complete reference for the cr-bio course content directory layout, file organization, and the development-to-publication pipeline.

---

## Two-Tier Architecture

```mermaid
flowchart LR
    subgraph PRIVATE[Development]
        CD[course_development/]
    end
    
    subgraph PIPELINE[Pipeline]
        PUB[publish.py]
    end
    
    subgraph PUBLIC[Published]
        B1[biol-1_repo]
        B8[biol-8_repo]
    end
    
    CD --> PUB
    PUB --> B1
    PUB --> B8
```

| Tier | Repository | Visibility | Contents |
|------|-----------|-----------|----------|
| **Development** | `cr-bio` (this repo) | Private | Source Markdown, software, exams, answer keys |
| **Published** | `biol-1`, `biol-8` | Public | Generated PDFs, DOCX, HTML, TXT, MD, MP3, websites |

The pipeline transforms source content into multiple output formats and pushes to the public repositories. Teacher-only materials (exams, answer keys) are **never published**.

---

## Repository Root Structure

```
cr-bio/
├── course_development/            # All course content
│   ├── biol-1/                    # General Biology (Pelican Bay)
│   └── biol-8/                    # Human Biology (College of the Redwoods)
│
├── software/                      # Processing pipeline
│   ├── src/                       # 16 Python packages
│   ├── tests/                     # Pytest suite (run --collect-only for current count)
│   ├── scripts/                   # CLI orchestrators
│   └── docs/                      # Documentation (YOU ARE HERE)
│
├── PUBLISHED/                     # Generated output (gitignored)
│   ├── biol-1/                    # Published BIOL-1 content
│   └── biol-8/                    # Published BIOL-8 content
│
├── publish.py                     # Top-level publish script
├── publish.toml                   # Pipeline configuration
└── .cursorrules                   # Real Methods Policy
```

---

## Course Directory Anatomy

Each course follows an identical structure:

```
course_development/biol-X/
├── course/                        # Core course content
│   ├── module-01-topic-name/      # Module directories (15-17)
│   ├── labs/                      # Lab protocols & dashboards
│   ├── exams/                     # Teacher-only assessments
│   └── quizzes/                   # Per-module quizzes
│
├── syllabus/                      # Syllabus & schedule
├── resources/                     # Supplementary materials
└── private/                       # Facility-specific content
```

---

## Module Structure

### Naming Convention

```
module-XX-topic-name/
```

Zero-padded two-digit number + kebab-case topic slug.

### Contents

```
module-01-exploring-life-science/
├── keys-to-success.md             # Study guide
├── questions.md                   # Review questions
├── resources/                     # Module-specific resources
│   └── *.pdf                      # Lecture slides, readings
└── output/                        # Generated outputs
    ├── study-guides/              # PDF, DOCX, HTML, TXT, MD, MP3 (per publish.toml)
    └── website/                   # index.html (interactive)
```

| File | Purpose | Output Formats |
|------|---------|----------------|
| `keys-to-success.md` | Student study guide | PDF, DOCX, HTML, TXT, MD, MP3 |
| `questions.md` | Review questions | PDF, DOCX, HTML, TXT, MD, MP3 |

---

## Lab Structure

Paths below are relative to `course_development/biol-{1,8}/`. The long example lists **BIOL-8** labs through **18** plus a supplemental follow-up page; **BIOL-1** stops at **17** numbered protocols but uses the same folder layout (`course/labs/`, `course/labs/dashboards/`, `course/labs/output/`).

### Source Files

```
course/labs/
├── lab-01_measurement-methods.md
├── lab-02_probability-statistics.md
├── lab-03_microscopy.md
├── lab-04_diffusion-membranes.md
├── lab-05_ph-solutions.md
├── lab-06_central-dogma.md
├── lab-07_cell-division.md
├── lab-08_inheritance.md
├── lab-09_enzymes.md
├── lab-10_tissues.md
├── lab-11_skeletal-system.md
├── lab-12_muscular-system.md
├── lab-13_nervous-system.md
├── lab-14_microbiology.md
├── lab-14_microbiology-followup.md
├── lab-15_cardiopulmonary-system.md
├── lab-16_exam-03-review.md
├── lab-17_ecology.md
├── lab-18_evolution.md
├── dashboards/                    # Interactive HTML dashboards
│   ├── lab-01_measurement-methods-dashboard.html
│   ├── ...
│   └── lab-18_evolution-dashboard.html
└── output/                        # Generated PDFs and HTML
```

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| **Lab protocol** | `lab-XX_topic-name.md` | `lab-07_cell-division.md` |
| **Dashboard** | `lab-XX_topic-dashboard.html` | `lab-07_cell-division-dashboard.html` |

See [LAB_FORMAT.md](LAB_FORMAT.md) and [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md) for authoring guides.

---

## Assessment Structure

### Exams (Teacher-Only)

Common on-disk layout under `course_development/biol-X/course/exams/`:

```
course/exams/
├── exam-NN.md
├── exam-NN_key.md
└── output/                        # Local renders (PDF, DOCX, etc.); never published publicly
```

**BIOL-1 (verify on disk):** **Two** exams with keys are common (e.g. `exam-01`, `exam-03`). **`exam-03` is the second-unit exam spanning modules 07–11**, not necessarily “modules 12–15” — course numbering is not interchangeable with BIOL-8 or generic templates.

**BIOL-8:** **Three** unit exams with keys (`exam-01` … `exam-03`); scopes are modules **01–06**, **07–10**, and **11–15** (typically **50 points** each — see headers in each file). Comprehensive final per syllabus; **`final-exam.md`** may appear only when authored.

> ⚠️ Exams and answer keys are **never published** to public student-facing repositories.

### Quiz point layouts

Per-quiz totals **vary by file** — when present, BIOL-8 module quizzes sometimes follow layouts such as ~7 pts multiple choice + ~3 pts free response; always read the live markdown.

### Quizzes (Teacher-Only)

**BIOL-8** — full per-module quiz set:

```
course/quizzes/
├── module-01_quiz.md
├── module-01_quiz_key.md
├── ...
└── (17 modules × 2 files)
```

**BIOL-1** — `course/quizzes/` is **template-only** (e.g. `quiz-template.md`). Routine practice sits in each module **`questions.md`**, not in parallel `module-NN_quiz` files per module.

---

## Syllabus Structure

```
syllabus/
├── BIOL-X_Spring-2026_Syllabus.md   # Course syllabus
├── Schedule.md                       # Week-by-week schedule
└── output/                           # Flat output (no subdirs)
    ├── BIOL-X_Spring-2026_Syllabus.pdf
    ├── BIOL-X_Spring-2026_Syllabus.docx
    ├── BIOL-X_Spring-2026_Syllabus.html
    ├── Schedule.pdf
    ├── Schedule.docx
    └── Schedule.html
```

> **Note**: Syllabus outputs use a **flat** structure (files directly in `output/`, no subdirectories).

---

## Published Directory Structure

After the publish pipeline runs, the `PUBLISHED/` directory contains:

```
PUBLISHED/
├── biol-1/
│   ├── modules/                   # Study guides and questions
│   │   ├── module-01/
│   │   │   ├── keys-to-success.pdf
│   │   │   ├── keys-to-success.docx
│   │   │   ├── questions.pdf
│   │   │   └── questions.docx
│   │   └── ...
│   ├── labs/                      # Lab protocols
│   ├── syllabus/                  # Syllabus and schedule
│   ├── slides/                    # Lecture slides
│   └── websites/                  # Interactive websites
│
└── biol-8/
    ├── modules/
    ├── labs/
    ├── syllabus/
    ├── slides/
    └── websites/
```

The `flatten` pipeline stage reorganizes outputs into these categories.

---

## BIOL-1 vs BIOL-8 Differences

| Feature | BIOL-1 | BIOL-8 |
|---------|--------|--------|
| **Setting** | Pelican Bay Prison | CR Del Norte Campus |
| **Content modules (`module-*`)** | 15 | 17 |
| **Slides** | 30 PDFs in course `resources/slides/` (module **9** may lack full + notes pair) | 15 PDFs in course `resources/slides/` |
| **Labs (+ dashboards)** | 17 protocols + dashboards | 18 protocols + dashboards |
| **Exams (on disk)** | 2 + keys (`course/exams/`) | 3 + keys (unit exams **01–03**) |
| **Quizzes (`course/quizzes/`)** | Template(s) only | 17 × 2 (student + key) |
| **Practice tests** | 3 + keys | 12 + keys (verify on disk) |
| **Private directory** | Includes facility-specific material | Standard private layout |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [LAB_FORMAT.md](LAB_FORMAT.md) | Lab protocol authoring guide |
| [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md) | Dashboard format guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Software architecture |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Pipeline workflows |
| [QUICKSTART.md](QUICKSTART.md) | Setup and quick commands |
