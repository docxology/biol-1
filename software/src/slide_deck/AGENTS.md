# Technical Documentation: slide_deck

## Contract

`slide_deck` creates active BIOL-1 Fall 2026 slide decks from `module.toml` through `module_content`.

## Public functions

- `build_slide_deck(module_dir)` returns an in-memory 10-12 slide deck.
- `validate_slide_deck(deck)` returns structural issues without writing files.
- `render_module_slide_deck(module_dir, slides_root, dry_run=False)` writes full and notes HTML plus PDF outputs.
- `render_course_slide_decks(course_root, module_filter=None, dry_run=False)` renders every active module deck.
- `describe_course_slide_decks(course_root, module_filter=None)` returns a dry-run summary.

## Output contract

Active slide PDFs live in `course_development/biol-1/resources/slides/` as `module-N-slides-full.pdf` and `module-N-slides-notes.pdf`. HTML sources live under `resources/slides/generated/`. Legacy imported PDFs are archive-only.
