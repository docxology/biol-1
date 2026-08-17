# Technical Documentation: BIOL-1 Review Materials

## Purpose

This folder contains non-primary exam-review worksheets that support
BIOL-1 exam preparation. These files are **not** numbered labs — active
numbered labs live only in `../labs/` and map one-to-one with Modules 01–16.

## File Inventory

| File | Scope | Status |
|------|-------|--------|
| `exam-01-review.md` | Modules 01–06 review | Complete |
| `exam-02-review.md` | Modules 07–11 review | Complete |
| `exam-03-review.md` | Modules 12–16 review | Complete |
| `final-exam-review.md` | Comprehensive review (Modules 01–15 plus Module 16 capstone synthesis) | Complete |

## Naming Convention

Files follow the pattern `exam-NN-review.md` for unit exams and
`final-exam-review.md` for the comprehensive final.

## Pipeline Integration

Review worksheets are processed through the `lab_manual` module alongside
numbered labs, generating PDF and HTML outputs. They use the same
`{fill:text}` and `<!-- lab:reflection -->` directive syntax.

**Do not** name files `lab-NN_*.md` here; the 16-module / 16-lab contract
requires that numbered labs live only in `../labs/`.

## Related Documentation

| Document | Description |
|----------|-------------|
| [`README.md`](README.md) | Student-facing overview |
| [`../AGENTS.md`](../AGENTS.md) | Course-level technical documentation |
| [`../labs/AGENTS.md`](../labs/AGENTS.md) | Lab manual technical documentation |
