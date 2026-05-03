# Technical documentation: BIOL-1 `exams/`

## Role

Source markdown for unit exams and answer keys. The batch pipeline renders these to `output/` (when the course exam step is run) and publish copies them into `PUBLISHED/biol-1/`.

## Artifacts (on disk)

| Files | Schedule exam | Module coverage |
|-------|----------------|-----------------|
| `exam-01.md`, `exam-01_key.md` | Exam 01 | **01–06** |
| `exam-02.md`, `exam-02_key.md` | Exam 02 | **07–11** |
| `exam-03.md`, `exam-03_key.md` | Exam 03 | **12–15** |
| `final-exam.md`, `final-exam_key.md` | Comprehensive final | **01–15** |
| `exam-template.md` | — | Scaffold / alternate 100-pt style |

Unit exams use a **50-point** layout: Part A **30** MC, Part B **11** fill-in (word bank), Part C **9** points free response (choose **three** of **five**). The **final** uses **100** points: Part A **45** MC (three per module), Part B **15** fill-in (19-term bank, four distractors), Part C **seven** short-answer prompts (**25** pts—**five**- or **seven**-question administration per instructor), Part D **one** essay (**15** pts) chosen from three prompts.

## Processing

- PDF (and other formats) via `batch_processing` / `generate_all_outputs.py` when exams are included in the run; same multi-format path as other markdown under `course/`.
- See [../../../../software/src/batch_processing/AGENTS.md](../../../../software/src/batch_processing/AGENTS.md) for the orchestration entry points.

## Related

- [../AGENTS.md](../AGENTS.md) — course materials layout
- [README.md](README.md) — exam inventory and schedule alignment
- [`../practice_tests/AGENTS.md`](../practice_tests/AGENTS.md) — practice-test parity (`practice-test-03` ↔ Exam 02; `practice-test-04` ↔ Exam 03)
