# Lab Protocol Format Guide

> **Navigation**: [← README](README.md) | [Dashboard Format](DASHBOARD_FORMAT.md) | [Architecture](ARCHITECTURE.md) | [Orchestration](ORCHESTRATION.md)

Complete guide for authoring lab protocols. Labs are Markdown files processed by the `lab_manual` module into fillable PDFs and interactive HTML pages.

---

## File Naming & Location

| Convention | Example |
|-----------|---------|
| **Pattern** | `lab-XX_topic-name.md` |
| **Location** | `course_development/biol-1/course/labs/` |
| **Dashboards** | `course_development/biol-1/course/labs/dashboards/` |

Number labs with zero-padded two-digit prefixes. **Expected numbered protocol ranges** track `publish.toml`: the active Fall 2026 **BIOL-1** course has labs `01`–`17` (`max_lab = 17`), plus optional supplemental `lab-*.md` files if needed. Spring 2026 BIOL-8 lab formats are historical reference material under [`../../archive/spring-2026/course_development/biol-8/course/labs/`](../../archive/spring-2026/course_development/biol-8/course/labs/). Use lowercase kebab-case for the topic slug.

---

## Required Document Structure

Every lab protocol must follow this section order:

```markdown
# Lab X: Title — Subtitle

**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay

---

## Learning Objectives & Goals

By the end of this lab, you will be able to:

- **Verb** objective description
- **Verb** objective description

---

## Introduction

Background context paragraph(s).

---

## Materials Needed

- Material 1
- Material 2

---

## Safety Notes

> ⚠️ Safety warning text.

---

## Procedure

### Part 1: Section Title

Step-by-step instructions.

### Part 2: Section Title

More instructions.

---

## Data Collection

<!-- lab:data-table rows=5 -->
| Column A | Column B | Column C |
|----------|----------|----------|
| {fill}   | {fill}   | {fill}   |
<!-- /lab:data-table -->

---

## Analysis & Questions

<!-- lab:reflection -->
Question text
{fill:textarea rows=4}
<!-- /lab:reflection -->

---

## Conclusions

{fill:textarea rows=5}
```

### Header Format

The first two lines are always:

1. **H1 title**: `# Lab X: Title — Subtitle`
2. **Course line**: `**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay`

The `lab_manual` module strips these when `include_header=True` (default) to avoid duplicating the rendered header block.

---

## Lab Directive Syntax

Lab directives are HTML comments processed by the `lab_manual` module into interactive HTML elements (for HTML output) or styled fillable fields (for PDF output).

### `{fill:text}` — Single-Line Input

Inline fillable text field. Renders as an underlined input in PDF or `<input>` in HTML.

```markdown
Student Name: {fill:text}
Temperature reading: {fill:text} °C
```

### `{fill:textarea rows=N}` — Multi-Line Text Area

Block-level fillable area. The `rows` parameter controls height.

```markdown
Describe your observations:
{fill:textarea rows=5}
```

### `<!-- lab:data-table -->` — Fillable Data Table

Wraps a Markdown table with fillable cells. Supports `rows=N` and `title="..."` attributes.

```markdown
<!-- lab:data-table rows=10 title="Measurement Data" -->
| Trial | Mass (g) | Volume (mL) | Density (g/mL) |
|-------|----------|-------------|----------------|
| {fill}| {fill}   | {fill}      | {fill}         |
<!-- /lab:data-table -->
```

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `rows` | No | 5 | Number of data rows |
| `title` | No | None | Table caption |

The column headers come from the Markdown table header row.

### `<!-- lab:object-selection -->` — Object Selection

Interactive object selection with two fields (in-room and not-in-room objects).

```markdown
<!-- lab:object-selection -->
Object in room: {fill:text}
Object NOT in room: {fill:text}
<!-- /lab:object-selection -->
```

### `<!-- lab:reflection -->` — Reflection Box

Styled reflection/analysis section with a left accent border.

```markdown
<!-- lab:reflection -->
What patterns did you observe in your data?
{fill:textarea rows=4}
<!-- /lab:reflection -->
```

### `<!-- lab:measurement-feasibility -->` — Feasibility Analysis

Section for analyzing measurement feasibility with checkboxes.

```markdown
<!-- lab:measurement-feasibility -->
Which aspects COULD we measure tonight?
{fill:textarea rows=3}

How might we get those other measurements?
- [ ] Internet access
- [ ] Money/funding
- [ ] Other: {fill:text}
<!-- /lab:measurement-feasibility -->
```

### `<!-- lab:calculation -->` — Calculation Box

Styled box for showing calculations, formulas, or worked examples.

```markdown
<!-- lab:calculation -->
**Density Formula:**

density = mass ÷ volume

Calculate the density of your object:
{fill:textarea rows=3}
<!-- /lab:calculation -->
```

---

## Inline HTML for Special Rendering

The PDF pipeline uses **WeasyPrint**, which renders inline HTML and CSS. This is useful for elements that cannot be expressed in standard Markdown.

