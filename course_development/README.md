# Course development

Authoritative markdown and assets for the active CR-BIO course live under this directory. The publish pipeline reads `publish.toml` at the repo root and writes generated artifacts to tracked `PUBLISHED/` subtrees.

## Courses

| Course | Label | Student overview | Technical docs |
|--------|-------|------------------|----------------|
| [biol-1](biol-1/README.md) | General Biology (Pelican Bay, Fall 2026) | [README](biol-1/README.md) | [AGENTS](biol-1/AGENTS.md) |
| [Spring 2026 archive](../archive/spring-2026/README.md) | Historical BIOL-1 and BIOL-8 | [README](../archive/spring-2026/README.md) | [AGENTS](../archive/spring-2026/AGENTS.md) |

## What each course folder contains

- **`course/`** — `module-NN-…` directories, labs, exams, practice tests, and quizzes/templates
- **`syllabus/`** — syllabus and schedule sources; **outputs** are written only under `syllabus/output/`
- **`resources/`** — in practice, **lecture slide PDFs** under `resources/slides/`
- **`private/`** — not published; not for student copies

## Generation (short)

```bash
cd software
uv run python scripts/generate_all_outputs.py --course biol-1
```

Full end-to-end: `python publish.py` from the repository root. See [software/docs/QUICKSTART.md](../software/docs/QUICKSTART.md).

## Documentation

- [AGENTS.md](AGENTS.md) — tooling and layout for *this* directory
- [../AGENTS.md](../AGENTS.md) — top-level technical reference for the whole repo
