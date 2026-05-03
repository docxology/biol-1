# BIOL-8 Course Materials — Technical Documentation

## Overview

Technical documentation for BIOL-8 course materials organization, processing, and workflow management. This directory contains student-facing course materials organized by module, exams, quizzes, and labs.

## Directory Structure

```
course/
├── README.md                    # Course materials overview (student-facing)
├── AGENTS.md                    # This technical documentation
│
├── exams/                       # Unit exams (as authored)
│   ├── exam-01.md              # Modules 01–06 (50 pts)
│   ├── exam-01_key.md          # Answer key with explanations
│   ├── exam-02.md              # Modules 07–10 (50 pts)
│   ├── exam-02_key.md
│   ├── exam-03.md              # Modules 11–15 (50 pts)
│   ├── exam-03_key.md
│   ├── final-exam.md            # Comprehensive final (modules 01–17, 100 pts)
│   └── final-exam_key.md
│
├── quizzes/                     # 34 files: 17 modules × (quiz + key)
│   ├── module-01_quiz.md       # Student version
│   ├── module-01_quiz_key.md   # Answer key
│   └── … module-17_quiz{,_key}.md
│
├── labs/                        # Lab protocols (Markdown + dashboards/)
│   ├── lab-01_measurement-methods.md
│   └── ... (see labs/README.md; e.g. lab-13_nervous-system.md, lab-14_microbiology.md, lab-14_microbiology-followup.md)
│
└── module-XX-topic-name/        # 17 module directories (optional assignments/, resources/)
    ├── keys-to-success.md      # Learning objectives
    ├── questions.md            # Study questions
    └── resources/              # Optional supplementary assets (several early modules)
```

## Module Naming Convention

Modules follow the pattern: `module-XX-topic-name/`

| Number | Directory Name |
|--------|---------------|
| 01 | `module-01-exploring-life-science` |
| 02 | `module-02-chemistry-of-life` |
| 03 | `module-03-biomolecules` |
| 04 | `module-04-cellular-function` |
| 05 | `module-05-membranes` |
| 06 | `module-06-metabolism` |
| 07 | `module-07-genetics` |
| 08 | `module-08-cell-division` |
| 09 | `module-09-tissues` |
| 10 | `module-10-inheritance` |
| 11 | `module-11-skeletal-system` |
| 12 | `module-12-muscular-system` |
| 13 | `module-13-nervous-system` |
| 14 | `module-14-microbiology` |
| 15 | `module-15-cardiopulmonary-system` |
| 16 | `module-16-ecology` |
| 17 | `module-17-evolution` |

## Content Specifications

### Module Content Files

Each module contains:

1. **`keys-to-success.md`**
   - 5-6 key learning objectives
   - Organized by numbered topic areas
   - Includes study tips section

2. **`questions.md`**
   - 18-20 natural language study questions
   - Continuous numbering (1 through 18-20)
   - Covers all learning objectives

3. **`resources/`** (optional)
   - Used when the module ships figures or datasets alongside markdown (several modules **01–12** include this folder).
   - Modules **13–17** currently omit `resources/` when there are no extra assets.

### Quiz Format

Each quiz follows consistent structure:

```markdown
# Module XX Quiz: Topic

**Name**: _________________________ **Date**: _____________

## Part A: Multiple Choice (7 points)
- 7 questions, 1 point each
- 4 answer choices (A-D)

## Part B: Free Response (3 points)
- 3 questions, 1 point each
- Answer lines provided
```

Answer keys include:

- Multiple choice answer table with explanations
- Rubric or key points for free response

### Exam Format

Unit exams (Exam 01–03) use **50 points** total. Typical layout:

| Section | Points | Format |
|---------|--------|--------|
| Part A: Multiple Choice | ~30–31 pts | 1 pt each |
| Part B: Fill in the Blank | 10–11 pts | Word bank; 1 pt per blank |
| Part C: Free Response | 9 pts | Choose **3 of 5** short responses; 3 pts each |
| **Total** | **50 pts** | |

**Comprehensive final** (`final-exam.md` + `final-exam_key.md`): **100** points cumulative — Part A **51** multiple choice (**3 × 17** modules); Part B **15** blanks (word bank); Part C **five** prompts × **5** points; Part D **choose one** of **three** essay prompts (**9** points).
### Lab Protocol Format

Lab stubs include sections for:

- Learning objectives (pre-filled)
- Estimated duration
- Materials needed (stub)
- Safety considerations (stub)
- Procedure (stub)
- Data collection (stub)
- Analysis questions (stub)

## Alignment with Schedule

| Unit | Modules | Exam |
|------|---------|------|
| Unit 1 | 01-06 | Exam 01 (Week 5) |
| Unit 2 | 07-10 | Exam 02 (Week 8) |
| Unit 3 | 11-15 | Exam 03 (Week 13) |
| Unit 4 | 16-17 | Final Exam (Finals Week) |
| All | 01-17 | Final Exam (Finals Week) |

## File Processing Workflow

### Current State

Module content files (`keys-to-success.md`, `questions.md`) are source markdown ready for:

- Direct Canvas upload
- Processing to PDF, DOCX, HTML via batch processing utilities
- TTS conversion for accessibility

### Future Processing

The `software/` directory contains batch processing utilities for:

- PDF generation via `markdown_to_pdf` module
- Audio generation via `text_to_speech` module  
- Format conversion via `format_conversion` module
- Website generation via `html_website` module

## Validation Checklist

### Completeness

- [x] 17 module directories created (`module-01-…` through `module-17-…`)
- [x] Each module has `keys-to-success.md` and `questions.md`; `resources/` present where assets exist (optional otherwise)
- [x] 3 unit exams + comprehensive final (`exam-01`–`exam-03` + keys, **plus** `final-exam*` = **10** markdown files total)
- [x] 17 quizzes with answer keys (34 files in `quizzes/`)
- [x] 18 lab protocols in `labs/` (`lab-01_measurement-methods.md` … `lab-18_evolution.md`)

### Coherence

- [x] Module numbering matches syllabus
- [x] Exam coverage matches schedule
- [x] Quiz content aligns with keys-to-success
- [x] Consistent formatting across all files

### Pedagogical Quality

- [x] Learning objectives use action verbs
- [x] Questions progress from recall to application
- [x] Multiple choice options are plausible
- [x] Free response allows demonstration of understanding

## Related Documentation

- **[../syllabus/](../syllabus/)**: Syllabus and schedule
- **[../../software/](../../software/)**: Processing utilities
- **[../../private/](../../private/)**: Non-student materials

