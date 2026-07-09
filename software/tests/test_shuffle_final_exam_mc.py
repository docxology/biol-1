"""Tests for BIOL-1 final exam Part A shuffle helper (balanced keyed letters + crosswalk)."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

from src.exam_tools import (
    FINAL_MC_SEED,
    crosswalk_verify,
    parse_part_a_questions,
    target_letters,
)
from src.exam_tools import main as exam_tools_main

# Compatibility aliases — tests reference these via the loaded module name `sm`.
sm = exam_tools_main


def test_target_letters_balanced_multiset() -> None:
    keyed = target_letters(FINAL_MC_SEED)
    assert Counter(keyed) == Counter({"A": 12, "B": 11, "C": 11, "D": 11})


def test_target_letters_reproducible() -> None:
    assert target_letters(999) == target_letters(999)


def test_parse_part_a_preserves_module_heading() -> None:
    body = """### Module 01 — X

**1.** Stem line
    - A) a
    - B) b
    - C) c
    - D) d

### Module 02 — Y

**2.** Another
    - A) w
    - B) x
    - C) y
    - D) z
"""
    qs, trailing = parse_part_a_questions(body, validate_span=False)
    assert len(qs) == 2
    assert "### Module 02 — Y" in "\n".join(qs[1].preamble_lines)
    assert trailing == ""


def test_parse_part_a_plain_ordered_list_stem() -> None:
    body = """### Module 01 — X

1. Stem line
    - A) a
    - B) b
    - C) c
    - D) d
"""
    qs, _ = parse_part_a_questions(body, validate_span=False)
    assert len(qs) == 1
    assert qs[0].number == 1
    assert "**1.** Stem line" in qs[0].preamble_lines


def test_parse_part_a_skips_blank_lines_between_options() -> None:
    body = """**1.** Stem

    - A) a

    - B) b

    - C) c

    - D) d
"""
    qs, _ = parse_part_a_questions(body, validate_span=False)
    assert len(qs) == 1
    assert qs[0].options == {"A": "a", "B": "b", "C": "c", "D": "d"}


_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*\*\*([ABCD])\*\*\s*\|")


def _keyed_answers_from_key_md(key_md: str) -> list[str]:
    letters: list[tuple[int, str]] = []
    for line in key_md.splitlines():
        m = _ROW_RE.match(line)
        if m:
            qn = int(m.group(1))
            if 1 <= qn <= 45:
                letters.append((qn, m.group(2)))
    letters.sort(key=lambda t: t[0])
    nums = [qn for qn, _ in letters]
    if nums != list(range(1, 46)):
        raise ValueError(f"Missing Part A key rows: got {nums}")
    return [ltr for _, ltr in letters]


def test_repo_final_exam_crosswalk_matches_key() -> None:
    """Checked-in shuffled exam options match Part A Ans column + legacy crosswalk."""
    root = Path(__file__).resolve().parents[2]
    exam_path = root / "course_development/biol-1/course/exams/final-exam.md"
    key_path = root / "course_development/biol-1/course/exams/final-exam_key.md"
    if not exam_path.is_file():
        pytest.skip("final-exam.md not present")
    md = exam_path.read_text(encoding="utf-8")
    key_md = key_path.read_text(encoding="utf-8")
    keyed = _keyed_answers_from_key_md(key_md)
    assert Counter(keyed) == Counter({"A": 12, "B": 11, "C": 11, "D": 11})
    crosswalk_verify(md, keyed)
