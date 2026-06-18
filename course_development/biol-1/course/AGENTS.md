# BIOL-1 Course Materials — Technical Documentation

Technical reference for the source materials under `course_development/biol-1/course/`.

## Layout

```
course/
├── README.md
├── AGENTS.md                                # This file
├── module-01-study-of-life/  …  module-16-capstone-systems-synthesis/
│   ├── README.md
│   ├── AGENTS.md
│   ├── module.toml                            # Canonical typed source
│   ├── questions.md                          # Generated learning questions
│   ├── keys-to-success.md                    # Generated module study guide
│   ├── practice-quiz.md                      # Generated practice quiz
│   ├── resources/                            # (optional) module-local assets
│   └── output/                               # Generated; do not edit by hand
│       ├── study-guides/
│       │   ├── module-NN-name-questions.{md,pdf,docx}
│       │   └── module-NN-name-keys-to-success.{md,pdf,docx}
│       └── website/index.html
├── labs/                                    # lab-NN_topic.md (1-16), with output/ + dashboards/
├── exams/                                   # exam-NN.md, exam-NN_key.md, final-exam.md, exam-template.md
├── review_materials/                        # non-primary exam review worksheets
├── practice_tests/                          # practice-test-NN.md, practice-test-NN_key.md
└── quizzes/                                 # quiz-template.md
```

## Module directories (16)

| # | Directory |
|---|---|
| 01 | `module-01-study-of-life` |
| 02 | `module-02-basic-chemistry` |
| 03 | `module-03-organic-molecules` |
| 04 | `module-04-cells` |
| 05 | `module-05-membranes` |
| 06 | `module-06-metabolism` |
| 07 | `module-07-molecular-genetics` |
| 08 | `module-08-cellular-genetics` |
| 09 | `module-09-inheritance-genetics` |
| 10 | `module-10-epigenetics` |
| 11 | `module-11-genomics-biotechnology` |
| 12 | `module-12-darwin-evolution` |
| 13 | `module-13-how-populations-evolve` |
| 14 | `module-14-macroevolution` |
| 15 | `module-15-population-systems-ecology` |
| 16 | `module-16-capstone-systems-synthesis` |

## File naming

- Module folders: `module-NN-topic-words/` (zero-padded `NN`, lowercase, hyphenated).
- Source of truth at module root: `module.toml`. Generated files: `questions.md`, `keys-to-success.md`, and `practice-quiz.md`.
- `keys-to-success.md` must put `## Learning Objectives` as the first level-2 section after the title.
- Generated outputs in `output/study-guides/` are prefixed with the full module slug:
  - `module-NN-topic-words-questions.{md,pdf,docx}`
  - `module-NN-topic-words-keys-to-success.{md,pdf,docx}`
  - `module-NN-topic-words-practice-quiz.{md,pdf,docx}` when quiz publishing is enabled later

HTML, TXT, and MP3 study-guide outputs are supported opt-in formats, not part
of the default local publish profile.

There is **no** `assignments/`, `for_upload/`, or per-module `slides/` subfolder in BIOL-1. Exam review worksheets live in `review_materials/`, not numbered labs. Slide PDFs live centrally under `../resources/slides/`.

## Generation

```bash
cd software

# Generate all BIOL-1 outputs
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate a specific module's outputs
uv run python scripts/generate_module_renderings.py --course biol-1 --module 12

# Build the per-module HTML site
uv run python scripts/generate_module_website.py \
    --course biol-1 --module 12
```

The end-to-end pipeline (`python publish.py`) at the repo root runs these steps for every module and pushes the results to `PUBLISHED/biol-1/` and the public subtree.

## Software dependencies

- `batch_processing` — drives per-module multi-format generation.
- `html_website` — builds `output/website/index.html`.
- `format_conversion` — md→pdf, md→docx, etc. (see `software/src/format_conversion/AGENTS.md`).
- `text_to_speech` — generates opt-in `*.mp3` audio narration.

## Related docs

| Document | Description |
|---|---|
| [`../README.md`](../README.md) | Course overview (student-facing) |
| [`../AGENTS.md`](../AGENTS.md) | Course-level technical docs |
| [`../../../software/AGENTS.md`](../../../software/AGENTS.md) | Software documentation |
