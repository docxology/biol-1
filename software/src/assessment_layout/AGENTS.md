# Assessment layout technical notes

`main.py` contains the pure Markdown transformation used by `markdown_to_pdf`. It requires Parts A, B, and C, preserves question content, and optionally preserves Part D after free response. The source marker is consumed before Markdown conversion so it does not appear in student PDFs.

Tests live in `software/tests/test_assessment_layout.py`; PDF integration coverage is in `test_markdown_to_pdf_main.py`.
