# Generated Slides

## Overview

Active BIOL-1 Fall 2026 slide decks are generated from structured module manifests, not hand-edited PDFs. The generator reads each `course/module-*/module.toml`, embeds that module's deterministic SVG visuals as the three-slide visual spine, and writes full-page plus speaker-notes PDFs.

## Active outputs

- `module-N-slides-full.pdf` — classroom/student full-page deck.
- `module-N-slides-notes.pdf` — instructor notes deck with teaching prompts.
- `generated/module-N-slides-full.html` — canonical HTML source for the full deck.
- `generated/module-N-slides-notes.html` — canonical HTML source for the notes deck.

There must be exactly one full PDF and one notes PDF for every active module 1-16.

Each deck has 11 slides. Exactly three slides embed generated SVGs: concept map, process model, and retrieval card. The remaining slides use deterministic CSS visual surfaces that support the same module/lab/question/quiz structure.

## Source of truth

The slide content comes from the same structured fields used by keys, questions, practice quizzes, labs, and generated visuals: topics, contents, learning objectives, terms, learning questions, practice quiz items, lab link, and generated SVG specs in `module.toml`.

## Legacy slides

Imported pre-generation slide PDFs were moved to `archive/fall-2026-legacy-slides/`. They are retained for historical reference only and are not active publish inputs.
