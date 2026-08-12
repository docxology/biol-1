# Operator task index

`cr-bio` is operated through its canonical course and publishing sources.
Operator uses this file as the root discovery signpost; content tasks remain in
the source trees named below.

## Canonical task surfaces

- `course_development/biol-1/` — canonical BIOL-1 source and schedule work.
- `software/` — pipeline, validation, and test maintenance.
- `publish.toml` and `publish.py` — publication orchestration and release
  checks.
- `TODO.md` files under the relevant source directory — local planning context.

## Operator operations

- Run `python publish.py --dry-run` before a publication change.
- Run the repo contract and software test gates before claiming a repair.
- Edit canonical source files, then regenerate derived `PUBLISHED/` artifacts.
- Keep private course material and generated output within the repository's
  existing confidentiality boundaries.

This is a discovery index, not a replacement for course or software plans.
