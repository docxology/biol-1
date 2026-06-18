# BIOL-1 Technical Documentation

## Course

General Biology — College of the Redwoods, taught at Pelican Bay. **16** content modules covering molecular biology through evolution and ecology.

## Directory layout

```
biol-1/
├── course/
│   ├── module-01-study-of-life/        # 16 modules: each has questions.md +
│   │   …                               #            keys-to-success.md + output/
│   ├── labs/                           # lab-NN_*.md (1–17), with output/ and dashboards/
│   ├── exams/                          # exam-NN.md, exam-NN_key.md, exam-template.md
│   ├── practice_tests/                 # practice-test-NN.md, practice-test-NN_key.md
│   └── quizzes/                        # quiz-template.md
├── syllabus/                           # syllabus + schedule (multi-format)
├── resources/
│   └── slides/                         # module-N-slides-{full,notes}.pdf
├── private/                            # Instructor-only (not published)
│   └── Pelican Bay/                    # Institution-specific PII (PBSP_Memos, …)
├── README.md
└── AGENTS.md
```

## Module structure

Each `course/module-NN-name/` contains:

- `README.md` — student-facing overview.
- `AGENTS.md` — technical doc for tooling.
- `questions.md` — practice questions.
- `keys-to-success.md` — module study guide.
- `resources/` (optional) — module-local images and datasets.
- `output/` — generated artifacts:
  - `output/study-guides/module-NN-name-questions.{md,pdf,docx}` by default
  - `output/study-guides/module-NN-name-keys-to-success.{md,pdf,docx}` by default
  - HTML, TXT, and MP3 are supported opt-in formats
  - `output/website/index.html`

There is **no** `assignments/` subfolder convention in BIOL-1.

## File naming

| Artifact | Source path | Generated naming |
|---|---|---|
| Module questions | `course/module-NN-name/questions.md` | `module-NN-name-questions.{md,pdf,docx,…}` |
| Module study guide | `course/module-NN-name/keys-to-success.md` | `module-NN-name-keys-to-success.{md,pdf,docx,…}` |
| Lab | `course/labs/lab-NN_topic.md` | `lab-NN_topic.{pdf,html}` |
| Lab dashboard | `course/labs/dashboards/lab-NN_topic-dashboard.html` | (already final HTML) |
| Practice test | `course/practice_tests/practice-test-NN.md` | `practice-test-NN.{pdf,docx,…}` |
| Exam | `course/exams/exam-NN.md` (+ `_key`) | `exam-NN.{pdf,docx,…}` |
| Slides | `resources/slides/module-N-slides-{full,notes}.pdf` | (already final PDF) |
| Syllabus | `syllabus/*.md` | `*.{pdf,docx,md}` by default in `syllabus/output/`; HTML, TXT, and MP3 are opt-in |

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
