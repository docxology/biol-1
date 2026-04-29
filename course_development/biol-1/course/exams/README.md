# BIOL-1 Exams

## Overview

This directory contains exams for BIOL-1: Introduction to Biology (Pelican Bay State Prison).

## Exam Structure

BIOL-1 has **15** content modules (`module-01` … `module-15`). The schedule maps unit exams to module ranges as follows (see `syllabus/Schedule.md`):

| Exam | Modules | Topic coverage |
| --- | --- | --- |
| Exam 01 | 01–06 | Scientific method, chemistry, cells, membranes, metabolism |
| Exam 02 | 07–11 | Molecular genetics, cellular genetics, inheritance, epigenetics, genomics & biotechnology |
| Exam 03 | 12–15 | Darwin & evolution, populations evolve, macroevolution, population & systems ecology |
| Final (Exam 04) | Comprehensive | Broad final (syllabus) |

**Note on filenames:** On disk, `exam-03.md` / `exam-03_key.md` are the **second** unit exam in the schedule (Exam **02**, modules **07–11**). The body and “Modules 07–11” coverage are correct for that exam. If the title line still reads “Exam 03”, treat that as a filename quirk: either rename the pair to `exam-02` / `exam-02_key` for clarity or retitle the H1 to match the schedule—do **not** retarget this file to modules **12–15**. For the **third** unit (12–15), author **new** files (for example `exam-04.md` + `exam-04_key.md`, after any rename of the current pair) and use [practice-test-04](../practice_tests/) for review until those exist.

## Files on disk

- `exam-01.md` + `exam-01_key.md`
- `exam-03.md` + `exam-03_key.md`
- `exam-template.md` — alternate full-exam scaffold (100-point style)

## File naming convention

- `exam-XX.md` — exam questions
- `exam-XX_key.md` — answer key

## Format

**`exam-01.md`** (Exam 01) and **`exam-03.md`** (schedule Exam 02; modules 07–11) both use a **50-point** layout (30 multiple choice, 11 fill-in-the-blank with word bank, 9 points free response — choose three of five). See those files for the live pattern.

The `exam-template.md` file describes an alternate **100-point** layout (25 MC at 2 points each, short answer, essay) for courses that adopt it.

## Development status

- [x] exam-01.md + exam-01_key.md
- [x] exam-03.md + exam-03_key.md (second unit exam on schedule; same as Exam 02 — reconcile **filename / H1** with schedule if desired, not module range)
- [ ] exam-02.md + key (optional duplicate if you rename the current `exam-03` pair to `exam-02`)
- [ ] final-exam.md + key (comprehensive)

## Template

See `exam-template.md` for an alternate full-exam scaffold.
