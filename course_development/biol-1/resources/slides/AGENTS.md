# Technical Documentation: Generated Slides

## Contract

Active BIOL-1 Fall 2026 slides are deterministic generated artifacts. Do not hand-edit active slide PDFs or HTML sources. Edit the module manifest and rerun `software/scripts/generate_slide_decks.py` or the full publish pipeline.

## File layout

- Active PDFs: `module-N-slides-full.pdf` and `module-N-slides-notes.pdf` for modules 1-16.
- HTML sources: `generated/module-N-slides-full.html` and `generated/module-N-slides-notes.html`.
- Legacy imported PDFs: `archive/fall-2026-legacy-slides/biol-1/resources/slides/`.

## Generation rules

Each deck has 11 slides. Every slide must include a visual surface: embedded generated SVG, CSS diagram, topic ladder, term grid, lab flow, quiz bridge, or exit-ticket panel. The canonical spine is exactly three dedicated generated-SVG slides: concept map, process model, and retrieval card. Those three slides must use the visual title from `module.toml`, include concise teaching points, and explicitly name the module title and same-numbered lab. The deck must also include learning objectives, module topics, terms/evidence, lab connection, contrast check, quiz bridge, synthesis/exit ticket, and speaker notes in the notes variant.

## Commands

- Dry run: `cd software && uv run python scripts/generate_slide_decks.py --course biol-1 --dry-run`
- Generate: `cd software && uv run python scripts/generate_slide_decks.py --course biol-1`
- Full publish: `python publish.py --skip-git`
