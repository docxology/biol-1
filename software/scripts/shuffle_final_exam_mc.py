#!/usr/bin/env python3
"""Shuffle BIOL-1 final exam Part A MC options with a reproducible balanced-letter layout.

Reads canonical correct-letter positions from the legacy (pre-shuffle) exam layout,
then assigns target keyed letters using FINAL_MC_SEED and per-question distractor shuffles.

Usage:
    uv run python scripts/shuffle_final_exam_mc.py [--dry-run]

Paths default to course_development/biol-1/course/exams/final-exam*.md under repo root.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Final

# Balanced multiset for 45 questions (12 A, 11 each B/C/D).
FINAL_MC_SEED: Final[int] = 20260203

# Legacy correct letters for Part A (recovered BIOL-1 final before any reshuffle).
_CORRECT_LETTERS_LEGACY_LAYOUT: Final[dict[int, str]] = {
    1: "B",
    2: "C",
    3: "B",
    4: "B",
    5: "B",
    6: "B",
    7: "B",
    8: "B",
    9: "C",
    10: "C",
    11: "C",
    12: "C",
    13: "B",
    14: "B",
    15: "B",
    16: "B",
    17: "A",
    18: "A",
    19: "C",
    20: "B",
    21: "C",
    22: "B",
    23: "A",
    24: "B",
    25: "B",
    26: "C",
    27: "B",
    28: "B",
    29: "B",
    30: "B",
    31: "B",
    32: "B",
    33: "B",
    34: "A",
    35: "B",
    36: "B",
    37: "B",
    38: "B",
    39: "B",
    40: "A",
    41: "B",
    42: "B",
    43: "B",
    44: "B",
    45: "B",
}


@dataclass(frozen=True)
class MCQuestion:
    """One numbered multiple-choice block inside Part A."""

    number: int
    preamble_lines: list[str]
    options: dict[str, str]


_OPTION_LINE = re.compile(r"^(\s*)-\s([A-D])\)\s(.*)$")


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


def parse_part_a_questions(
    part_a_body: str, *, validate_span: bool = True
) -> tuple[list[MCQuestion], str]:
    """Parse MC question blocks starting at **1.** through **45.** plus trailing lines (e.g. rule)."""
    lines = part_a_body.splitlines()
    questions: list[MCQuestion] = []
    buffer: list[str] = []
    i = 0

    while i < len(lines):
        mnum = re.match(r"^(\*\*\d+\.\*\*)(.*)$", lines[i])
        if not mnum:
            buffer.append(lines[i])
            i += 1
            continue

        digits_m = re.search(r"\d+", mnum.group(1))
        if digits_m is None:
            raise ValueError(f"Malformed question header: {lines[i]!r}")
        digits = int(digits_m.group())
        preamble = buffer + [mnum.group(1) + mnum.group(2)]
        buffer = []
        i += 1

        while i < len(lines):
            om = _OPTION_LINE.match(lines[i])
            if om:
                break
            preamble.append(lines[i])
            i += 1

        options: dict[str, str] = {}
        for _ in range(4):
            if i >= len(lines):
                raise ValueError(f"Q{digits}: fewer than four option lines.")
            om = _OPTION_LINE.match(lines[i])
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
    legacy = _CORRECT_LETTERS_LEGACY_LAYOUT[q.number]
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
    new_opts = {L: new_texts[j] for j, L in enumerate(order_slots)}
    return MCQuestion(number=q.number, preamble_lines=list(q.preamble_lines), options=new_opts)


def render_question(q: MCQuestion, indent: str = "    ") -> str:
    lines: list[str] = list(q.preamble_lines)
    for L in ("A", "B", "C", "D"):
        lines.append(f"{indent}- {L}) {q.options[L]}")
    return "\n".join(lines)


def shuffle_exam_markdown(md: str, seed: int = FINAL_MC_SEED) -> tuple[str, list[str]]:
    head, part_a, tail = _split_part_a(md)
    idx = part_a.find("\n**1.**")
    if idx < 0:
        raise ValueError("Could not find first MC question **1.** in Part A.")
    intro = part_a[: idx + 1]
    body_from_q1 = part_a[idx + 1 :]
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


_LEGACY_CORRECT_TEXTS: Final[dict[int, str]] = {
    1: "Atom → Molecule → Cell → Tissue → Organ",
    2: "A testable prediction or explanation that can be supported or refuted with evidence",
    3: "Ability of an organism to maintain stable internal conditions amid external change",
    4: "Protons in its atoms (under neutral atoms, sets identity of element)",
    5: "Share electrons between nuclei",
    6: "Hydrogen bonding creates an open lattice in ice that is less dense than liquid water",
    7: "Condensation / dehydration synthesis",
    8: "Nucleic acids (DNA / RNA)",
    9: "Proteins (sometimes RNA catalysts) that speed specific reactions by lowering activation energy",
    10: "All living organisms are made of cells and cells come from pre-existing cells (modern framing includes revisions but retains core ideas)",
    11: "Mitochondrion",
    12: "Membrane-bound nucleus",
    13: "A lipid bilayer with embedded proteins that can move laterally",
    14: "Down the molecule’s concentration gradient without direct metabolic energy for the crossing itself",
    15: "Diffusion of **water** across a selectively permeable membrane",
    16: "Energy stored in its phosphate bonds can be transferred to drive cellular work when hydrolyzed / regenerated in coupled reactions",
    17: "Uses oxygen and breaks fuel molecules to capture usable energy (often linked to ATP production)",
    18: "Binds substrates and catalyzes conversion to products for that reaction",
    19: "Ribosomes synthesizing polypeptides using an mRNA code",
    20: "DNA polymerase adding complementary nucleotides",
    21: "Contains ribose (often single-stranded functional molecules such as mRNA, tRNA, rRNA)",
    22: "Haploid (n)",
    23: "Prophase I of meiosis",
    24: "Two genetically identical diploid daughter cells (barring mutation)",
    25: "Alleles",
    26: "**3 dominant-looking : 1 recessive-looking** among offspring (classic single-gene expectation)",
    27: "Heterozygotes show an intermediate phenotype between homozygotes",
    28: "Alter gene activity **without** necessarily changing the DNA sequence itself",
    29: "Reduces transcription / promotes a gene-off state compared with unmethylated promoter regions in many examples",
    30: "One X is largely condensed / silenced in each somatic cell for dosage compensation",
    31: "Amplify targeted DNA sequences from small samples",
    32: "The positive electrode; smaller fragments often travel farther in a given time",
    33: "Target specific DNA sequences for cutting / editing with guide RNA assistance",
    34: "Populations tend to produce **more offspring than can survive and reproduce**",
    35: "Shared ancestry with structural modification under different selective regimes",
    36: "Relative contribution of alleles to future generations through survival and reproduction",
    37: "Move alleles between populations through migration and mating—often homogenizing allele frequencies between connected groups over time (depending on rates)",
    38: "Population size is **small** so random sampling shifts allele frequencies strongly between generations",
    39: "A mathematical **null / baseline** against which observed allele-frequency change is interpreted",
    40: "Temporal isolation",
    41: "Postzygotic reduced hybrid fertility",
    42: "Allopatric speciation starting with geographic isolation",
    43: "Growth slows as **N** approaches **K** (carrying capacity)",
    44: "Density-dependent regulation (impact intensifies with density in many textbook examples)",
    45: "Lost largely as heat between trophic transfers—supporting fewer top consumers than low trophic levels per unit primary production",
}


def crosswalk_verify(shuffled_md: str, keyed: list[str]) -> None:
    _, part_a, _ = _split_part_a(shuffled_md)
    idx = part_a.find("\n**1.**")
    body_from_q1 = part_a[idx + 1 :] if idx >= 0 else part_a
    questions, _ = parse_part_a_questions(body_from_q1.lstrip("\n"))
    for q, ans in zip(questions, keyed, strict=True):
        at_letter = _norm_txt(q.options[ans])
        expected = _norm_txt(_LEGACY_CORRECT_TEXTS[q.number])
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


def repo_root_from_scripts() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Compute shuffle only; do not write files."
    )
    parser.add_argument(
        "--seed", type=int, default=FINAL_MC_SEED, help="RNG seed (default FINAL_MC_SEED)."
    )
    args = parser.parse_args(argv)

    root = repo_root_from_scripts()
    exam_path = root / "course_development/biol-1/course/exams/final-exam.md"
    key_path = root / "course_development/biol-1/course/exams/final-exam_key.md"
    exam_text = exam_path.read_text(encoding="utf-8")
    key_text = key_path.read_text(encoding="utf-8")

    new_exam, keyed = shuffle_exam_markdown(exam_text, seed=args.seed)
    crosswalk_verify(new_exam, keyed)
    print(f"FINAL_MC_SEED={args.seed} Part A histogram: {histogram_report(keyed)}")

    if args.dry_run:
        return 0

    key_updated = update_key_part_a_answers(key_text, keyed)
    exam_path.write_text(new_exam, encoding="utf-8")
    key_path.write_text(key_updated, encoding="utf-8")
    print(f"Wrote {exam_path.relative_to(root)} and {key_path.relative_to(root)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
