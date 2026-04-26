# Course development

Authoritative markdown and assets for CR-BIO live under this directory. The publish pipeline reads `publish.toml` at the repo root and writes generated artifacts to `PUBLISHED/` (git-ignored from this monorepo; pushed to per-course public repos when configured).

## Courses

| Course | Label | Student overview | Technical docs |
|--------|-------|------------------|----------------|
| [biol-1](biol-1/README.md) | General Biology (Pelican Bay) | [README](biol-1/README.md) | [AGENTS](biol-1/AGENTS.md) |
| [biol-8](biol-8/README.md) | Human Biology (Del Norte) | [README](biol-8/README.md) | [AGENTS](biol-8/AGENTS.md) |

## What each course folder contains

- **`course/`** — `module-NN-…` directories, labs, exams, practice tests, and (BIOL-8) module quizzes
- **`syllabus/`** — syllabus and schedule sources; **outputs** are written only under `syllabus/output/`
- **`resources/`** — in practice, **lecture slide PDFs** under `resources/slides/` (see each course’s resources README)
- **`private/`** — not published; not for student copies

## Generation (short)

```bash
cd software
uv run python scripts/generate_all_outputs.py --course biol-1   # or biol-8
```

Full end-to-end: `python publish.py` from the repository root. See [software/docs/QUICKSTART.md](../software/docs/QUICKSTART.md).

## Documentation

- [AGENTS.md](AGENTS.md) — tooling and layout for *this* directory
- [../AGENTS.md](../AGENTS.md) — top-level technical reference for the whole repo
