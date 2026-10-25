# BIOL-1 public course publication

This repository is the generated `PUBLISHED/biol-1` subtree of the private
`cr-bio` authoring repository. Its student-facing guide is [README.md](README.md).

## Source and regeneration

The canonical copies of these two landing documents live in
`course_development/biol-1/resources/publication/` in cr-bio. `publish_course`
copies only `README.md` and `AGENTS.md` from that directory. Edit the canonical
copies and regenerate; direct edits to the public checkout will be replaced.

Module content comes from `module.toml`, and lab/practice-test content from their
course Markdown sources. The configured profile renders PDF and DOCX for 16
modules, 17 labs, four review worksheets and four practice-test sets, plus
syllabus, PDF slides and dashboards. Lecture copying requires an explicit
`include_lectures = true`; it is disabled for this course. `publish.toml` is the authority for enabled formats and stages.

The authoring workflow renders and validates locally before committing. The
`PUBLISHED/biol-1` tree is then split and pushed to this repository. Public pushes
must preserve remote work; a non-fast-forward result requires reconciliation.

## Layout

- `course/`: syllabus and schedule.
- `modules/`: module bundles and generated local visual assets.
- `module-NN-*/`: module quiz outputs.
- `homework/`, `module_keys/`, `labs/`, `slides/`, `practice_tests/`, `dashboards/`:
  category collections.
- `full_flat/`, `ALL_FILES/`: generated bulk collections.

## Validation and privacy

Publishing checks all 16 modules, configured formats and the dashboard/lab
invariant. The shared renderer stages and validates new PDF/DOCX files before
replacement and checks declared source fingerprints. Structural validation does
not replace visual inspection or establish content correctness.

Exams, exam answer keys, accommodations and private institutional files remain
in the private authoring repository. Public practice-test/module keys are
intentional. Before publication, scan the complete generated tree, including flat
mirrors, for excluded files. Archive snapshots are not active publish targets.
