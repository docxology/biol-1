# Glossary

> **Navigation**: [← README](README.md) | [CLI Reference](CLI_REFERENCE.md) | [Config Reference](CONFIG_REFERENCE.md) | [Troubleshooting](TROUBLESHOOTING.md)

Terms and concepts used throughout the cr-bio codebase.

---

## Course Terms

| Term | Definition |
|------|-----------|
| **BIOL-1** | General Biology course at College of the Redwoods, Pelican Bay, Fall 2026. 16 content modules. |
| **BIOL-8** | Archived Spring 2026 biology course. Not an active publish target. |
| **Pelican Bay** | Teaching location (Pelican Bay State Prison). PII-sensitive. |
| **College of the Redwoods** | Institution where courses are taught. |
| **module.toml** | Typed manifest file — the canonical source of truth for each BIOL-1 module. Defines number, title, topics, objectives, terms, quiz, and SVG specs. |
| **keys-to-success.md** | Generated module study guide. First section must be `## Learning Objectives`. |
| **questions.md** | Generated practice questions for a module. Continuously numbered. |
| **practice-quiz.md** | Generated multiple-choice quiz from `module.toml`. |
| **module-NN-name/** | Module directory naming convention (zero-padded number, lowercase, hyphenated). |

---

## Pipeline Terms

| Term | Definition |
|------|-----------|
| **publish pipeline** | The 9-stage process: clean -> generate -> publish -> copy_extras -> flatten -> validate -> all_files -> git_commit -> git_push. |
| **publish.py** | Top-level entry point that reads `publish.toml` and runs the full pipeline. |
| **publish.toml** | Configuration file controlling formats, courses, pipeline stages, and git remotes. |
| **PUBLISHED/** | Generated, tracked directory for subtree publishing. Never edit by hand. |
| **subtree push** | Git technique that splits a subdirectory into its own commit and pushes to a separate remote. Used to publish `PUBLISHED/biol-1/` to `github.com/docxology/biol-1`. |
| **ALL_FILES/** | Flattened copy of every file in `PUBLISHED/<course>/` for direct browsing. |
| **course_development/** | The "back office" — private source materials. The only place humans edit content. |
| **output/** | Generated artifacts within a module or syllabus directory. Created by the pipeline, not hand-edited. |

---

## Content Types

| Term | Definition |
|------|-----------|
| **study guide** | Module learning materials: `keys-to-success.md` and `questions.md`. |
| **lab manual** | Fillable lab worksheet with `{fill:text}` directives, rendered to PDF via `lab_manual` package. |
| **lab dashboard** | Standalone interactive HTML file per lab with evidence capture, checkpoints, and key terms. |
| **SVG concept card** | Deterministic generated visual asset: concept-map, process-model, or retrieval-card. |
| **slide deck** | 11-slide presentation generated from `module.toml` via the `slide_deck` package. Full (student) and notes (instructor) variants. |
| **exam** | Teacher-only assessment material. Never pushed to public repos. Rendered locally to PDF/DOCX. |
| **practice test** | Student-facing test preparation material. Published to public repos. |

---

## Technical Terms

| Term | Definition |
|------|-----------|
| **Layer 0-4** | Dependency hierarchy. Layer 0 (independent) through Layer 4 (external integration). |
| **thin orchestrator** | Script pattern: CLI parsing + module calls + logging only. No business logic in scripts. |
| **Real Methods Policy** | Production code uses real implementations — no mocks, stubs, or fakes. Test doubles only at external-service boundaries. |
| **py.typed** | PEP 561 marker file signaling that the package provides type information. |
| **fillable directive** | Lab manual syntax: `<!-- lab:data-table -->`, `<!-- lab:reflection -->`, `{fill:text}`, `{fill:textarea}`. |
| **transmedia** | Multi-format publishing: same source content rendered to PDF, DOCX, MD, HTML, TXT, MP3, plus interactive websites and dashboards. |
| **repo_contracts** | Repository-level invariant checks: doc coverage, link integrity, course counts, git tracking, production code purity. |

---

## Format Terms

| Format | Extension | Generator | Default |
|--------|-----------|-----------|---------|
| PDF | `.pdf` | WeasyPrint (`markdown_to_pdf`) | Active |
| DOCX | `.docx` | python-docx (`format_conversion`) | Active |
| MD | `.md` | Copy + rename (`format_conversion`) | Active |
| HTML | `.html` | markdown2 (`format_conversion`) | Opt-in |
| TXT | `.txt` | Markdown strip (`format_conversion`) | Opt-in |
| MP3 | `.mp3` | macOS `say` + ffmpeg (`text_to_speech`) | Opt-in |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [CLI_REFERENCE.md](CLI_REFERENCE.md) | All script CLI arguments |
| [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) | All configuration settings |
| [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md) | Course directory layout |
