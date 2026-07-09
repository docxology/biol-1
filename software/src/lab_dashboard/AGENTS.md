# Lab Dashboard Module — Technical Documentation

## Overview

BIOL-1 lab dashboard HTML generation. Each of the 17 lab specs produces a
self-contained HTML page with evidence capture, concept checks, and key terms.

## Module Structure

```text
lab_dashboard/
├── __init__.py      # Re-exports public API from main.py
├── main.py          # LabDashboardSpec, SPECS, render_dashboard, render_all_dashboards
├── config.py        # REPO_ROOT, DASHBOARD_DIR path constants
├── README.md        # User-facing overview
└── AGENTS.md        # This file
```

## Standalone: Yes

This module uses only the Python standard library (`dataclasses`, `html`, `pathlib`).
No external dependencies.

## Public API

### `LabDashboardSpec` (dataclass, frozen)

```python
@dataclass(frozen=True)
class LabDashboardSpec:
    number: int
    slug: str
    title: str
    module: str
    focus: str
    evidence: tuple[str, str, str]
    checkpoints: tuple[str, str, str]
    terms: tuple[str, str, str, str]

    @property
    def filename(self) -> str  # → "lab-NN_slug-dashboard.html"
```

### `SPECS`

```python
SPECS: tuple[LabDashboardSpec, ...]
```

17 lab dashboard specifications covering Modules 01–15 plus three exam review dashboards.

### `render_dashboard(spec: LabDashboardSpec) -> str`

Render a single lab dashboard as a complete HTML document string.

**Parameters:**
- `spec`: A `LabDashboardSpec` instance.

**Returns:** Complete HTML document string with embedded CSS and JavaScript.

### `render_all_dashboards(dashboard_dir: Path, dry_run: bool = False) -> list[str]`

Write all dashboard HTML files to `dashboard_dir`.

**Parameters:**
- `dashboard_dir`: Target directory for generated files. Created if it does not exist.
- `dry_run`: If `True`, skip file writes; return paths that *would* be written.

**Returns:** List of file path strings that were written (or would be written).

**Side effects:**
- Creates `dashboard_dir` if it does not exist (non-dry-run only).
- Removes existing `lab-*-dashboard.html` files in `dashboard_dir` before writing (non-dry-run only).
- Writes 17 HTML files to `dashboard_dir`.

## Configuration (`config.py`)

```python
REPO_ROOT: Path      # Repository root (cr-bio/)
DASHBOARD_DIR: Path  # Default output directory for dashboards
```

## Downstream Callers

- `scripts/generate_biol1_lab_dashboards.py` — thin CLI orchestrator that calls `render_all_dashboards`.

## Testing

```bash
cd software && uv run pytest tests/ -q --no-cov -k lab_dashboard
```
