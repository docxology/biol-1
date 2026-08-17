# BIOL-1 Technical Documentation

## Course

General Biology — College of the Redwoods, taught at Pelican Bay. **16** content modules covering molecular biology through evolution and ecology.

## Directory layout

```
biol-1/
├── course/
│   ├── course_by_date/                 # generated dated teaching handoffs
│   ├── module-01-study-of-life/        # 16 modules: each has questions.md +
│   │   …                               #            key-points.md + output/
│   ├── labs/                           # lab-NN_*.md (1–20), with output/ and dashboards/
│   ├── exams/                          # exam-NN.md, exam-NN_key.md, exam-template.md
│   ├── practice_tests/                 # practice-test-NN.md, practice-test-NN_key.md
│   └── quizzes/                        # quiz-template.md
├── syllabus/                           # syllabus + schedule (multi-format)
├── resources/
│   └── slides/                         # generated module-N-slides-{full,notes}.pdf + generated HTML sources
├── private/                            # Instructor-only (not published)
│   └── Pelican Bay/                    # Institution-specific PII (PBSP_Memos, …)
├── README.md
└── AGENTS.md
```

## Course-by-date projection

`course_calendar.toml` is the canonical Fall 2026 mapping from each scheduled
meeting date to planned and currently used modules, labs, practice tests,
reviews, exams, and assigned textbook chapters. The generated
`course/course_by_date/YYYY-MM-DD/` folders contain a
single flat `materials/` directory of copied learner-facing rendered
deliverables (no Markdown or JSON) plus `meeting.json` provenance metadata; do
not edit them by hand.

```bash
cd software
uv run python scripts/generate_course_by_date.py
uv run python scripts/generate_course_by_date.py --validate-only
```

LectureCreate date folders contain the playable MP4 and module YAML.
Captions, JSON manifests, frames, WAV files, hashes, and render intermediates
remain in the canonical `output/lectures/` tree.

## Module structure

Each `course/module-NN-name/` contains:

- `README.md` — student-facing overview.
- `AGENTS.md` — technical doc for tooling.
- `module.toml` — **canonical typed source** (module number, slug, title, linked lab, topics, learning objectives/questions, practice-quiz items, module-local assets). Edit this, not the generated files below.
- `questions.md` — practice questions, **generated from `module.toml`**.
- `key-points.md` — module study guide, **generated from `module.toml`**.
- `practice-quiz.md` — practice quiz items, **generated from `module.toml`**.
- `resources/` (optional) — module-local images and datasets.
- `output/` — generated artifacts:
  - `output/study-guides/module-NN-name-questions.{pdf,docx}` by default
  - `output/study-guides/module-NN-name-key-points.{pdf,docx}` by default
  - HTML, TXT, and MP3 are supported opt-in formats
  - `output/website/index.html`

There is **no** `assignments/` subfolder convention in BIOL-1.

Regenerate the generated Markdown after editing `module.toml`:

```bash
cd software && uv run python scripts/generate_module_materials.py --course biol-1 --module NN
```

## File naming

| Artifact | Source path | Generated naming |
|---|---|---|
| Module source | `course/module-NN-name/module.toml` | (canonical; not itself a generated-naming target) |
| Module questions | `course/module-NN-name/questions.md` (generated from `module.toml`) | `module-NN-name-questions.{md,pdf,docx,…}` |
| Module study guide | `course/module-NN-name/key-points.md` (generated from `module.toml`) | `module-NN-name-key-points.{md,pdf,docx,…}` |
| Module practice quiz | `course/module-NN-name/practice-quiz.md` (generated from `module.toml`) | `module-NN-name-practice-quiz.{md,pdf,docx,…}` |
| Lab | `course/labs/lab-NN_topic.md` | `lab-NN_topic.pdf` |
| Lab dashboard | `course/labs/dashboards/lab-NN_topic-dashboard.html` | (already final HTML) |
| Practice test | `course/practice_tests/practice-test-NN.md` | `practice-test-NN.{pdf,docx,…}` |
| Exam | `course/exams/exam-NN.md` (+ `_key`) | `exam-NN.{pdf,docx,…}` |
| Slides | `resources/slides/module-N-slides-{full,notes}.pdf` | generated from module.toml via `generate_slide_decks.py` |
| Syllabus | `syllabus/*.md` | `*.{pdf,docx}` by default in `syllabus/output/`; Markdown source is retained; HTML, TXT, and MP3 are opt-in |

## Pipeline integration

```bash
# Generate all BIOL-1 outputs
cd software && uv run python scripts/generate_all_outputs.py --course biol-1

# Generate a single module
cd software && uv run python scripts/generate_module_renderings.py --course biol-1 --module 12

# Render syllabus
cd software && uv run python scripts/generate_syllabus_renderings.py --course biol-1

# Publish into PUBLISHED/biol-1/
cd software && uv run python scripts/publish_course.py --course biol-1
```

The top-level `python publish.py` runs all of the above end-to-end and pushes `PUBLISHED/biol-1/` to its public subtree (`github.com/docxology/biol-1`).

## Privacy

- `private/` is excluded from `PUBLISHED/`. Never link or copy material from `private/` into `course/`.
- `private/Pelican Bay/` contains institution-specific PII (memos, accommodation forms). Treat as confidential.

## Generated slide decks

Generated slide decks are active Fall 2026 outputs. Edit `course/module-*/module.toml`, then run `cd software && uv run python scripts/generate_slide_decks.py --course biol-1` or the full publish pipeline. Legacy imported decks live under `archive/fall-2026-legacy-slides/`.
