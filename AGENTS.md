# `PUBLISHED/biol-1/` — generated BIOL-1 course subtree (technical doc)

**Status: generated.** This entire directory is rebuilt on every publish run.
It is the exact content that gets `git subtree split --prefix=PUBLISHED/biol-1`
force-pushed to `github.com/docxology/biol-1` (`main`). The human-facing
landing page is [README.md](README.md).

## Generated layout

| Path | Produced by |
|---|---|
| `course/` | `publish_course.py` (syllabus + schedule renders) |
| `module-NN-*/`, `modules/`, `module_keys/` | `publish_course.py` + `copy_module_bundles` |
| `homework/`, `labs/`, `slides/`, `practice_tests/`, `dashboards/` | `copy_extras.py` (`copy_labs_and_dashboards`, `copy_slides`, `copy_practice_tests`) |
| `lectures/` | `copy_lectures` (per-module `captions.srt`; combined mp4+srt when present) |
| `full_flat/`, `ALL_FILES/` | `copy_full_flat` / root `publish.py::flatten_all_files` |

Exams are **never** published (teacher-only; rendered locally into
`course_development/biol-1/course/exams/output/`).

## Invariants

- Only `README.md` and `AGENTS.md` at this level survive
  `clean_published` (`src/publish/flatten.py`); every other file is regenerated
  each run — do not hand-edit, do not add files.
- Validation gate: `scripts/validate_outputs.py --course biol-1` must pass
  (16/16 modules, dashboard invariant, lecture captions present).
- Config source: `publish.toml` (`max_module = 16`, `max_lab = 19`,
  `all_files = true`, per-course `include_*` toggles wired to `--skip-*` flags).

## Regenerate

```bash
python publish.py --skip-git        # regenerate + validate locally
python publish.py                   # regenerate + commit + subtree push
```
