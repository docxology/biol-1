"""Tests for BIOL-1 final exam Part A shuffle helper (balanced keyed letters + crosswalk)."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

from src.exam_tools import (
    FINAL_MC_SEED,
    MCQuestion,
    crosswalk_verify,
    histogram_report,
    parse_part_a_questions,
    part_a_keyed_letters_from_key,
    render_question,
    reshape_part_a_spacing,
    shuffle_exam_markdown,
    shuffle_question_options,
    target_letters,
    update_key_part_a_answers,
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


class TestShuffleQuestionOptions:
    """Direct unit tests for shuffle_question_options (Q1's legacy-correct letter is B)."""

    def test_moves_correct_text_to_target_letter(self) -> None:
        q = MCQuestion(
            number=1,
            preamble_lines=["**1.** Stem"],
            options={"A": "opt-A", "B": "the-correct-one", "C": "opt-C", "D": "opt-D"},
        )
        shuffled = shuffle_question_options(q, target="C", sub_seed=42)
        assert shuffled.number == 1
        assert shuffled.options["C"] == "the-correct-one"

    def test_preserves_full_distractor_multiset(self) -> None:
        q = MCQuestion(
            number=1,
            preamble_lines=["**1.** Stem"],
            options={"A": "opt-A", "B": "the-correct-one", "C": "opt-C", "D": "opt-D"},
        )
        shuffled = shuffle_question_options(q, target="A", sub_seed=7)
        assert sorted(shuffled.options.values()) == sorted(q.options.values())
        assert shuffled.options["A"] == "the-correct-one"

    def test_preserves_preamble_lines(self) -> None:
        q = MCQuestion(
            number=1,
            preamble_lines=["### Module 01 — X", "", "**1.** Stem"],
            options={"A": "opt-A", "B": "the-correct-one", "C": "opt-C", "D": "opt-D"},
        )
        shuffled = shuffle_question_options(q, target="D", sub_seed=1)
        assert shuffled.preamble_lines == q.preamble_lines


class TestRenderQuestion:
    def test_renders_stem_and_all_four_options_in_order(self) -> None:
        q = MCQuestion(
            number=1,
            preamble_lines=["**1.** Stem"],
            options={"A": "aa", "B": "bb", "C": "cc", "D": "dd"},
        )
        rendered = render_question(q)
        assert rendered.startswith("**1.** Stem")
        assert "- A) aa" in rendered
        assert "- B) bb" in rendered
        assert "- C) cc" in rendered
        assert "- D) dd" in rendered
        # Options must appear in A, B, C, D order.
        assert (
            rendered.index("- A)")
            < rendered.index("- B)")
            < rendered.index("- C)")
            < rendered.index("- D)")
        )


class TestShuffleExamMarkdownRoundTrip:
    """Build a small synthetic 45-question exam and verify shuffle + crosswalk round-trip."""

    @staticmethod
    def _make_question_block(n: int, legacy_correct_letter: str) -> str:
        options = {"A": f"q{n}-A", "B": f"q{n}-B", "C": f"q{n}-C", "D": f"q{n}-D"}
        lines = [f"**{n}.** Question {n} stem", ""]
        letters = ("A", "B", "C", "D")
        for idx, letter in enumerate(letters):
            lines.append(f"    - {letter}) {options[letter]}")
            if idx < 3:
                lines.append("")
        return "\n".join(lines)

    def _build_synthetic_exam(self) -> str:
        blocks = [
            self._make_question_block(n, exam_tools_main.CORRECT_LETTERS_LEGACY_LAYOUT[n])
            for n in range(1, 46)
        ]
        part_a_body = "\n\n".join(blocks)
        return (
            "# Final Exam\n\n"
            "## Part A: Multiple Choice\n\n"
            f"{part_a_body}\n\n"
            "## Part B: Free Response\n\n"
            "Some free response content.\n"
        )

    def test_shuffle_then_crosswalk_verify_round_trips(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Use each question's own synthetic option text as the "legacy correct text"
        # so crosswalk_verify (which checks against LEGACY_CORRECT_TEXTS) succeeds.
        synthetic_correct_texts = {
            n: f"q{n}-{exam_tools_main.CORRECT_LETTERS_LEGACY_LAYOUT[n]}" for n in range(1, 46)
        }
        monkeypatch.setattr(exam_tools_main, "LEGACY_CORRECT_TEXTS", synthetic_correct_texts)

        md = self._build_synthetic_exam()
        shuffled_md, keyed = shuffle_exam_markdown(md, seed=FINAL_MC_SEED)

        assert Counter(keyed) == Counter({"A": 12, "B": 11, "C": 11, "D": 11})
        # Round trip must not raise.
        crosswalk_verify(shuffled_md, keyed)
        assert "## Part B: Free Response" in shuffled_md
        assert "Some free response content." in shuffled_md


class TestUpdateKeyPartAAnswers:
    def _make_key_md(self) -> str:
        rows = [f"| {n} | **A** | some explanation {n} |" for n in range(1, 46)]
        return "# Key\n\n" + "\n".join(rows) + "\n"

    def test_rewrites_only_part_a_key_rows(self) -> None:
        key_md = self._make_key_md()
        new_answers = target_letters(FINAL_MC_SEED)
        updated = update_key_part_a_answers(key_md, new_answers)
        recovered = part_a_keyed_letters_from_key(updated)
        assert recovered == new_answers
        # Explanation text after the answer column must be preserved verbatim.
        assert "some explanation 1" in updated
        assert "some explanation 45" in updated

    def test_rejects_wrong_length_answers_list(self) -> None:
        key_md = self._make_key_md()
        with pytest.raises(ValueError, match="Expected 45 keyed letters"):
            update_key_part_a_answers(key_md, ["A"] * 44)


class TestPartAKeyedLettersFromKey:
    def test_raises_on_incomplete_key_rows(self) -> None:
        # Only 44 of the required 45 rows present.
        rows = [f"| {n} | **A** | text |" for n in range(1, 45)]
        key_md = "# Key\n\n" + "\n".join(rows) + "\n"
        with pytest.raises(ValueError, match="Q1–Q45"):
            part_a_keyed_letters_from_key(key_md)


class TestHistogramReport:
    def test_reports_letter_counts(self) -> None:
        report = histogram_report(["A", "A", "B", "C", "C", "C"])
        assert report == "A=2 B=1 C=3 D=0"


class TestReshapePartASpacing:
    def test_is_a_noop_on_option_ordering(self, monkeypatch: pytest.MonkeyPatch) -> None:
        synthetic_correct_texts = {
            n: f"q{n}-{exam_tools_main.CORRECT_LETTERS_LEGACY_LAYOUT[n]}" for n in range(1, 46)
        }
        monkeypatch.setattr(exam_tools_main, "LEGACY_CORRECT_TEXTS", synthetic_correct_texts)

        blocks = [
            TestShuffleExamMarkdownRoundTrip._make_question_block(
                n, exam_tools_main.CORRECT_LETTERS_LEGACY_LAYOUT[n]
            )
            for n in range(1, 46)
        ]
        part_a_body = "\n\n".join(blocks)
        md = (
            "# Final Exam\n\n"
            "## Part A: Multiple Choice\n\n"
            f"{part_a_body}\n\n"
            "## Part B: Free Response\n\n"
            "Some free response content.\n"
        )
        keyed = [exam_tools_main.CORRECT_LETTERS_LEGACY_LAYOUT[n] for n in range(1, 46)]

        reshaped = reshape_part_a_spacing(md, keyed)

        questions_before, _ = parse_part_a_questions(
            md[md.index("## Part A") : md.index("## Part B")].split("Multiple Choice\n\n", 1)[1]
        )
        questions_after, _ = parse_part_a_questions(
            reshaped[reshaped.index("## Part A") : reshaped.index("## Part B")].split(
                "Multiple Choice\n\n", 1
            )[1]
        )
        assert [q.options for q in questions_before] == [q.options for q in questions_after]


class TestParsePartAQuestionsErrors:
    def test_raises_on_fewer_than_four_options(self) -> None:
        body = """**1.** Stem
    - A) a
    - B) b
    - C) c
"""
        with pytest.raises(ValueError, match="fewer than four option lines"):
            parse_part_a_questions(body, validate_span=False)

    def test_raises_on_malformed_option_line(self) -> None:
        body = """**1.** Stem
    - A) a
    - B) b
    - C) c
    not an option line
"""
        with pytest.raises(ValueError, match="expected option line"):
            parse_part_a_questions(body, validate_span=False)

    def test_raises_on_non_contiguous_question_numbers_when_span_validated(self) -> None:
        body = """**1.** Stem
    - A) a
    - B) b
    - C) c
    - D) d

**3.** Another
    - A) a
    - B) b
    - C) c
    - D) d
"""
        with pytest.raises(ValueError, match="Expected questions 1"):
            parse_part_a_questions(body, validate_span=True)
