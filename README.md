# BIOL-1 — General Biology

Course materials for **BIOL-1, General Biology** at College of the Redwoods (Fall 2026). Sixteen modules run from the study of life through a capstone systems synthesis, and every module ships with slides, a lab, homework, a practice quiz, an answer key, and an interactive review dashboard.

Most artifacts exist in more than one format — a rendered PDF for handing out, and a DOCX you can edit — so the materials can be used as-is, adapted, or rebuilt.

## Modules

| # | Module |
|---|---|
| 01 | Study of Life |
| 02 | Basic Chemistry |
| 03 | Organic Molecules |
| 04 | Cells |
| 05 | Membranes |
| 06 | Metabolism |
| 07 | Molecular Genetics |
| 08 | Cellular Genetics |
| 09 | Inheritance Genetics |
| 10 | Epigenetics |
| 11 | Genomics and Biotechnology |
| 12 | Darwin and Evolution |
| 13 | How Populations Evolve |
| 14 | Macroevolution |
| 15 | Population and Systems Ecology |
| 16 | Capstone: Systems Synthesis |

## Repository layout

| Path | Contents |
|---|---|
| `course/` | Syllabus and schedule (DOCX + PDF) |
| `modules/` | Per-module bundles: study guides, quizzes, slides, visual assets |
| `module-NN-*/` | That module's practice quiz (DOCX + PDF) |
| `module_keys/` | Answer keys |
| `slides/` | Lecture decks (full + notes PDFs per module) |
| `labs/` | Lab handouts (16 protocols + 3 TBD sessions) |
| `homework/` | Homework sets |
| `practice_tests/` | Practice tests 01–04 + keys (PT04 = comprehensive final review) |
| `dashboards/` | Interactive HTML review dashboards (per lab + exam reviews) |
| `lectures/` | Per-module lecture captions (`.srt`); videos regenerate locally |
| `full_flat/` | Every export file flattened one level, for bulk download |
| `ALL_FILES/` | Flat mirror of every file (collision-prefixed duplicates) |

686 files (298 PDF, 144 SVG, 132 DOCX, 60 HTML, 32 caption files, 20 Markdown), plus the `ALL_FILES/` mirror of the same 686.

## Using this repository

**Students** — start with `course/` for the syllabus and schedule, then work module by module. The `dashboards/` folder holds self-check review pages for each lab and exam; open the `.html` files directly in a browser.

**Instructors** — `full_flat/` gives you every artifact in one directory if you want to bulk-import into an LMS. The per-module folders keep quizzes next to their keys. Markdown sources are included wherever they exist, so you can edit and re-render rather than starting from the PDF.

## Reuse

No license file is present in this repository. Please contact the author before redistributing or adapting these materials for another course.

## Related

- [`biol-8`](https://github.com/docxology/biol-8) — Human Anatomy and Physiology, same structure
- [`biology_textbook`](https://github.com/docxology/biology_textbook) — an open, generatively-built introductory biology textbook (CC BY 4.0)

---

> **Agents, note:** This tree is GENERATED. Do not hand-edit files here; edit
> source in `course_development/biol-1/` (module content lives in each module's
> `module.toml`) and regenerate with `python publish.py --skip-git` from the repo
> root. This README survives `clean_published`; wrong-path edits elsewhere in
> this tree are silently overwritten by the next publish run.
