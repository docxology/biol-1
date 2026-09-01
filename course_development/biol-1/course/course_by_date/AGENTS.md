# AGENTS.md — `course_by_date/`

Generated per-class-meeting folders for BIOL-1 Fall 2026, one `YYYY-MM-DD/`
per scheduled class date (created from `course_calendar.toml` at the
`biol-1/` level). Each date folder is **generated**: a `README.md` (meeting
metadata + provenance of each copied file), `meeting.json` (typed meeting
record), and `materials/` with copies of that day's rendered artifacts
(study-guides, slides, lecture mp4) pulled from module `output/` and
`resources/slides/` locations listed in the README.

Gotchas:
- Regenerate from the calendar tooling; do not hand-edit date folders or
  `materials/` — the READMEs record exact source paths.
- Future dates (e.g. September–December) may exist as skeletons with empty
  or partial `materials/` until that class's content is generated.
- Course dates with no meeting (holidays) have no folder here.
