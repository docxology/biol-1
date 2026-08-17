# Technical documentation: BIOL-1 `exams/`

## Role

Source markdown for unit exams and answer keys. The batch pipeline renders these to `output/` (when the course exam step is run) and publish copies them into `PUBLISHED/biol-1/`.

## Artifacts (on disk)

| Files | Schedule exam | Module coverage |
|-------|----------------|-----------------|
| `exam-01.md`, `exam-01_key.md` | Exam 01 | **01–06** |
| `exam-02.md`, `exam-02_key.md` | Exam 02 | **07–11** |
| `exam-03.md`, `exam-03_key.md` | Exam 03 | **12–15 plus Module 16 capstone synthesis** |
| `final-exam.md`, `final-exam_key.md` | Comprehensive final | **01–15 plus Module 16 capstone synthesis** |
| `exam-template.md` | — | Scaffold / alternate 100-pt style |

Unit exams use a **50-point** layout: Part A **30** MC, Part B **11** fill-in (word bank), Part C **9** points free response (choose **three** of **six**). Exam 03's sixth prompt is the Module 16 capstone synthesis. The **final** uses **100** points: Part A **45** MC, Part B **15** fill-in, Part C **seven** prompts—students **choose any five** (**25** pts; **5** each), and Part D **one** essay (**15** pts) chosen from four prompts.

## Processing

- PDF (and other formats) via `batch_processing` / `generate_all_outputs.py` when exams are included in the run; same multi-format path as other markdown under `course/`.
- See [../../../../software/src/batch_processing/AGENTS.md](../../../../software/src/batch_processing/AGENTS.md) for the orchestration entry points.

## Related

- [../AGENTS.md](../AGENTS.md) — course materials layout
- [README.md](README.md) — exam inventory and schedule alignment
- [`../practice_tests/AGENTS.md`](../practice_tests/AGENTS.md) — practice-test parity (`practice-test-03` ↔ Exam 02; `practice-test-04` ↔ Exam 03)
## Duplex tear-off layout

Every BIOL-1 student practice test and unit/comprehensive exam source carries the `assessment-layout: tearoff-duplex` marker. The renderer produces a duplex packet: page 1 is a compact tear-off answer sheet with one response line per multiple-choice and fill-in item; the reverse side begins the free-response section; subsequent pages contain the question booklet. Answer keys remain conventional and are not transformed.
