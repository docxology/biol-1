# Course development — technical documentation

## Purpose

`course_development/` is the **authoring tree** for CR-BIO courses. Humans edit markdown and assets here; `python publish.py` (from the repo root) generates `PUBLISHED/<course>/` and can push per-course public subtrees.

## Layout

| Path | Role |
|------|------|
| [`biol-1/`](biol-1/AGENTS.md) | General Biology (Pelican Bay): **15** content modules, labs 01–17, exams, practice tests, syllabus. |
| [`biol-8/`](biol-8/AGENTS.md) | Human Biology (Del Norte): **17** modules, labs 01–18, unit exams, quizzes, syllabus. |

Each course has:

- `course/` — modules (`module-NN-…/`), `labs/`, `exams/`, `practice_tests/`, `quizzes/` (as applicable)
- `syllabus/` — markdown sources; outputs go to `syllabus/output/` (not second sources for batch discovery)
- `resources/` — course-level resources (in practice, **`resources/slides/`** PDFs for both courses; see per-course `resources/README.md`)
- `private/` — instructor-only; excluded from `PUBLISHED/`
- `README.md` / `AGENTS.md` — student vs tooling docs

## Processing

- **modules**: `software` batch processing → `output/study-guides/`, TTS, optional `output/website/`
- **labs**: `lab_manual` + dashboards HTML
- **syllabus**: `batch_processing.process_syllabus` / `generate_syllabus_renderings.py`
- **config**: [publish.toml](../../publish.toml) per-course `max_module`, `max_lab`, formats

## Conventions

- **BIOL-1** module folders: `module-01-…` through `module-15-…` (no `module-16` in the current tree).
- **Per-module** `AGENTS.md` and `module-*/resources/AGENTS.md` may stay short for the default pipeline; each file’s **Related documentation** section points to the authoritative `course/AGENTS.md` and `biol-*/AGENTS.md` for layout and publish commands.

## Privacy

- Do not copy `private/` or Pelican Bay PII into student-facing or `course/` trees.

## Related

| Document | Use |
|----------|-----|
| [README.md](README.md) | Short index of the two courses |
| [../software/docs/ORCHESTRATION.md](../software/docs/ORCHESTRATION.md) | Pipeline stages |
| [../AGENTS.md](../AGENTS.md) | Repository-wide course + publish overview |
