# Exam Format Guide

> **Navigation**: [← Content Types](../README.md) | [Module Format](MODULE_FORMAT.md) | [Practice Test Format](PRACTICE_TEST_FORMAT.md) | [Syllabus Format](SYLLABUS_FORMAT.md) | [Lab Format](../LAB_FORMAT.md) | [Course Structure](../COURSE_STRUCTURE.md) | [Architecture](../ARCHITECTURE.md)

Complete guide for authoring unit exams and the comprehensive final. Exams are **teacher-only** materials — they are never published to public student-facing repositories.

---

## File Naming & Location

| Convention | Example |
|-----------|---------|
| **Unit exam** | `exam-NN.md` |
| **Unit exam key** | `exam-NN_key.md` |
| **Final exam** | `final-exam.md` |
| **Final exam key** | `final-exam_key.md` |
| **Template scaffold** | `exam-template.md` |
| **Location** | `course_development/biol-1/course/exams/` |
| **Output directory** | `course_development/biol-1/course/exams/output/` |

```
course/exams/
├── exam-01.md
├── exam-01_key.md
├── exam-02.md
├── exam-02_key.md
├── exam-03.md
├── exam-03_key.md
├── final-exam.md
├── final-exam_key.md
├── exam-template.md
└── output/                        # Local renders (PDF, DOCX, etc.)
```

> ⚠️ Exams and answer keys are **never published** to public student-facing repositories. The publish pipeline may render them locally but does not copy them to `PUBLISHED/`.

---

## BIOL-1 Exam Inventory

| Files | Schedule Exam | Module Coverage | Points |
|-------|---------------|-----------------|--------|
| `exam-01.md`, `exam-01_key.md` | Exam 01 | **Modules 01–06** | 50 |
| `exam-02.md`, `exam-02_key.md` | Exam 02 | **Modules 07–11** | 50 |
| `exam-03.md`, `exam-03_key.md` | Exam 03 | **Modules 12–15** | 50 |
| `final-exam.md`, `final-exam_key.md` | Comprehensive Final | **Modules 01–15** | 100 |
| `exam-template.md` | — | Scaffold / alternate 100-pt style | — |

### Practice Test Parity

| Practice Test | Corresponding Exam |
|---------------|-------------------|
| `practice-test-03` | Exam 02 (Modules 7–11) |
| `practice-test-04` | Exam 03 (Modules 12–15) |
| `practice-test-05` | Comprehensive Final (Modules 1–16) |

See [PRACTICE_TEST_FORMAT.md](PRACTICE_TEST_FORMAT.md) for practice test details.

---

## Point Structure

### Unit Exams (50 points)

| Part | Points | Format |
|------|--------|--------|
| **Part A** | 30 | Multiple choice |
| **Part B** | 11 | Fill-in-the-blank (word bank) |
| **Part C** | 9 | Free response (choose **three** of **five** prompts) |
| **Total** | **50** | |

### Final Exam (100 points)

| Part | Points | Format |
|------|--------|--------|
| **Part A** | 45 | Multiple choice (three per module, 15 modules) |
| **Part B** | 15 | Fill-in-the-blank (19-term bank, four distractors) |
| **Part C** | 25 | Free response — choose **any five** of **seven** prompts (5 pts each) |
| **Part D** | 15 | Essay — choose **one** of **three** prompts |
| **Total** | **100** | |

---

## Part A/B/C Layout

### Part A — Multiple Choice

Standard multiple choice with 4 options (A–D). Each question is worth 1 point.

```markdown
### Part A: Multiple Choice (30 points)

**Instructions**: Choose the best answer for each question. Each question is worth 1 point.

1. Which property is shared by all living organisms?
   A. They reproduce sexually.
   B. They are composed of cells.
   C. They move voluntarily.
   D. They photosynthesize.

2. ...
```

### Part B — Fill-in-the-Blank (Word Bank)

Students match terms from a word bank to fill blanks in sentences.

```markdown
### Part B: Fill-in-the-Blank (11 points)

**Instructions**: Use the word bank to fill in the blanks. Each blank is worth 1 point.

**Word Bank**: (1) Homeostasis, (2) Hypothesis, (3) Metabolism, ...

1. The maintenance of stable internal conditions is called __________.
2. A testable explanation for an observed pattern is a __________.
3. ...
```

### Part C — Free Response (Choose N of M)

Students choose a subset of prompts to answer.

```markdown
### Part C: Free Response (9 points)

**Instructions**: Choose **three** of the following **five** prompts. Each is worth 3 points.

1. Explain how the hierarchy of biological organization extends from cells to ecosystems.
2. Describe the difference between a hypothesis and a scientific theory.
3. ...
```

---

## exam-template.md

The `exam-template.md` file is a scaffold for creating new exams. It demonstrates the alternate 100-point style layout and can be adapted for unit exams or supplemental assessments. Use it as a starting point when authoring a new exam.

---

## Exam Shuffling (exam_tools package)

The `exam_tools` package provides utilities for shuffling question and answer option order to create exam variants. This is useful for:

- Creating alternate forms for accommodation or academic integrity
- Generating practice versions from the same question pool
- Randomizing Part A option order while preserving correct answer keys

```python
# Example usage (see software/src/ for actual API)
from src.exam_tools.main import shuffle_questions

# Shuffle question order while tracking answer key mapping
shuffled = shuffle_questions(exam_path="exam-01.md", seed=42)
```

> **Note**: When shuffling, the `_key.md` file must be regenerated to match the shuffled order. Always verify shuffled exams against their keys before distribution.

---

## Generation Commands

```bash
cd software

# Generate all BIOL-1 outputs (includes exams when enabled)
uv run python scripts/generate_all_outputs.py --course biol-1

# The publish pipeline renders exams locally but does NOT push them to public repos
python publish.py --skip-git
```

Exams use the same multi-format rendering path as other markdown content under `course/`. PDF and other formats are generated via `batch_processing` / `generate_all_outputs.py` when exams are included in the run.

> **BIOL-1 note**: `publish.toml` does not set `include_exams` for BIOL-1. Local renders follow whatever the generation script includes. See [../../publish.toml](../../publish.toml) for current configuration.

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [PRACTICE_TEST_FORMAT.md](PRACTICE_TEST_FORMAT.md) | Practice test format and exam parity |
| [README.md](../README.md) | Content types index |
| [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md) | Course directory layout (assessment section) |
| [../../course_development/biol-1/course/exams/AGENTS.md](../../course_development/biol-1/course/exams/AGENTS.md) | Source-level exam documentation |
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Pipeline and generation workflows |
