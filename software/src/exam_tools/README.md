# exam_tools

> **Navigation**: [← AGENTS.md](AGENTS.md) | [src/ AGENTS.md](../AGENTS.md)

BIOL-1 final exam Part A multiple-choice shuffling and verification toolkit.

## Overview

Provides deterministic, reproducible shuffling of multiple-choice option order for
45 Part A questions on the BIOL-1 final exam, plus a crosswalk verification that
ensures the correct answer text maps to the keyed letter after shuffling.

## Key features

- **Balanced keyed-letter multiset**: 12 A, 11 B, 11 C, 11 D across 45 questions.
- **Deterministic shuffle**: `FINAL_MC_SEED = 20260203` drives both the target-letter
  assignment and the per-question distractor permutation.
- **Dual stem parsing**: Part A questions authored as `**N.**` bold or plain `N.` ordered-list
  are both supported.
- **Crosswalk verification**: After shuffling, each keyed letter's option text is compared
  against the canonical legacy correct-answer text to catch transcription errors.
- **Spacing re-render**: `reshape_part_a_spacing()` re-renders Part A with blank lines
  after stems and between options without reordering options.

## Usage

```python
from src.exam_tools import (
    FINAL_MC_SEED,
    shuffle_exam_markdown,
    crosswalk_verify,
    histogram_report,
    update_key_part_a_answers,
    part_a_keyed_letters_from_key,
    reshape_part_a_spacing,
)

# Shuffle exam markdown
new_md, keyed = shuffle_exam_markdown(exam_text, seed=FINAL_MC_SEED)
crosswalk_verify(new_md, keyed)
print(histogram_report(keyed))

# Update key file
updated_key = update_key_part_a_answers(key_text, keyed)

# Spacing-only re-render (no shuffle)
keyed = part_a_keyed_letters_from_key(key_text)
new_md = reshape_part_a_spacing(exam_text, keyed)
```

CLI entry point: `scripts/shuffle_final_exam_mc.py`

## Module structure

```text
exam_tools/
├── __init__.py    # Re-exports public API
├── main.py        # MCQuestion dataclass + all parsing/shuffling/rendering/verification
├── config.py      # FINAL_MC_SEED, legacy correct letters/texts, regex patterns
├── README.md      # This file
└── AGENTS.md      # Technical doc with function signatures
```
