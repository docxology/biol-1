# Changelog

All notable changes to the CR-BIO Course Development System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md for version tracking
- CONTRIBUTING.md with development guidelines
- DOCUMENT_TYPES.md with comprehensive format reference
- BIOL-1 exam directory structure with templates
- BIOL-1 quiz directory structure with templates
- BIOL-1 lab stubs for modules 02-17 (16 new files)

### Improved
- Course parity between BIOL-1 and BIOL-8 lab structures
- Updated BIOL-1 labs README with full inventory

### Identified Gaps (Audit 2026-01-28)
- **Lab Development**: 30 lab stubs need full development (16 BIOL-1, 14 BIOL-8)
- **BIOL-1 Assessments**: Exams and quizzes have templates but no content
- **BIOL-1 Slides**: Modules 9 and 17 missing slide PDFs (30 of 34 present)

## [0.1.0] - 2026-01-28

### Course Content
- **BIOL-8**: 15 modules covering Human Biology (College of the Redwoods)
  - 4 exams with answer keys
  - 15 quizzes with answer keys
  - 1 complete lab (Lab 01: Measurement Methods)
  - 14 lab protocol stubs
- **BIOL-1**: 17 modules covering Introduction to Biology (Pelican Bay Prison)
  - 17 keys-to-success files
  - 17 questions files
  - 1 complete lab (Lab 01: Measurement Methods)
  - 30 slide PDFs (modules 1-8, 10-16; modules 9 and 17 missing)

### Software Infrastructure
- 11 generation modules (markdown_to_pdf, text_to_speech, etc.)
- 6 output formats (PDF, HTML, MP3, DOCX, TXT, Lab Manual)
- 26 test files with 325+ tests
- Orchestration system for batch processing

### Documentation
- ARCHITECTURE.md
- QUICKSTART.md
- ORCHESTRATION.md
- Module-level AGENTS.md files

---

## Version History Notes

| Version | Date | Focus |
|---------|------|-------|
| 0.1.0 | 2026-01-28 | Initial audit and version tracking |

[Unreleased]: https://github.com/cr-bio/course_development/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cr-bio/course_development/releases/tag/v0.1.0
