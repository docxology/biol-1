# Lab Dashboard Module

> **Navigation**: [← src](../) | [AGENTS.md](AGENTS.md)

## Overview

Generates aligned BIOL-1 lab dashboard HTML files. Each dashboard is a
self-contained HTML page with evidence-capture fields, concept checkpoints,
and key terms — styled to match the BIOL-1 course branding.

The dashboard files are source materials copied into `PUBLISHED/`. This
module keeps their filenames, titles, and study prompts aligned with the
active lab markdown files.

## Usage

### Generate all dashboards

```python
from pathlib import Path
from src.lab_dashboard import render_all_dashboards

written = render_all_dashboards(Path("course_development/biol-1/course/labs/dashboards"))
for path in written:
    print(path)
```

### Dry run (render without writing files)

```python
written = render_all_dashboards(
    Path("course_development/biol-1/course/labs/dashboards"),
    dry_run=True,
)
```

### Render a single dashboard

```python
from src.lab_dashboard import SPECS, render_dashboard

html = render_dashboard(SPECS[0])  # first lab spec
```

## Module Structure

```text
lab_dashboard/
├── __init__.py      # Public API exports
├── main.py          # LabDashboardSpec, SPECS, render_dashboard, render_all_dashboards
├── config.py        # DASHBOARD_DIR path constant
├── README.md        # This file
└── AGENTS.md        # Technical documentation
```

## CLI

The thin CLI orchestrator lives in `software/scripts/generate_biol1_lab_dashboards.py`.
