# Practice Test Format Guide

> **Navigation**: [← Content Types](../README.md) | [Module Format](MODULE_FORMAT.md) | [Exam Format](EXAM_FORMAT.md) | [Syllabus Format](SYLLABUS_FORMAT.md) | [Slides Format](SLIDES_FORMAT.md) | [Lab Format](../LAB_FORMAT.md) | [Course Structure](../COURSE_STRUCTURE.md) | [Architecture](../ARCHITECTURE.md)

Complete guide for authoring practice tests. Practice tests are optional exam-preparation assessments with student versions and answer keys. The pipeline globs `*.md` (excluding `README` / `AGENTS` prefixes) and writes PDFs under `output/` via `process_course_practice_tests` in `software/src/batch_processing/main.py`.

---

## File Naming & Location

| Convention | Example |
|-----------|---------|
| **Student version** | `practice-test-NN.md` |
| **Answer key** | `practice-test-NN_key.md` |
| **Location** | `course_development/biol-1/course/practice_tests/` |
| **Output directory** | `course_development/biol-1/course/practice_tests/output/` |

```
course/practice_tests/
├── practice-test-01.md
├── practice-test-01_key.md
├── practice-test-02.md
├── practice-test-02_key.md
├── practice-test-03.md
├── practice-test-03_key.md
├── practice-test-04.md
├── practice-test-04_key.md
├── practice-test-05.md
├── practice-test-05_key.md
├── README.md
├── AGENTS.md
└── output/
```

### Naming Convention

- **Student version**: `practice-test-NN.md` (zero-padded two-digit number)
- **Answer key**: `practice-test-NN_key.md` (same stem + `_key`)
- **Slug**: lowercase kebab-case throughout

---

## Module Coverage Mapping

BIOL-1 has **5 practice tests** covering progressively wider module ranges:

| Practice Test | Module Coverage | Exam Prep Target |
|---------------|-----------------|------------------|
| `practice-test-01` | Modules **1–4** | Exam 01 (partial) |
| `practice-test-02` | Modules **5–6** | Exam 01 (partial) |
| `practice-test-03` | Modules **7–11** | **Exam 02** |
| `practice-test-04` | Modules **12–16** | **Exam 03** |
| `practice-test-05` | Modules **1–16** | **Comprehensive Final** |

### Assessment Scope Contracts

Each practice test is designed as a parallel-forms assessment for its corresponding exam. The scope contract ensures:

1. **Topic alignment** — practice test items sample broadly within each module's stated learning objectives
2. **No verbatim duplication** — items do not copy `questions.md` content directly
3. **Coverage parity** — module weight in the practice test matches module weight in the corresponding exam
4. **Key term alignment** — terms tested in practice tests match the `[[terms]]` section of each module's `module.toml`

---

## Key Format

The answer key file (`practice-test-NN_key.md`) mirrors the student version's question structure with answers filled in:

```markdown
# Practice Test 01 — Answer Key

## Part A: Multiple Choice

1. **B** — All living organisms are composed of cells.
2. **D** — A scientific theory is supported by many lines of evidence.
3. **A** — Homeostasis maintains stable internal conditions.
...

## Part B: Fill-in-the-Blank

1. **homeostasis**
2. **hypothesis**
...

## Part C: Free Response (Sample Answers)

1. *Sample answer*: The hierarchy of biological organization extends from molecules...
```

---

## Practice Test 05 — Detailed Layout

Practice Test 05 is the comprehensive final-prep assessment with **135 numbered items** across three parts. Cohort framing appears in the student markdown header.

| Part | Item Numbers | Per-Module Pattern |
|------|--------------|---------------------|
| **A — Multiple Choice** | 1–80 | Module N (1–16): (N−1)×5 + 1 through N×5 |
| **B — Fill in the Blank** | 76–105 | Module N: 76 + 2(N−1) and 77 + 2(N−1) |
| **C — Free Response** | 106–135 | Module N: 106 + 2(N−1) and 107 + 2(N−1) |

> **Note**: Part A items 76–80 and Part B items 76–80 overlap in numbering — Part B starts at item 76 in the original assessment design.

### Section Headings

Section headings in Part A match module titles:

```
module-01-study-of-life
module-02-basic-chemistry
...
module-16-capstone-systems-synthesis
```

### Traceability Crosswalk

Each module's PT05 block was matched to that folder's `keys-to-success.md` learning objectives and key terms. Spot-check results:

| Module | PT05 Samples | Alignment Notes |
|--------|-------------|-----------------|
| 01 | MC 1–5, FR 106–107 | Matches Study of Life LOs (cells, scientific method, homeostasis, hierarchy) |
| 05 | MC 21–25, FITB 84–85, FR 114–115 | Matches membranes LOs (fluid mosaic, diffusion/osmosis, passive vs active) |
| 12 | MC 56–60, FR 128–129 | Matches Darwin/evolution LOs (natural selection, descent, homology, fitness) |
| 15 | MC 71–75, FR 134–135 | Matches ecology keys (exponential/logistic K, trophic levels, ~10% rule) |

**Outcome**: No conflicting topics observed between PT05 prompts and module study guides.

---

## Generation Commands

```bash
cd software

# Generate all BIOL-1 outputs (includes practice tests when enabled)
uv run python scripts/generate_all_outputs.py --course biol-1

# The publish step copies practice_tests/ (and output/) into PUBLISHED/biol-1/practice_tests/
python publish.py --skip-git
```

Practice tests are processed by `process_course_practice_tests` in `software/src/batch_processing/main.py`. The publish step copies `practice_tests/` and `output/` into `PUBLISHED/biol-1/practice_tests/`.

> **Note**: Practice test generation requires `include_practice_tests = true` in [`publish.toml`](../../publish.toml).

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [EXAM_FORMAT.md](EXAM_FORMAT.md) | Exam format and practice test parity |
| [README.md](../README.md) | Content types index |
| [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md) | Course directory layout |
| [../../course_development/biol-1/course/practice_tests/AGENTS.md](../../course_development/biol-1/course/practice_tests/AGENTS.md) | Source-level practice test documentation |
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Pipeline and generation workflows |
