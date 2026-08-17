"""Build a printable two-sided, tear-off assessment layout."""

from __future__ import annotations

import re


_SECTION_RE = re.compile(r"(?ms)^## Part ([A-D]):[^\n]*\n.*?(?=^## Part [A-D]:|\Z)")
_ITEM_RE = re.compile(r"(?m)^\s*(?:\*\*)?\d+\.(?:\*\*)?\s")


def _section(markdown: str, letter: str) -> str:
    match = re.search(
        rf"(?ms)^## Part {letter}:[^\n]*\n.*?(?=^## Part [A-D]:|\Z)",
        markdown,
    )
    if match is None:
        raise ValueError(f"assessment is missing Part {letter}")
    return match.group(0).strip()


def _count_items(section: str) -> int:
    return len(_ITEM_RE.findall(section))


def build_tearoff_assessment(markdown: str) -> str:
    """Reorder a student assessment for duplex printing.

    Page 1 is a compact answer sheet, page 2 is free response, and the
    remaining pages are the multiple-choice/fill-in question booklet.
    """
    part_a = _section(markdown, "A")
    part_b = _section(markdown, "B")
    part_c = _section(markdown, "C")
    part_d = None
    if re.search(r"(?m)^## Part D:", markdown):
        part_d = _section(markdown, "D")

    first_part = re.search(r"(?m)^## Part [A-D]:", markdown)
    if first_part is None:
        raise ValueError("assessment has no Parts")
    introduction = re.sub(
        r"(?m)^\s*<!-- assessment-layout: tearoff-duplex -->\s*\n?",
        "",
        markdown[: first_part.start()],
    ).rstrip()

    mc_count = _count_items(part_a)
    blank_count = _count_items(part_b)
    answer_lines = [
        "## Multiple-choice answers",
        "\n\n".join(f"{i}. ______" for i in range(1, mc_count + 1)),
        "",
        "## Fill-in answers",
        "\n\n".join(f"{i}. ______________________________" for i in range(1, blank_count + 1)),
    ]
    tearoff = "\n".join(
        [
            '<div class="assessment-page tearoff-page">',
            "## ✂️ TEAR-OFF ANSWER SHEET",
            "",
            "**Write your name and date above. Turn in this page when instructed.**",
            "",
            '<div class="answer-columns">',
            *answer_lines,
            "</div>",
            "",
            "*One answer per line; use the question numbers printed in the booklet.*",
            "</div>",
        ]
    )
    free_response = "\n".join(
        [
            '<div class="assessment-page free-response-page">',
            "## QUESTION BOOKLET — FREE RESPONSE",
            "",
            "**Answer the free-response questions on the lined space provided.**",
            "",
            part_c,
            *(["", part_d] if part_d else []),
            "</div>",
        ]
    )
    objective = "\n".join(
        [
            '<div class="assessment-page question-booklet-page">',
            "## QUESTION BOOKLET — MULTIPLE CHOICE AND FILL-IN",
            "",
            "**Question booklet: answer the questions below using the tear-off sheet for Parts A and B.**",
            "",
            part_a,
            "",
            part_b,
            "</div>",
        ]
    )
    return "\n\n".join([introduction, tearoff, free_response, objective]).strip() + "\n"
