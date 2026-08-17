"""Build a printable two-sided, tear-off assessment layout."""

from __future__ import annotations

import re

import markdown as _markdown_lib

_ITEM_RE = re.compile(r"(?m)^\s*(?:\*\*)?\d+\.(?:\*\*)?\s")
_WORD_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}


def _section(markdown_text: str, letter: str) -> str:
    match = re.search(
        rf"(?ms)^## Part {letter}:[^\n]*\n.*?(?=^## Part [A-D]:|\Z)",
        markdown_text,
    )
    if match is None:
        raise ValueError(f"assessment is missing Part {letter}")
    return match.group(0).strip()


def _count_items(section: str) -> int:
    return len(_ITEM_RE.findall(section))


def _markdown_fragment(text: str) -> str:
    """Render a markdown fragment to HTML with the project's extensions."""
    md = _markdown_lib.Markdown(extensions=["extra", "tables", "fenced_code"])
    return md.convert(text)


def _prompt_items(section: str) -> list[str]:
    """Extract numbered prompt bodies from a free-response section."""
    body = re.sub(r"(?m)^## Part [A-D]:[^\n]*\n", "", section).strip()
    # Drop the italic instructions paragraph(s) before the first numbered item.
    first_item = re.search(r"(?m)^\s*(?:\*\*)?\d+\.(?:\*\*)?\s", body)
    if first_item is None:
        return []
    body = body[first_item.start() :]
    parts = re.split(r"(?m)^\s*(?:\*\*)?(\d+)\.(?:\*\*)?\s", body)
    items: list[str] = []
    # parts = [prefix, num, text, num, text, ...]
    for i in range(1, len(parts) - 1, 2):
        text = parts[i + 1].strip()
        # Strip trailing answer-space scaffolding from the prompt text.
        text = re.split(r"(?m)^\s*(?:<br>|\*Answer:\*|\*\*Response)", text, maxsplit=1)[0]
        text = text.replace("<br>", " ").strip()
        if text:
            items.append(text)
    return items


def _choose_count(section: str, fallback: int) -> int:
    """Read 'choose N of M' wording from a section's instructions."""
    match = re.search(
        r"[Cc]hoose\s+(?:\*\*)?([A-Za-z]+|\d+)(?:\*\*)?\s+(?:of|of the following|of the)",
        section,
    )
    if match is None:
        return fallback
    token = match.group(1).lower()
    if token.isdigit():
        return int(token)
    return _WORD_NUMBERS.get(token, fallback)


