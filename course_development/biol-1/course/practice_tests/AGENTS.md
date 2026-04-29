# Technical documentation: BIOL-1 `practice_tests/`

## Role

Optional practice tests and keys for exam preparation. The pipeline globs `*.md` (excluding `README` / `AGENTS` prefixes) and writes PDFs under `output/` via `process_course_practice_tests` in `software/src/batch_processing/main.py`.

## Files

| File | Module coverage / exam prep |
|------|----------------------------|
| `practice-test-01.md` + `_key.md` | Modules 1–4 |
| `practice-test-02.md` + `_key.md` | Modules 5–6 |
| `practice-test-03.md` + `_key.md` | Modules 7–11 (Exam 02 prep) |
| `practice-test-04.md` + `_key.md` | Modules 12–15 (Exam 03 prep) |
| `practice-test-05.md` + `_key.md` | Modules 1–15 (comprehensive final prep) |

### Practice Test 05 — layout

135 numbered items total; cohort framing appears in the student markdown header.

| Part | Item numbers | Per-module pattern |
|------|----------------|-------------------|
| A — Multiple choice | **1–75** | Module **N** (1–15): **(N−1)×5 + 1** through **N×5** |
| B — Fill in the blank | **76–105** | Module **N**: **76 + 2(N−1)** and **77 + 2(N−1)** |
| C — Free response | **106–135** | Module **N**: **106 + 2(N−1)** and **107 + 2(N−1)** |

Section headings in Part A match module titles (`module-01-study-of-life` … `module-15-population-systems-ecology`) via [`course/AGENTS.md`](../AGENTS.md).

### Traceability crosswalk (`practice-test-05` ↔ modules)

**Method.** Each module’s PT05 block was matched to that folder’s `keys-to-success.md` learning objectives and key terms (spot-checked Modules **01**, **05**, **12**, **15**) and title alignment across **02–04**, **06–11**, **13–14** via topic headings versus MC stems.

**Spot-check.**

| Module | PT05 samples | Alignment notes |
|--------|----------------|-----------------|
| 01 | MC **1–5**, FR **106–107** | Matches Study of Life LOs (cells, scientific method, homeostasis, hierarchy). |
| 05 | MC **21–25**, FITB **84–85**, FR **114–115** | Matches membranes LOs (fluid mosaic, diffusion/osmosis, passive vs active, phospholipid tails). |
| 12 | MC **56–60**, FR **128–129** | Matches Darwin/evolution LOs (natural selection, descent with modification, homology, fitness, populations evolve). |
| 15 | MC **71–75**, FR **134–135** | Matches ecology keys (exponential/logistic **K**, trophic levels / ~10% rule, matter cycles vs energy flow). |

**Outcome.** No conflicting topics observed between PT05 prompts and the corresponding module study guides; items sample broadly within each module’s stated objectives rather than duplicating `questions.md` verbatim.

## Conventions

- Student version: `practice-test-NN.md`
- Key: `practice-test-NN_key.md` (same stem + `_key`)

## Processing

- From repo: `cd software && uv run python scripts/generate_all_outputs.py --course biol-1` (with practice tests enabled in [publish.toml](../../../../publish.toml)).
- Publish step copies `practice_tests/` (and `output/`) into `PUBLISHED/biol-1/practice_tests/`.

## Related

- [../exams/AGENTS.md](../exams/AGENTS.md) — formal exams
- [../AGENTS.md](../AGENTS.md) — full course tree
