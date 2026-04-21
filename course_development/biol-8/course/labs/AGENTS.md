# Technical Documentation: Labs

## Technical Specifications

This directory follows the standard `cr-bio` repository structure for `course` items.
No special processing rules apply beyond the standard automated multi-format export pipeline.

## Lab numbering (Spring 2026)

There are **18** Markdown lab sources (`lab-01_*.md` … `lab-18_*.md`). Notable pairings:

| File | Role |
|------|------|
| `lab-16_exam-03-review.md` | Paper review for Exam 03 (Modules 11–15); aligns with `../exams/exam-03.md` |
| `lab-17_ecology.md` | Module 16 ecology — DDT bead model, three trials; **HTML `table.lab-table lab-table-compact`** for summary (T1–T3 + Mean); data cells use `{fill}` (fillable) so PDF columns stay narrow — `{fill:text}` blows out width |
| `lab-18_evolution.md` | Module 17 evolution — point schedule + **HTML `table.lab-table`** for roster; **Table 1** uses **`lab-table-compact`** + `<td>{fill}</td>` for LG/SG/LS/SS grids (three season blocks); Table 2 earnings; static price grid; not `lab:data-table` for labeled rows |

See [README.md](README.md) for the full inventory.
