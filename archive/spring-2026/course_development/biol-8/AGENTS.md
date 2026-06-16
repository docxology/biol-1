# BIOL-8 Technical Documentation

## Course

Human Anatomy & Physiology — College of the Redwoods, Del Norte campus. 17 modules covering cell biology, body systems, microbiology, ecology, and evolution.

## Directory layout

```
biol-8/
├── course/
│   ├── module-01-exploring-life-science/   # 17 modules: each has questions.md +
│   │   …                                   #            keys-to-success.md + output/
│   ├── module-17-evolution/                #            (some include assignments/)
│   ├── labs/                               # lab-NN_*.md (1–18), with output/ and dashboards/
│   ├── exams/                              # exam-NN.md / exam-NN_key.md
│   ├── practice_tests/                     # practice-test-NN.md / _key.md
│   └── quizzes/                            # quiz-template.md
├── syllabus/                               # syllabus + schedule (multi-format)
├── resources/
│   └── slides/                             # module-N-slides-{full,notes}.pdf
├── private/                                # Instructor-only (not published)
├── README.md
└── AGENTS.md
```

## Module structure

Each `course/module-NN-name/` contains:

- `README.md` — student-facing overview.
- `AGENTS.md` — technical doc for tooling.
- `questions.md` — practice questions.
- `keys-to-success.md` — module study guide.
- `resources/` (most modules) — module-local images and datasets.
- `assignments/` (some modules, e.g. module-15) — homework / quizzes specific to the module.
- `output/` — generated artifacts:
  - `output/study-guides/module-NN-name-questions.{md,pdf,docx,html,txt,mp3}`
  - `output/study-guides/module-NN-name-keys-to-success.{md,pdf,docx,html,txt,mp3}`
  - `output/website/index.html`

## File naming

| Artifact | Source path | Generated naming |
|---|---|---|
| Module questions | `course/module-NN-name/questions.md` | `module-NN-name-questions.{md,pdf,docx,…}` |
| Module study guide | `course/module-NN-name/keys-to-success.md` | `module-NN-name-keys-to-success.{md,pdf,docx,…}` |
| Lab | `course/labs/lab-NN_topic.md` | `lab-NN_topic.{pdf,html}` |
| Lab dashboard | `course/labs/dashboards/lab-NN_topic-dashboard.html` | Final HTML; Lab 15 uses two files (`*_cardiovascular-*`, `*_respiratory-*`) for one lab markdown |
| Practice test | `course/practice_tests/practice-test-NN.md` | `practice-test-NN.{pdf,docx,…}` |
| Exam | `course/exams/exam-NN.md` (+ `_key`) | `exam-NN.{pdf,docx,…}` |
| Slides | `resources/slides/module-N-slides-{full,notes}.pdf` | (already final PDF) |
| Syllabus | `syllabus/*.md` | `*.{pdf,docx,html,txt,mp3}` in `syllabus/output/` |

## Pipeline integration

```bash
# Generate all BIOL-8 outputs
cd software && uv run python scripts/generate_all_outputs.py --course biol-8

# Generate a single module
cd software && uv run python scripts/generate_module_renderings.py --course biol-8 --module 13

# Render syllabus
cd software && uv run python scripts/generate_syllabus_renderings.py --course biol-8

# Publish into PUBLISHED/biol-8/
cd software && uv run python scripts/publish_course.py --course biol-8
```

The top-level `python publish.py` runs all of the above end-to-end and pushes `PUBLISHED/biol-8/` to its public subtree (`github.com/docxology/biol-8`).

## Privacy

- `private/` is excluded from `PUBLISHED/`. Never link or copy material from `private/` into `course/`.
