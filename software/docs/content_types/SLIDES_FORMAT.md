# Slides Format

> **Navigation**: [← README](../README.md) | [Module Format](MODULE_FORMAT.md) | [Syllabus Format](SYLLABUS_FORMAT.md) | [../output/PDF.md](../output/PDF.md)

Authoring and generation guide for BIOL-1 slide decks.

---

## Overview

| Property | Value |
|----------|-------|
| **Source** | `module.toml` (via `module_content`) |
| **Generator** | `slide_deck` package |
| **Output directory** | `course_development/biol-1/resources/slides/` |
| **HTML sources** | `resources/slides/generated/` |
| **Variants** | Full (student-facing), Notes (instructor) |
| **Format** | PDF (via WeasyPrint) + HTML source |

---

## Slide Deck Structure

Each module generates an 11-slide deck:

| Slide # | Title | Role | Visual |
|---------|-------|------|--------|
| 1 | Module map | title-map | module-map |
| 2 | Learning objectives | objectives | objective-ladder |
| 3 | Topic sequence | topics | topic-sequence |
| 4 | Concept map | concept-map | embedded-svg |
| 5 | Process model | process-model | embedded-svg |
| 6 | Retrieval card | retrieval-card | embedded-svg |
| 7 | Key terms | terms | term-grid |
| 8 | Practice quiz | quiz | quiz-panel |
| 9 | Lab connection | lab | lab-bridge |
| 10 | Summary | summary | summary-recap |
| 11 | Next module | next | transition-card |

---

## Output Naming

| Variant | Filename pattern |
|---------|-----------------|
| Full (student) | `module-N-slides-full.pdf` |
| Notes (instructor) | `module-N-slides-notes.pdf` |
| HTML source | `generated/module-N-slides-{full,notes}.html` |

---

## Generation

```bash
# Generate slide decks for all BIOL-1 modules
cd software && uv run python scripts/generate_slide_decks.py --course biol-1

# Single module
cd software && uv run python scripts/generate_slide_decks.py --course biol-1 --module 1

# Dry run
cd software && uv run python scripts/generate_slide_decks.py --course biol-1 --dry-run
```

The `slide_deck` package:
1. Loads `module.toml` via `module_content.load_module_content()`
2. Builds a `SlideDeck` with 11 `Slide` objects
3. Renders each variant (full + notes) as HTML
4. Converts HTML to PDF via WeasyPrint

---

## Notes Variant

The notes variant includes instructor guidance for each slide:
- Suggested talking points
- Transition cues
- Student engagement prompts

Notes slides are **never** pushed to the public student repository.

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [MODULE_FORMAT.md](MODULE_FORMAT.md) | Module manifest format |
| [../output/PDF.md](../output/PDF.md) | PDF output format |
| [../../src/slide_deck/AGENTS.md](../../src/slide_deck/AGENTS.md) | Slide deck package docs |
