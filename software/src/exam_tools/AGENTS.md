# exam_tools — Technical Documentation

> **Navigation**: [← README](README.md) | [src/ AGENTS.md](../AGENTS.md)

## Overview

BIOL-1 final exam Part A multiple-choice shuffling and verification toolkit. Moves all
parsing, shuffling, rendering, and crosswalk logic out of `scripts/shuffle_final_exam_mc.py`
into a reusable `src/` package.

**Layer**: 0 (foundation — no dependencies on sibling modules).

**Standalone**: Yes — depends only on the standard library (`re`, `random`, `dataclasses`,
`collections`).

## Module structure

```text
exam_tools/
├── __init__.py    # Re-exports public API from main.py
├── main.py        # MCQuestion dataclass + all functions
├── config.py      # FINAL_MC_SEED, legacy correct letters/texts, regex patterns
├── README.md      # User-facing overview
└── AGENTS.md      # This file
```

## Configuration constants (config.py)

| Constant | Type | Description |
|---|---|---|
| `FINAL_MC_SEED` | `Final[int]` | `20260203` — balanced multiset seed for 45 questions. |
| `CORRECT_LETTERS_LEGACY_LAYOUT` | `Final[dict[int, str]]` | Legacy correct-letter positions for Q1–Q45. |
| `LEGACY_CORRECT_TEXTS` | `Final[dict[int, str]]` | Canonical correct-answer text for Q1–Q45 (for crosswalk). |
| `OPTION_LINE` | `Final[re.Pattern[str]]` | Matches `- A) option text` lines. |
| `QUESTION_HEADER_BOLD` | `Final[re.Pattern[str]]` | Matches `**N.**` bold question headers. |
| `QUESTION_HEADER_PLAIN` | `Final[re.Pattern[str]]` | Matches `N.` plain ordered-list headers. |
| `KEY_ROW_RE` | `Final[re.Pattern[str]]` | Matches key table rows `\| N \| **A** \|`. |

## Public API (main.py)

### Dataclass

```python
@dataclass(frozen=True)
class MCQuestion:
    number: int
    preamble_lines: list[str]
    options: dict[str, str]
```

### Functions

```python
def parse_part_a_questions(
    part_a_body: str, *, validate_span: bool = True
) -> tuple[list[MCQuestion], str]
```
Parse MC blocks for questions 1–45. Supports `**N.**` bold and plain `N.` ordered-list stems.
Returns sorted questions and any trailing text after the last question.

---

```python
def target_letters(seed: int = FINAL_MC_SEED) -> list[str]
```
Generate a balanced 45-letter multiset (12 A, 11 B, 11 C, 11 D) shuffled deterministically.

---

```python
def shuffle_question_options(q: MCQuestion, target: str, sub_seed: int) -> MCQuestion
```
Shuffle one question's distractors so the correct answer lands at `target` letter.
Uses `CORRECT_LETTERS_LEGACY_LAYOUT` to identify the correct option text.

---

```python
def render_question(q: MCQuestion, indent: str = "    ") -> str
```
Render a question as markdown with blank lines after the stem and between options.

---

```python
def shuffle_exam_markdown(md: str, seed: int = FINAL_MC_SEED) -> tuple[str, list[str]]
```
Full pipeline: split exam markdown, parse Part A, shuffle all 45 questions, rebuild.
Returns `(new_markdown, keyed_letters)`.

---

```python
def update_key_part_a_answers(key_md: str, answers: list[str]) -> str
```
Replace Part A answer letters in the key table markdown with the new shuffled keyed letters.

---

```python
def crosswalk_verify(shuffled_md: str, keyed: list[str]) -> None
```
Verify that each keyed letter's option text matches the canonical legacy correct text.
Raises `ValueError` on mismatch.

---

```python
def histogram_report(keyed: list[str]) -> str
```
Return a compact `A=12 B=11 C=11 D=11` histogram string.

---

```python
def part_a_keyed_letters_from_key(key_md: str) -> list[str]
```
Extract Part A answer letters Q1–Q45 from the markdown key table.

---

```python
def reshape_part_a_spacing(md: str, keyed: list[str]) -> str
```
Re-render Part A with blank lines after stems and between options (no reordering).
Runs crosswalk verification before and after.

## Downstream callers

| Caller | Path | Purpose |
|---|---|---|
| `shuffle_final_exam_mc.py` | `software/scripts/` | CLI entry point — arg parsing + orchestration |
| `test_shuffle_final_exam_mc.py` | `software/tests/` | Unit + repo integration tests |

## Testing

```bash
cd software && uv run pytest tests/test_shuffle_final_exam_mc.py -q --no-cov
```
