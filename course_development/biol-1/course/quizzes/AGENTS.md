# Technical documentation: BIOL-1 `quizzes/`

## Role

Holds a **quiz template** (`quiz-template.md`); this course does **not** use one quiz file per module the way BIOL-8 does. Authors may duplicate the template to create new quizzes under this folder; naming should stay consistent if multiple quizzes are added (for example `module-NN_quiz.md` + `_key`).

## Processing

If markdown quizzes are added here, include them in whatever generation step you use (Pandoc/docx, or ad hoc PDF) — the main repo pipeline is centered on `questions.md` in each `module-NN-…/` folder, not on this directory, unless you wire a script to process these files.

## Related

- [../AGENTS.md](../AGENTS.md) — where primary assessment-style questions are authored (per-module `questions.md`)
