"""Main logic for exam_tools: MC question parsing, shuffling, rendering, and crosswalk verification.

Reads canonical correct-letter positions from the legacy (pre-shuffle) exam layout,
then assigns target keyed letters using FINAL_MC_SEED and per-question distractor shuffles.

Part A stems may be authored as `**N.**` or plain ordered-list `N.` (both are parsed).
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from random import Random

from .config import (
    CORRECT_LETTERS_LEGACY_LAYOUT,
    FINAL_MC_SEED,
    KEY_ROW_RE,
    LEGACY_CORRECT_TEXTS,
    OPTION_LINE,
    QUESTION_HEADER_BOLD,
    QUESTION_HEADER_PLAIN,
)

__all__ = [
    "FINAL_MC_SEED",
    "MCQuestion",
    "crosswalk_verify",
    "histogram_report",
    "parse_part_a_questions",
    "part_a_keyed_letters_from_key",
    "render_question",
    "reshape_part_a_spacing",
    "shuffle_exam_markdown",
    "shuffle_question_options",
    "target_letters",
    "update_key_part_a_answers",
]


@dataclass(frozen=True)
class MCQuestion:
    """One numbered multiple-choice block inside Part A."""

    number: int
    preamble_lines: list[str]
    options: dict[str, str]


def _norm_txt(s: str) -> str:
    """Normalize option text for stable comparisons."""
    t = s.replace("**", "").strip()
    return " ".join(t.split())


def _split_part_a(md: str) -> tuple[str, str, str]:
    """Return (head_before_part_a, part_a_only, tail_from_part_b)."""
    marker = "## Part A: Multiple Choice"
    end = "\n## Part B:"
    i0 = md.find(marker)
    i1 = md.find(end)
    if i0 < 0 or i1 < 0 or i1 <= i0:
        raise ValueError("Could not locate Part A / Part B markers in exam markdown.")
    head = md[:i0]
    part_a = md[i0:i1]
    tail = md[i1:]
    return head, part_a, tail


def _part_a_split_at_question_one(part_a: str) -> tuple[str, str]:
    """Split Part A into intro (through newline before Q1) and body starting at Q1 line."""
    bold = re.search(r"\n\*\*1\.\*\*", part_a)
    plain = re.search(r"\n1\.\s+", part_a)
    candidates: list[tuple[int, str]] = []
    if bold:
        candidates.append((bold.start(), "bold"))
    if plain:
        candidates.append((plain.start(), "plain"))
    if not candidates:
        raise ValueError(
            "Could not find question 1 in Part A (expected a line starting with **1.** or plain '1. ')."
        )
    idx = min(c[0] for c in candidates)
    intro = part_a[: idx + 1]
    body_from_q1 = part_a[idx + 1 :]
    return intro, body_from_q1


def parse_part_a_questions(
    part_a_body: str, *, validate_span: bool = True
) -> tuple[list[MCQuestion], str]:
    """Parse MC blocks for questions 1–45 (stems as **N.** or plain ordered-list `N.`)."""
    lines = part_a_body.splitlines()
    questions: list[MCQuestion] = []
    buffer: list[str] = []
    i = 0

    while i < len(lines):
        mnum = QUESTION_HEADER_BOLD.match(lines[i])
        plain_m: re.Match[str] | None = None
        if not mnum:
            plain_m = QUESTION_HEADER_PLAIN.match(lines[i])
        if not mnum and not plain_m:
            buffer.append(lines[i])
            i += 1
            continue

        if mnum:
            digits = int(mnum.group(2))
            stem_line = mnum.group(1) + mnum.group(3)
        else:
            assert plain_m is not None
            digits = int(plain_m.group(1))
            stem_line = f"**{digits}.** {plain_m.group(2)}"
        preamble = buffer + [stem_line]
        buffer = []
        i += 1

        while i < len(lines):
            om = OPTION_LINE.match(lines[i])
            if om:
                break
            preamble.append(lines[i])
            i += 1

        options: dict[str, str] = {}
        for _ in range(4):
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i >= len(lines):
                raise ValueError(f"Q{digits}: fewer than four option lines.")
            om = OPTION_LINE.match(lines[i])
            if not om:
                raise ValueError(f"Q{digits}: expected option line, got {lines[i]!r}.")
            letter = om.group(2)
            text = om.group(3)
            options[letter] = text
            i += 1

        questions.append(MCQuestion(number=digits, preamble_lines=preamble, options=options))

    trailing = "\n".join(buffer).lstrip("\n")
    if trailing and not trailing.endswith("\n"):
        trailing += "\n"

    questions.sort(key=lambda q: q.number)
    if validate_span and [q.number for q in questions] != list(range(1, 46)):
        raise ValueError(f"Expected questions 1–45, got {[q.number for q in questions]}")
    return questions, trailing


def target_letters(seed: int = FINAL_MC_SEED) -> list[str]:
    letters = ["A"] * 12 + ["B"] * 11 + ["C"] * 11 + ["D"] * 11
    Random(seed).shuffle(letters)
    expect = Counter({"A": 12, "B": 11, "C": 11, "D": 11})
    if Counter(letters) != expect:
        raise RuntimeError("Multiset corrupted.")
    return letters


def shuffle_question_options(q: MCQuestion, target: str, sub_seed: int) -> MCQuestion:
    legacy = CORRECT_LETTERS_LEGACY_LAYOUT[q.number]
    correct_text = q.options[legacy]
    distractors = [q.options[L] for L in ("A", "B", "C", "D") if L != legacy]
    rng = Random(sub_seed)
    rng.shuffle(distractors)

    order_slots = ["A", "B", "C", "D"]
    idx_correct = order_slots.index(target)
    new_texts: list[str | None] = [None, None, None, None]
    new_texts[idx_correct] = correct_text
    empty_indices = [k for k in range(4) if k != idx_correct]
    for slot, dist_text in zip(empty_indices, distractors, strict=True):
        new_texts[slot] = dist_text
    if any(t is None for t in new_texts):
        raise RuntimeError(f"Q{q.number}: failed to fill option slots.")
    assert all(t is not None for t in new_texts)
    new_opts = {L: new_texts[j] for j, L in enumerate(order_slots)}
    return MCQuestion(number=q.number, preamble_lines=list(q.preamble_lines), options=new_opts)


def render_question(q: MCQuestion, indent: str = "    ") -> str:
    lines: list[str] = list(q.preamble_lines)
    lines.append("")
    letters = ("A", "B", "C", "D")
    for idx, L in enumerate(letters):
        lines.append(f"{indent}- {L}) {q.options[L]}")
        if idx < len(letters) - 1:
            lines.append("")
    return "\n".join(lines)


def shuffle_exam_markdown(md: str, seed: int = FINAL_MC_SEED) -> tuple[str, list[str]]:
    head, part_a, tail = _split_part_a(md)
    intro, body_from_q1 = _part_a_split_at_question_one(part_a)
    questions, trailing = parse_part_a_questions(body_from_q1.lstrip("\n"))

    targets = target_letters(seed)
    out_questions = [
        shuffle_question_options(q, tgt, seed + q.number)
        for q, tgt in zip(questions, targets, strict=True)
    ]

    rebuilt_blocks = "\n\n".join(render_question(q) for q in out_questions)
    new_part_a = intro.rstrip("\n") + "\n\n" + rebuilt_blocks + "\n"
    if trailing.strip():
        new_part_a += "\n" + trailing.lstrip("\n")
    return head + new_part_a + tail, targets


def update_key_part_a_answers(key_md: str, answers: list[str]) -> str:
    if len(answers) != 45:
        raise ValueError(f"Expected 45 keyed letters, got {len(answers)}.")
    ans_map = dict(enumerate(answers, start=1))
    row_re = re.compile(r"^(\|\s*\d+\s*\|\s*)\*\*[ABCD]\*\*(\s*\|\s*)(.*)$")
    lines_out: list[str] = []
    for line in key_md.splitlines():
        m = row_re.match(line)
        if m:
            qn_s = re.search(r"\d+", m.group(1))
            if qn_s:
                qn = int(qn_s.group())
                if qn in ans_map:
                    line = f"| {qn} | **{ans_map[qn]}** | {m.group(3)}"
        lines_out.append(line)
    result = "\n".join(lines_out)
    if key_md.endswith("\n"):
        result += "\n"
    return result


def crosswalk_verify(shuffled_md: str, keyed: list[str]) -> None:
    _, part_a, _ = _split_part_a(shuffled_md)
    _, body_from_q1 = _part_a_split_at_question_one(part_a)
    questions, _ = parse_part_a_questions(body_from_q1.lstrip("\n"))
    for q, ans in zip(questions, keyed, strict=True):
        at_letter = _norm_txt(q.options[ans])
        expected = _norm_txt(LEGACY_CORRECT_TEXTS[q.number])
        if at_letter == expected:
            continue
        if expected in at_letter or at_letter in expected:
            continue
        raise ValueError(
            f"Q{q.number}: crosswalk mismatch.\nExpected: {expected}\nGot: {at_letter}"
        )


def histogram_report(keyed: list[str]) -> str:
    c = Counter(keyed)
    return f"A={c['A']} B={c['B']} C={c['C']} D={c['D']}"


def part_a_keyed_letters_from_key(key_md: str) -> list[str]:
    """Return Part A answer letters Q1–Q45 from the markdown key table."""
    pairs: list[tuple[int, str]] = []
    for line in key_md.splitlines():
        m = KEY_ROW_RE.match(line)
        if m:
            qn = int(m.group(1))
            if 1 <= qn <= 45:
                pairs.append((qn, m.group(2)))
    pairs.sort(key=lambda t: t[0])
    nums = [t[0] for t in pairs]
    if nums != list(range(1, 46)):
        raise ValueError(f"Key Part A rows must cover Q1–Q45 once; got {nums}")
    return [ltr for _, ltr in pairs]


def reshape_part_a_spacing(md: str, keyed: list[str]) -> str:
    """Re-render Part A with blank lines after the stem and between options (no reordering)."""
    crosswalk_verify(md, keyed)
    head, part_a, tail = _split_part_a(md)
    intro, body_from_q1 = _part_a_split_at_question_one(part_a)
    questions, trailing = parse_part_a_questions(body_from_q1.lstrip("\n"))
    rebuilt_blocks = "\n\n".join(render_question(q) for q in questions)
    new_part_a = intro.rstrip("\n") + "\n\n" + rebuilt_blocks + "\n"
    if trailing.strip():
        new_part_a += "\n" + trailing.lstrip("\n")
    out = head + new_part_a + tail
    crosswalk_verify(out, keyed)
    return out