### When to Use Inline HTML

- Chromosome cutouts or tear-out manipulatives
- Colored or styled boxes beyond what Markdown supports
- Page break control (`<div style="page-break-before: always;"></div>`)
- Custom table layouts with specific widths/colors

### Example: Styled Chromosome Cutouts

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 12px 0;">
  <div style="border: 2px dashed #c41e3a; padding: 12px; text-align: center;
              background: #fff5f5; border-radius: 6px;">
    <div style="font-size: 9px; color: #666;">✂️ Cut along dashed line</div>
    <div style="font-size: 28px; font-weight: bold; color: #c41e3a;">A</div>
    <div style="font-size: 10px;">Maternal — Gene 1 (dominant)</div>
  </div>
  <div style="border: 2px dashed #2563eb; padding: 12px; text-align: center;
              background: #f0f4ff; border-radius: 6px;">
    <div style="font-size: 9px; color: #666;">✂️ Cut along dashed line</div>
    <div style="font-size: 28px; font-weight: bold; color: #2563eb;">a</div>
    <div style="font-size: 10px;">Paternal — Gene 1 (recessive)</div>
  </div>
</div>
```

> **Note**: Use inline styles exclusively — WeasyPrint does not load external stylesheets from HTML comment blocks.

### Page Breaks

Force a page break for worksheets or appendices:

```html
<div style="page-break-before: always;"></div>
```

---

## Tear-Out Worksheets & Appendices

### Ordering Convention

Lab documents should follow this page order:

1. **Lab Protocol** — Instructions, procedure, safety
2. **Tear-Out Worksheet** — Data tables, questions, analysis (with page break before)
3. **Appendices** — Cutouts, templates, reference materials (always last)

### Worksheet Header

Include a header on the worksheet page:

```markdown
<div style="page-break-before: always;"></div>

## Tear-Out Worksheet

**Name:** _________________ **Date:** _________________

> Complete this worksheet during the lab activity. Tear out and submit.
```

---

## Lab Templates

The `lab_manual` module provides starter templates via Python API:

```python
from src.lab_manual.main import get_lab_template

# Available templates: "basic", "measurement", "observation"
template = get_lab_template("measurement")
Path("new-lab.md").write_text(template)
```

| Template | Directives Included | Best For |
|----------|-------------------|----------|
| `basic` | data-table, reflection, textarea | Simple data collection labs |
| `measurement` | object-selection, data-table, measurement-feasibility, reflection | Measurement & observation labs |
| `observation` | data-table, reflection | Field observation labs |

---

## Generation Commands

### Single Lab

```bash
# PDF
cd software && uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual('course_development/biol-1/course/labs/lab-01_measurement-methods.md',
                  'output/lab-01.pdf', output_format='pdf', course_name='BIOL-1')
"

# HTML (interactive)
cd software && uv run python -c "
from src.lab_manual.main import render_lab_manual
render_lab_manual('course_development/biol-1/course/labs/lab-01_measurement-methods.md',
                  'output/lab-01.html', output_format='html', course_name='BIOL-1')
"
```

### Batch Generation

```bash
# Lab manuals run as part of the standard course-wide script (omit --skip-labs)
cd software && uv run python scripts/generate_all_outputs.py --course biol-1

# Limit how many numbered labs are rendered for that course
cd software && uv run python scripts/generate_all_outputs.py --course biol-1 --max-lab biol-1:5
```

There is no `--labs-only` flag on `generate_all_outputs.py`; use `render_lab_manual` (above) or the orchestration helpers for narrower runs.

See [ORCHESTRATION.md#lab-manual-generation](ORCHESTRATION.md#lab-manual-generation) for advanced options.

---

## HTML Interactive Features

When rendered as HTML, lab manuals include JavaScript for:

| Feature | Description |
|---------|-------------|
| **Auto-Save** | Form data saved to `localStorage` on every input change |
| **Load Saved** | Previously entered data restored on page load |
| **Clear Data** | Button to wipe all saved progress |
| **Print** | Print-friendly button that triggers `window.print()` |

These are powered by the `LAB_INTERACTIVE_JS` constant in `src/lab_manual/config.py`.

---

## Canonical Examples

| Lab | Key Features | File |
|-----|-------------|------|
| Lab 01: Measurement Methods | Object selection, measurement tables, feasibility | `lab-01_measurement-methods.md` |
| Lab 04: Diffusion & Membranes | Data tables, reflection, multi-part procedure | `lab-04_diffusion-membranes.md` |
| Lab 07: Cell Division | Inline HTML cutouts, tear-out worksheet | `lab-07_cell-division.md` |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md) | Interactive dashboard format guide |
| [OUTPUT_PDF.md](OUTPUT_PDF.md) | PDF output format details |
| [OUTPUT_HTML.md](OUTPUT_HTML.md) | HTML output format details |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Lab generation workflows |
| [../src/lab_manual/README.md](../src/lab_manual/README.md) | Module-level documentation |
