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
| Final | Comprehensive | Broad final (syllabus) |

**Comprehensive final:** `final-exam.md` + `final-exam_key.md` — **100 points** (45 MC, 15 fill-in with word bank, Part C **choose five of seven** short answers with lined space, one essay chosen from three prompts). Longer and broader than the **50-point** unit exams.

**Filenames match the schedule:** `exam-02.md` / `exam-02_key.md` cover modules **07–11**; `exam-03.md` / `exam-03_key.md` cover modules **12–15**.

## Files on disk

- `exam-01.md` + `exam-01_key.md`
- `exam-02.md` + `exam-02_key.md`
- `exam-03.md` + `exam-03_key.md`
- `final-exam.md` + `final-exam_key.md` — cumulative final (**100** pts)
- `exam-template.md` — alternate full-exam scaffold (100-point style)

## File naming convention

- `exam-XX.md` — unit exam questions  
- `exam-XX_key.md` — unit exam answer key  
- `final-exam.md` / `final-exam_key.md` — cumulative final + key

## Format

**`exam-01.md`**, **`exam-02.md`**, and **`exam-03.md`** use a **50-point** layout (30 multiple choice, 11 fill-in-the-blank with word bank, 9 points free response — choose three of five). Exam **02** uses **six** MC items per module (**07–11**). Exam **03** uses **eight** MC items for modules **12** and **13**, and **seven** each for modules **14** and **15**, for **30** total MC items across four modules.

**`final-exam.md`** uses **100 points:** Part A **45** MC (three per module, modules **01–15**), Part B **15** fill-in terms drawn from a **19-word** bank (**four** decoys), Part C **seven** prompts—students **choose any five** (**25** points; **5** points each), Part D **one** essay (**15** points) from three options.

**Part A shuffle:** Multiple-choice answer letters are **not** kept in a fixed cycle. They are laid out with `software/scripts/shuffle_final_exam_mc.py` using **`FINAL_MC_SEED = 20260203`**. The keyed multiset is **12×A, 11×B, 11×C, 11×D**; distractors within each stem use `Random(FINAL_MC_SEED + question_number)`. Re-run that script after editing Part A option text so `final-exam_key.md` stays aligned. Use **`--spacing-only`** on that script to insert blank lines after stems and between options **without** reshuffling.

The `exam-template.md` file describes another **100-point** scaffold (25 MC at 2 points each, short answer, essay) for courses that adopt it.

## Development status

- [x] exam-01.md + exam-01_key.md
- [x] exam-02.md + exam-02_key.md (modules 07–11)
- [x] exam-03.md + exam-03_key.md (modules 12–15)
- [x] final-exam.md + final-exam_key.md (comprehensive, 100 pts)

## Template

See `exam-template.md` for an alternate full-exam scaffold.
