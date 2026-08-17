# `course_by_date` package

This package is the typed implementation of the BIOL-1 date-map projection.
Keep the layer boundaries intact:

- `calendar.py` parses/validates TOML and resolves source artifacts.
- `generator.py` copies existing outputs and writes provenance metadata.
- `validation.py` verifies folder completeness, source existence, checksums,
  and exclusion of rebuildable LectureCreate intermediates.

Do not add authored course content here. Edit
`course_development/biol-1/course_calendar.toml` for scheduling decisions.
