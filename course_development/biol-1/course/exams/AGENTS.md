# Technical documentation: BIOL-1 `exams/`

## Role

Source markdown for unit exams and answer keys. The batch pipeline renders these to `output/` (when the course exam step is run) and publish copies them into `PUBLISHED/biol-1/`.

## Artifacts (on disk)

| Files | Intent (per Spring 2026 schedule) | Notes |
|-------|-----------------------------------|--------|
| `exam-01.md`, `exam-01_key.md` | Exam 01 — modules **01–06** | — |
| `exam-03.md`, `exam-03_key.md` | **Filename** `exam-03` is the **second** unit exam in this folder (schedule: **Exam 02**, modules **07–11**) | The markdown header in `exam-03.md` may still read “Modules 07–11”; align file body with the syllabus when editing. |
| `exam-template.md` | Scaffolding / alternate 100-pt style | — |

**Exam 03** in the **syllabus** (third unit) covers modules **12–15**; there is not necessarily a same-named `exam-0X` file for that range yet. See [README.md](README.md) and [`../practice_tests/AGENTS.md`](../practice_tests/AGENTS.md) for review materials (`practice-test-04`).

## Processing

- PDF (and other formats) via `batch_processing` / `generate_all_outputs.py` when exams are included in the run; same multi-format path as other markdown under `course/`.
- See [../../software/src/batch_processing/AGENTS.md](../../software/src/batch_processing/AGENTS.md) for the orchestration entry points.

## Related

- [../AGENTS.md](../AGENTS.md) — course materials layout
- [README.md](README.md) — exam file inventory and exam vs schedule note
