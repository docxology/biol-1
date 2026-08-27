# Project State Report - 2026-08-26 (cr-bio)

## Scope

Two-part mission in `projects/ongoing/DAF/cr-bio` (its own git checkout,
private sidecar repo at `/Users/4d/Documents/GitHub/projects/ongoing/DAF/cr-bio`):

1. Verify all rendering types work end to end.
2. Update `course_development/biol-1/syllabus/Schedule.md`: cancel the 8/25
   meeting, renumber all sessions starting 8/27 keeping the same order, remove
   Lab 20, keep 11/24 + 11/26 as no-class days.

## Rendering verification and defect fix

Ran the canonical pipeline (`publish.py --dry-run`, then full
`publish_all.py` with PDF+DOCX, 16 modules, 20 labs). First runs crashed
intermittently with SIGSEGV (exit 139, ~1-in-3 runs, varying documents).

macOS crash reports (`.ips`) pinned a consistent signature: GC finalization
destroys a WeasyPrint-per-render `PangoFcFontMap`'s HarfBuzz faces while a
later teardown pass still walks them (`hb_face_destroy` -> SIGSEGV inside
`hb_ot_face_t::fini`). Observed on the Homebrew pango 1.58 / harfbuzz 14.3.1
stack (macOS arm64, cpython 3.11 venv).

**Fix**: one process-wide `FontConfiguration` owned by
`software/src/shared/pdf_font_config.py`; every `write_pdf` call site across
all four renderer modules (`markdown_to_pdf`, `lab_manual`, `slide_deck`,
`format_conversion`) passes it as `font_config`. The first commit covered only
`markdown_to_pdf`; the follow-up caught the remaining three sites because the
full test suite passed 765/765 yet still exited 139 during
`Py_FinalizeEx` - tests green was NOT enough, shutdown had to be verified too.

### Verification evidence

- Stress loop that previously failed ~2-in-3: 6/6 clean (720+ renders)
- Full publish pipeline: 3/3 clean consecutive runs ("Pipeline complete",
  all validations passed)
- Software test suite: **765 passed, EXIT=0** (clean interpreter shutdown;
  an earlier identical run with the partial fix gave 765 passed + exit 139)
- Real post-fix render paths exercised: slide decks (16 decks / 64 files),
  module materials (176 files), lab manual PDF render
- `FakeHTML` test double updated for the new kwarg; its suite passes

## Schedule.md changes

Per instruction plus stated defaults:

- Header and Important Dates note the August 25 cancellation; first class
  meeting is now Thursday, August 27.
- All sessions renumbered 1-32 on the actual Tue/Thu calendar (dates checked
  programmatically against every real meeting day 8/27-12/15); content order
  unchanged, Module 1 + Lab 1 open on 8/27.
- Lab 20 row removed; Labs 17-19 (TBD) fill 11/12-11/19.
- 11/24 and 11/26 remain No Class / fall break; final exam stays 12/10;
  feedback 12/15.
- To absorb the one freed meeting after dropping Lab 20 while preserving the
  same order, the redundant duplicate final-prep row on 12/3 was merged into
  12/1's prep session wording (12/3 kept as review + make-up work). No module
  or lab content was invented or dropped.
- Exam Schedule section synced: Exam 01 -> 9/22, Exam 02 -> 10/15,
  Exam 03 -> 11/10.

Rendered artifacts regenerated into `PUBLISHED/biol-1/`
(`Schedule.pdf` spot-checked via text extraction: contains 8/27, Module 1,
Labs 17-19; "Lab 20" absent).

## Commit delivery to origin/main

The three mission commits below were delivered explicitly and path-scoped
per owner authorization:

1. `fd908d1b` docs(syllabus): cancel 8/25 meeting, renumber sessions from
   8/27, drop Lab 20
2. `d4b10499` fix(render): share one FontConfiguration per process to stop
   pango teardown segfault (+ regenerated PUBLISHED/biol-1)
3. `959fea86` fix(render): route all four WeasyPrint call sites through the
   shared FONT_CONFIG

## Left untouched

- `course_development/biol-1/private/Pelican Bay/Fall_2026/` (pre-existing
  untracked directory) - not staged, not committed, not modified.

## What remains

- Root cause upstream: consider reporting the pango/harfbuzz teardown issue
  to WeasyPrint; the repo-side mitigation is complete.
- The mitigation depends on Homebrew library versions; revisit if
  harfbuzz/pango are upgraded.