def _mc_table(mc_count: int, columns: int = 3) -> str:
    rows = -(-mc_count // columns)
    cells: list[str] = []
    for row in range(rows):
        cells.append("<tr>")
        for col in range(columns):
            num = row + col * rows + 1
            if num <= mc_count:
                cells.append(f'<td class="mc-num">{num}.</td><td class="mc-line">&nbsp;</td>')
            else:
                cells.append('<td class="mc-num"></td><td class="mc-line empty"></td>')
        cells.append("</tr>")
    return '<table class="mc-grid">' + "".join(cells) + "</table>"


def _fitb_table(blank_count: int, columns: int = 2) -> str:
    rows = -(-blank_count // columns)
    cells: list[str] = []
    for row in range(rows):
        cells.append("<tr>")
        for col in range(columns):
            num = row + col * rows + 1
            if num <= blank_count:
                cells.append(f'<td class="fitb-num">{num}.</td><td class="fitb-line">&nbsp;</td>')
            else:
                cells.append('<td class="fitb-num"></td><td class="fitb-line empty"></td>')
        cells.append("</tr>")
    return '<table class="fitb-table">' + "".join(cells) + "</table>"


def _lined_box(label: str, lines: int) -> str:
    ruled = "".join('<div class="ruled-line"></div>' for _ in range(lines))
    return f'<div class="response-box"><div class="response-label">{label}</div>{ruled}</div>'


def build_tearoff_assessment(markdown_text: str) -> str:
    """Reorder a student assessment for duplex printing.

    Returns a full HTML document body: page 1 is a compact answer sheet,
    page 2 is free response, and remaining pages are the question booklet.
    """
    part_a = _section(markdown_text, "A")
    part_b = _section(markdown_text, "B")
    part_c = _section(markdown_text, "C")
    part_d = None
    if re.search(r"(?m)^## Part D:", markdown_text):
        part_d = _section(markdown_text, "D")

    first_part = re.search(r"(?m)^## Part [A-D]:", markdown_text)
    if first_part is None:
        raise ValueError("assessment has no Parts")
    introduction = re.sub(
        r"(?m)^\s*<!-- assessment-layout: tearoff-duplex -->\s*\n?",
        "",
        markdown_text[: first_part.start()],
    ).strip()

    title_match = re.search(r"(?m)^#\s+(.+)$", introduction)
    title = title_match.group(1).strip() if title_match else "Assessment"
    subtitle_lines = [
        re.sub(r"\*\*", "", line).strip().strip("*").strip()
        for line in introduction.splitlines()
        if line.strip().startswith("**") and "Instructions" not in line
    ]
    module_line = next(
        (
            re.sub(r"^#+\s*", "", line).strip()
            for line in introduction.splitlines()
            if line.strip().startswith("## ")
        ),
        "",
    )
    points_match = re.search(r"Total Points\*\*:\s*([0-9]+)", introduction)
    total_points = points_match.group(1) if points_match else ""
    subtitle_bits = [
        bit for bit in (module_line, f"{total_points} points total" if total_points else "") if bit
    ]
    seen_subtitle: list[str] = []
    for bit in [*subtitle_lines, *subtitle_bits]:
        if bit and bit not in seen_subtitle:
            seen_subtitle.append(bit)
    subtitle = " | ".join(seen_subtitle[:3])

    mc_count = _count_items(part_a)
    blank_count = _count_items(part_b)
    compact = " compact" if mc_count > 45 or blank_count > 20 else ""
    # Very large answer sheets reserve the entire page for the MC grid and put
    # fill-in lines on the free-response page instead of overflowing page 1.
    split_large = mc_count > 60

    part_a_heading = re.sub(r"^##\s*", "", part_a.splitlines()[0]).strip()
    part_b_heading = re.sub(r"^##\s*", "", part_b.splitlines()[0]).strip()
    part_c_heading = re.sub(r"^##\s*", "", part_c.splitlines()[0]).strip()

    prompts_c = _prompt_items(part_c)
    answer_slots_c = _choose_count(part_c, fallback=len(prompts_c))
    lines_per_box_c = 6 if answer_slots_c <= 3 else 5

    page1 = f"""
<div class="tearoff-page{compact}">
  <div class="tearoff-header">
    <div class="tearoff-title">{title} — Answer Sheet</div>
    <div class="tearoff-subtitle">{subtitle}</div>
    <table class="student-info"><tr>
      <td class="si-label">Name:</td><td class="si-line"></td>
      <td class="si-label">Date:</td><td class="si-line"></td>
      <td class="si-label">Score:</td><td class="si-line si-score"></td>
    </tr></table>
  </div>
  <div class="tearoff-banner">✂️ <strong>TEAR-OFF ANSWER SHEET:</strong> record every
  {part_a_heading} and {part_b_heading} answer on this page. Free response begins on the
  reverse side. Detach and turn in this sheet.</div>
  <div class="section-heading">{part_a_heading}</div>
  {_mc_table(mc_count)}
  {("" if split_large else f'<div class="section-heading">{part_b_heading}</div>' + _fitb_table(blank_count))}
</div>
"""

    prompt_lis = "".join(f"<li>{_markdown_fragment(p)}</li>" for p in prompts_c)
    boxes_c = "".join(
        _lined_box(f"Response {i} — Question Number: ______", lines_per_box_c)
        for i in range(1, answer_slots_c + 1)
    )
    if split_large:
        page2_sections = [
            '<div class="free-response-page">',
            f'<div class="tearoff-header"><div class="tearoff-title">{title} — {part_b_heading}</div>'
            '<div class="tearoff-subtitle">Fill-in answer lines. Record every blank on this page.</div></div>',
            f'<div class="section-heading">{part_b_heading}</div>',
            _fitb_table(blank_count),
            '<div class="page-break"></div>',
            f'<div class="tearoff-header"><div class="tearoff-title">{title} — {part_c_heading}</div>'
            '<div class="tearoff-subtitle">Free response. Write clearly in the lined spaces.</div></div>',
            f'<ol class="prompt-list">{prompt_lis}</ol>',
            boxes_c,
        ]
    else:
        page2_sections = [
            '<div class="free-response-page">',
            f'<div class="tearoff-header"><div class="tearoff-title">{title} — {part_c_heading}</div>'
            '<div class="tearoff-subtitle">Free response. Write clearly in the lined spaces.</div></div>',
            f'<ol class="prompt-list">{prompt_lis}</ol>',
            boxes_c,
        ]
    if part_d is not None:
        part_d_heading = re.sub(r"^##\s*", "", part_d.splitlines()[0]).strip()
        prompts_d = _prompt_items(part_d)
        prompt_lis_d = "".join(f"<li>{_markdown_fragment(p)}</li>" for p in prompts_d)
        page2_sections.extend(
            [
                f'<div class="section-heading">{part_d_heading}</div>',
                f'<ol class="prompt-list">{prompt_lis_d}</ol>',
                _lined_box("Essay response", 18),
            ]
        )
    page2_sections.append("</div>")
    page2 = "".join(page2_sections)

    booklet_body = _markdown_fragment(part_a + "\n\n" + part_b)
    booklet = (
        '<div class="question-booklet-page">'
        '<div class="tearoff-header">'
        f'<div class="tearoff-title">{title} — Question Booklet</div>'
        '<div class="tearoff-subtitle">Answer Parts A and B on the tear-off sheet. '
        "Keep this booklet with your exam materials.</div></div>" + booklet_body + "</div>"
    )

    return page1 + page2 + booklet
