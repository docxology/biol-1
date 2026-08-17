# Syllabus Format

> **Navigation**: [← README](../README.md) | [Module Format](MODULE_FORMAT.md) | [Exam Format](EXAM_FORMAT.md) | [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md)

Authoring guide for syllabus and schedule source files.

---

## Overview

| Property | Value |
|----------|-------|
| **Source directory** | `course_development/biol-1/syllabus/` |
| **Source files** | `BIOL-1_Fall-2026_Syllabus.md`, `Schedule.md` |
| **Output directory** | `syllabus/output/` |
| **Default formats** | PDF, DOCX |
| **Opt-in formats** | HTML, TXT, MP3 |
| **Backing module** | `batch_processing.process_syllabus` |

---

## Source File Structure

### Syllabus (`BIOL-1_Fall-2026_Syllabus.md`)

```markdown
# BIOL-1: General Biology
## College of the Redwoods — Pelican Bay, Fall 2026

**Instructor:** Dr. Daniel Ari Friedman
**Email:** ...
**Office Hours:** ...

## Course Description
...

## Learning Outcomes
...

## Grading
...

## Policies
...
```

### Schedule (`Schedule.md`)

```markdown
# BIOL-1 Fall 2026 Schedule

| Week | Day | Date | Topic | Notes |
|-----|-----|------|-------|-------|
| 1 | Mon | 8/24 | Module 01: Study of Life | |
| 1 | Wed | 8/26 | Lab 01: Measurement Methods | |
| 2 | Mon | 8/31 | Module 02: Basic Chemistry | |
...
```

---

## Generation

```bash
# From repo root
python publish.py --skip-git

# Direct from software/
uv run python scripts/generate_syllabus_renderings.py --course biol-1
```

The syllabus is processed by `batch_processing.process_syllabus()` which:
1. Reads markdown source files (excluding README.md, AGENTS.md)
2. Renders each to all enabled formats (PDF and DOCX by default)
3. Writes outputs to `syllabus/output/`

---

## Output Naming

| Source | Output pattern |
|--------|---------------|
| `BIOL-1_Fall-2026_Syllabus.md` | `BIOL-1_Fall-2026_Syllabus.{pdf,docx}` |
| `Schedule.md` | `Schedule.{pdf,docx}` |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md) | Course directory layout |
| [../pipeline/GENERATION_FLOW.md](../pipeline/GENERATION_FLOW.md) | Generation pipeline |
| [../../AGENTS.md](../../AGENTS.md) | API reference |
