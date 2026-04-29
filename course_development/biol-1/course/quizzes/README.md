# BIOL-1 Quizzes

## Overview

This folder holds a **quiz template** for ad hoc or instructor-built quizzes. Unlike BIOL-8, BIOL-1 does **not** ship a full set of per-module quiz markdown files here.

Student-facing practice items for each module are authored in that module’s **`questions.md`** (and study narrative in **`keys-to-success.md**`). See [course README](../README.md) and [course AGENTS.md](../AGENTS.md) for layout and publishing.

## On disk

- **`quiz-template.md`** — copy this when adding a new quiz in this directory.

If you add more files, keep naming consistent (for example `module-NN_quiz.md` and `module-NN_quiz_key.md`) and document them in [AGENTS.md](AGENTS.md).

## Pipeline

The main publish pipeline renders per-module `questions.md` / `keys-to-success.md`, not this folder, unless you add a dedicated generation step for new quiz markdown here.

## Related

- [AGENTS.md](AGENTS.md) — technical notes for authors and tooling
- [../AGENTS.md](../AGENTS.md) — full course tree and file naming
