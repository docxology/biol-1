# Contributing to CR-BIO Course Development

Thank you for contributing to the CR-BIO course development system. This guide covers how to add course content, develop lab protocols, and create assessments.

## Table of Contents

- [Quick Start](#quick-start)
- [Lab Protocol Development](#lab-protocol-development)
- [Assessment Development](#assessment-development)
- [Module Content Guidelines](#module-content-guidelines)
- [Testing Your Changes](#testing-your-changes)

---

## Quick Start

1. **Clone the repository**
2. **Install dependencies**: `cd software && uv sync`
3. **Run tests**: `uv run pytest tests/ -v`
4. **Generate outputs**: `uv run python scripts/generate_all_outputs.py --course biol-8 --module 1`

---

## Lab Protocol Development

### Template Reference

Use `course_development/biol-8/course/labs/lab-01_measurement-methods.md` as the reference template. This 390-line lab demonstrates all required components.

### Required Sections

Each lab protocol must include:

```markdown
# Lab Protocol: Module XX - [Topic]

## Learning Objectives
- [7-10 measurable objectives aligned with module content]

## Part 0: Lab Orientation
[Safety, equipment familiarization]

## Part 1-N: Activity Sections
[Structured activities with clear instructions]

## Data Collection
[Tables and recording areas using lab directives]

## Analysis Questions
[Reflection and interpretation prompts]

## Summary
[Skills practiced and module connection]
```

### Interactive Elements

Use these lab markdown directives:

| Directive | Purpose | Example |
|-----------|---------|---------|
| `{fill:text}` | Single-line input | Student name field |
| `{fill:textarea rows=N}` | Multi-line text area | Reflection responses |
| `<!-- lab:reflection -->` | Open-ended text areas | Discussion prompts |
| `<!-- lab:data-table -->` | Fillable data tables | Measurement recording |
| `<!-- lab:object-selection -->` | Object identification | Material selection |

### Quality Checklist

- [ ] 7+ learning objectives
- [ ] Safety considerations documented
- [ ] Materials list with quantities
- [ ] Step-by-step procedures
- [ ] Data collection tables
- [ ] Analysis questions (5+)
- [ ] Interactive elements for student input
- [ ] Module connection statement
- [ ] Estimated duration

---

## Assessment Development

### Exam Format (BIOL-8 Standard)

```markdown
# [Course] Exam [Number]
## Modules XX-YY: [Topic Coverage]

**Date**: [Date]
**Total Points**: 100

## Part A: Multiple Choice (50 points)
*2 points each, 25 questions*

## Part B: Short Answer (30 points)
*5 points each, 6 questions*

## Part C: Essay Questions (20 points)
*Choose ONE, 20 points*
```

### Quiz Format (BIOL-8 Standard)

```markdown
# Module XX Quiz: [Topic]

**Name**: _________________________ **Date**: _____________

## Part A: Multiple Choice (7 points)
*1 point each, 7 questions*

## Part B: Free Response (3 points)
*1 point each, 3 questions*
```

### Assessment Guidelines

1. **Align with module content**: Every question should map to learning objectives
2. **Balance difficulty**: Mix recall, application, and analysis questions
3. **Create answer keys**: Every assessment needs a `*_key.md` file
4. **Use consistent formatting**: Follow the templates exactly

---

## Module Content Guidelines

### Keys to Success Files

Each module needs a `keys-to-success.md` with:
- Learning objectives
- Key concepts
- Study tips
- Common misconceptions

### Questions Files

Each module needs a `questions.md` with:
- 18-20 natural language study questions
- Range from factual to analytical
- Aligned with exam/quiz content

---

## Testing Your Changes

### Validate File Structure

```bash
cd software
uv run python -m src.file_validation.main --course biol-8
```

### Generate Outputs (Dry Run)

```bash
uv run python scripts/generate_all_outputs.py --course biol-8 --module 1 --dry-run
```

### Run Full Test Suite

```bash
uv run pytest tests/ -v
```

### Generate Lab Manual

```bash
uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual(
    '../course_development/biol-8/course/labs/lab-XX_topic.md',
    '../course_development/biol-8/course/labs/output/lab-XX_topic.pdf',
    'pdf',
    course_name='BIOL-8: Human Biology'
)
"
```

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Lab | `lab-XX_topic-name.md` | `lab-01_measurement-methods.md` |
| Exam | `exam-XX.md` | `exam-01.md` |
| Exam Key | `exam-XX_key.md` | `exam-01_key.md` |
| Quiz | `module-XX_quiz.md` | `module-01_quiz.md` |
| Quiz Key | `module-XX_quiz_key.md` | `module-01_quiz_key.md` |
| Keys to Success | `keys-to-success.md` | (within module directory) |
| Questions | `questions.md` | (within module directory) |

---

## Getting Help

- Check existing complete files as references
- Run validation before committing
- Open an issue for questions

---

*Last Updated: 2026-01-28*
