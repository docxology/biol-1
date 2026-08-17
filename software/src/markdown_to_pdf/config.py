"""Configuration for Markdown to PDF conversion."""

from typing import Any

# Default PDF options
DEFAULT_PDF_OPTIONS: dict[str, Any] = {
    "page_size": "letter",
    "margin_top": "1in",
    "margin_bottom": "1in",
    "margin_left": "1in",
    "margin_right": "1in",
    "encoding": "utf-8",
}

# Default CSS template for PDF styling
DEFAULT_CSS: str = """@page {
    size: letter;
    margin: 1in;
}

body {
    font-family: "Times New Roman", serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #000;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Arial", sans-serif;
    margin-top: 1em;
    margin-bottom: 0.5em;
}

/* Duplex assessment contract: page 1 is removable, page 2 is free response. */
.tearoff-page, .free-response-page, .question-booklet-page {
    break-before: page;
    page-break-before: always;
}
.tearoff-page {
    break-before: auto;
    page-break-before: auto;
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.35;
}
.tearoff-header {
    border-bottom: 2px dashed #444;
    padding-bottom: 6px;
    margin-bottom: 10px;
}
.tearoff-title {
    font-size: 15pt;
    font-weight: bold;
    margin: 0 0 3px 0;
}
.tearoff-subtitle {
    font-size: 9.5pt;
    color: #444;
    margin: 0 0 8px 0;
}
.student-info {
    width: 100%;
    border-collapse: collapse;
}
.student-info td {
    padding: 3px 6px;
    font-size: 10pt;
}
.si-label { width: 8%; font-weight: bold; white-space: nowrap; }
.si-line { border-bottom: 1px solid #222; width: 30%; }
.si-score { width: 12%; }
.tearoff-banner {
    background-color: #f0f4f8;
    border: 1px solid #d0d7de;
    border-left: 4px solid #0969da;
    padding: 6px 10px;
    font-size: 9pt;
    margin-bottom: 12px;
}
.section-heading {
    font-size: 11pt;
    font-weight: bold;
    color: #0969da;
    border-bottom: 1px solid #d0d7de;
    padding-bottom: 3px;
    margin: 10px 0 6px 0;
}
.mc-grid, .fitb-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
}
.mc-grid td {
    padding: 3px 4px;
    font-size: 9.5pt;
    border-bottom: 1px dotted #ccc;
}
.mc-num { font-weight: bold; width: 28px; color: #333; }
.mc-line { width: 42px; border-bottom: 1.5px solid #111 !important; }
.mc-line.empty { border-bottom: none !important; }
.fitb-table td {
    padding: 3px 4px;
    font-size: 9pt;
}
.fitb-num { font-weight: bold; width: 28px; vertical-align: bottom; }
.fitb-line { border-bottom: 1.5px solid #111; height: 16px; }
.fitb-line.empty { border-bottom: none; }
.tearoff-page.compact { font-size: 8.5pt; }
.tearoff-page.compact .mc-grid td { padding: 1.5px 3px; font-size: 8pt; }
.tearoff-page.compact .fitb-table td { padding: 1.5px 3px; font-size: 8pt; }
.tearoff-page.compact .fitb-line { height: 12px; }
.tearoff-page.compact .tearoff-title { font-size: 13pt; }
.tearoff-page.compact .section-heading { font-size: 9.5pt; margin: 6px 0 4px 0; }
.prompt-list { margin: 0 0 10px 18px; padding: 0; }
.prompt-list li { margin-bottom: 6px; }
.prompt-list li p { margin: 0; }
.response-box { margin-bottom: 14px; }
.response-label { font-weight: bold; margin-bottom: 4px; }
.ruled-line { border-bottom: 1px solid #888; height: 24px; }
.page-break { break-before: page; page-break-before: always; }

h1 {
    font-size: 18pt;
    page-break-after: avoid;
}

h2 {
    font-size: 16pt;
    page-break-after: avoid;
}

h3 {
    font-size: 14pt;
    page-break-after: avoid;
}

code {
    font-family: "Courier New", monospace;
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
}

pre {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
    page-break-inside: avoid;
}

img {
    max-width: 100%;
    height: auto;
    page-break-inside: avoid;
}

table {
    border-collapse: collapse;
    width: 100%;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}
"""
