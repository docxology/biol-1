"""Exam-tools package for BIOL-1 final exam Part A MC shuffling and verification."""

from .main import (
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
