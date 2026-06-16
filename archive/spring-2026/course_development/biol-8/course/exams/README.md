# BIOL-8 Exams

## Overview

This directory contains exams for BIOL-8: Human Biology (College of the Redwoods, Del Norte Campus).

## Exam Structure

BIOL-8 unit exams (Exam 01–03) use **50 points** total. Coverage:

| Exam | Modules | Topic Coverage |
|------|---------|----------------|
| Exam 01 | 01-06 | Scientific Method through Metabolism (see exam header) |
| Exam 02 | 07-10 | Genetics, Cell Division, Tissues, Inheritance |
| Exam 03 | 11-15 | Skeletal, Muscular, Nervous, Microbiology, Cardiopulmonary |
| Final | 01–17 | Comprehensive (**100 pts** layout in `final-exam.md`; see syllabus) |

## File Naming Convention

- `exam-XX.md` - Exam questions
- `exam-XX_key.md` - Answer key

## Format (final: 100 points)

`final-exam.md` is **comprehensive (modules 01–17)** and uses:

- **Part A:** 51 multiple choice (**three per module**) — **51** pts  
- **Part B:** 15 fill-in blanks with word bank — **15** pts  
- **Part C:** seven integrated short prompts; students answer **any five** — **25** pts (**5 × 5**)  
- **Part D:** essay — **choose one** of three prompts — **9** pts  

See the live markdown files for wording and keys.

---

## Format (unit exams: 50 points)

Exams 01–03 follow this pattern (exact counts may vary slightly by exam):

```markdown
## Part A: Multiple Choice (~30–31 points)
*1 point each*

## Part B: Fill in the Blank (10–11 points)
*Word bank; 1 point each blank*

## Part C: Free Response (9 points)
*Choose THREE of five questions; 3 points each*
```

## Development Status

- [x] exam-01.md + key
- [x] exam-02.md + key
- [x] exam-03.md + key
- [x] final-exam.md + key

## Contents

| File | Description | Status |
|------|-------------|--------|
| exam-01.md | Exam 1: Modules 01-06 | Complete |
| exam-01_key.md | Exam 1 Answer Key | Complete |
| exam-02.md | Exam 2: Modules 07-10 | Complete |
| exam-02_key.md | Exam 2 Answer Key | Complete |
| exam-03.md | Exam 3: Modules 11-15 | Complete |
| exam-03_key.md | Exam 3 Answer Key | Complete |
| final-exam.md | Final Exam: Modules 01–17 (100 pts) | Complete |
| final-exam_key.md | Final Exam Answer Key | Complete |

---

## Output Rendering

Exams are rendered locally to `output/` (PDF + DOCX) by `generate_all_outputs.py`.
Both exam questions and answer keys are rendered for teacher use.

> **Teacher-Only Materials**: Exams are **never published** to public git repositories.
> The `output/` directory is for local instructor use only.

---

*Created: 2026-01-29 · Updated: 2026-05*
