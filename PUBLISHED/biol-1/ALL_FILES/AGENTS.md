# Technical documentation: BIOL-1 `practice_tests/`

## Role

Optional practice tests and keys for exam preparation. The pipeline globs `*.md` (excluding `README` / `AGENTS` prefixes) and writes PDFs under `output/` via `process_course_practice_tests` in `software/src/batch_processing/main.py`.

## Files

| File | Module coverage / exam prep |
|------|----------------------------|
| `practice-test-01.md` + `_key.md` | Modules 1–4 |
| `practice-test-02.md` + `_key.md` | Modules 5–6 |
| `practice-test-03.md` + `_key.md` | Modules 7–11 (Exam 02 prep) |
| `practice-test-04.md` + `_key.md` | Modules 12–15 (Exam 03 prep) |

## Conventions

- Student version: `practice-test-NN.md`
- Key: `practice-test-NN_key.md` (same stem + `_key`)

## Processing

- From repo: `cd software && uv run python scripts/generate_all_outputs.py --course biol-1` (with practice tests enabled in [publish.toml](../../../../publish.toml)).
- Publish step copies `practice_tests/` (and `output/`) into `PUBLISHED/biol-1/practice_tests/`.

## Related

- [../exams/AGENTS.md](../exams/AGENTS.md) — formal exams
- [../AGENTS.md](../AGENTS.md) — full course tree
