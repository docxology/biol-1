# Validation Module Technical Documentation

## Overview

The validation module verifies that course outputs have been generated correctly and published to the expected locations. It produces detailed logs and structured reports for the publish pipeline (see [`scripts/validate_outputs.py`](../../scripts/validate_outputs.py) and [`scripts/publish_all.py`](../../scripts/publish_all.py)).

## Module Structure

```
validation/
├── __init__.py    # Public API surface
├── config.py      # Expected outputs, format mappings, course config
├── utils.py       # File system helpers and lab/study-guide checkers
├── main.py        # Top-level validators and report builder
└── AGENTS.md      # This documentation
```

## Public API (`main.py`)

```python
def validate_outputs(
    course_path: str,
    formats: Optional[List[str]] = None,
    max_module: Optional[int] = None,
    max_lab: Optional[int] = None,
) -> Dict[str, Any]
```

Validate a course's source-tree outputs.

- `course_path`: directory like `course_development/biol-8`.
- `formats`: formats requested by the publish pipeline (e.g. `["pdf", "docx", "md"]`). When provided it is threaded through to module, syllabus, and **lab** checks so the log only reports formats that were actually requested. Defaults to `DEFAULT_REQUIRED_FORMATS` (`pdf`, `docx`).
- `max_module` / `max_lab`: optional caps used during partial test runs.

Returns a dict with `valid`, `formats_validated`, `modules_checked`, `modules_valid`, `modules`, `syllabus_valid`, `labs`, and `issues`.

```python
def validate_published(published_path: str) -> Dict[str, Any]
```

Recursively counts files under `PUBLISHED/<course>/` for each course in `COURSE_CONFIG`. The total it reports is **pre-`ALL_FILES/` flatten** — see [Publish totals scope](#publish-totals-scope).

```python
def generate_validation_report(
    course_name: str,
    repo_root: Optional[str] = None,
    formats: Optional[List[str]] = None,
    max_module: Optional[int] = None,
    max_lab: Optional[int] = None,
) -> Dict[str, Any]
```

Convenience wrapper that calls `validate_outputs` and `validate_published` and returns a combined report (`source_validation`, `published_validation`, `summary`).

```python
def get_output_summary(course_path: str) -> Dict[str, Any]
```

Tallies generated files by extension across all module `output/` directories.

## Helper API (`utils.py`)

```python
def count_files_by_extension(directory: Path) -> Dict[str, int]
def get_module_directories(course_path: Path) -> List[Path]
def check_output_directory(module_path: Path) -> Tuple[bool, Dict[str, bool]]
def check_study_guide_files(module_path: Path, formats: Optional[List[str]] = None) -> Dict[str, bool]
def check_website_files(module_path: Path) -> Dict[str, bool]
def format_file_counts(counts: Dict[str, int]) -> str
def get_timestamp() -> str
def check_lab_files(
    course_path: Path,
    max_lab: Optional[int] = None,
    formats: Optional[List[str]] = None,
) -> Dict[str, Any]
def check_dashboard_invariant(
    course_path: Path,
    course_name: Optional[str] = None,
    max_lab: Optional[int] = None,
) -> Dict[str, Any]
```

`check_lab_files` returns:

| Key | Meaning |
|-----|---------|
| `source_labs` | Total `lab-*.md` files in scope (after `max_lab` filter). |
| `source_labs_numbered` | Files matching `lab-NN_*.md` that are **not** marked as a follow-up. |
| `source_labs_supplemental` | Follow-up pages (e.g. `lab-14_microbiology-followup.md`) and other non-numbered `lab-*.md` files. |
| `formats_checked` | Formats actually tallied (intersection of requested formats with `LAB_RENDERABLE_FORMATS`). |
| `output_files` | `{fmt: count}` for each tallied format, summing flat (`output/<stem>.<fmt>`) and per-format (`output/<fmt>/<stem>.<fmt>`) layouts. |
| `dashboards` | HTML files in `course/labs/dashboards/`. |
| `missing_outputs` | Lab stems with no rendered output in any tallied format. |
| `issues` | Free-form messages (missing `output/` or `dashboards/` directories). |

`max_lab` clips numbered protocols whose number exceeds the cap but **keeps** supplemental files for in-scope numbers (e.g. `lab-14_microbiology-followup.md` stays when `max_lab=14`).

## Format-aware lab counting

Historically the lab checker only counted `pdf` and `html` regardless of what the publish pipeline actually produced, so log lines like `outputs: {'pdf': 19, 'html': 0}` were misleading when the run requested `pdf,docx,md`.

`check_lab_files` now honours the `formats` argument:

- When `formats` is `None`, the legacy behaviour applies (`LAB_OUTPUT_FORMATS = ["pdf", "html"]`).
- When `formats` is supplied (as `validate_outputs` does), it is intersected with `LAB_RENDERABLE_FORMATS = ["pdf", "docx", "html", "md", "txt"]` via `config.get_lab_output_formats`.

`validate_outputs` always threads its `formats` through, so a publish run with `--formats pdf,docx,md` produces a log line like:

```
Labs (source tree): 19 markdown (18 numbered + 1 supplemental); outputs: pdf:19, docx:19, md:19; dashboards: 19
```

## Strict dashboard invariant (opt-in)

`check_dashboard_invariant` enforces, for each numbered protocol
`lab-NN_*.md` in the course's `course/labs/`, that the
`course/labs/dashboards/` directory contains the expected number of
`lab-NN_*-dashboard.html` files. Defaults and overrides come from
`COURSE_CONFIG[course]["dashboards"]` via `get_dashboard_config`:

| Course | default_per_lab | overrides | exempt |
|---|---|---|---|
| `biol-1` | 1 | — | — |
| `biol-8` | 1 | `{15: 2}` (cardiovascular + respiratory) | — |

The check is **opt-in**:

- API: `validate_outputs(..., strict_dashboards=True)` and
  `generate_validation_report(..., strict_dashboards=True)`.
- CLI: `uv run python scripts/validate_outputs.py --course all --strict-dashboards`.
- Pipeline: `python publish.py` honours `[publish.pipeline].strict_dashboards = true`
  in `publish.toml`, which forwards `--strict-dashboards` through `publish_all.py`
  to the validation step.

When enabled, `validate_outputs` adds a `dashboard_invariant` field with
`per_lab` counts and any mismatch issues, and emits a one-line summary
such as `Dashboard invariant (biol-8, strict): ✓ 18 numbered labs checked, 0 issue(s)`.
Mismatches also bubble up into `results["issues"]` and flip
`results["valid"]` to `False`.

Supplemental files (e.g. `lab-14_microbiology-followup.md`) and lab
numbers without any numbered protocol are skipped, so adding a follow-up
page never accidentally triggers a false positive.

## Publish totals scope

Different log lines describe different snapshots of `PUBLISHED/`:

| Line (printer) | Scope |
|---|---|
| `Validation complete (source tree): N/M modules valid` (`main.py`) | Module validity in `course_development/<course>/`. |
| `Labs (source tree): ...` (`main.py`) | Source `course/labs/*.md` and `course/labs/output/*` for one course. |
| `Published Outputs (PUBLISHED/<course>/, recursive, pre-ALL_FILES flatten)` (`scripts/validate_outputs.py`) | Recursive count of `PUBLISHED/<course>/` **before** the `publish.py` wrapper copies everything into `ALL_FILES/`. |
| `PUBLISHED DIRECTORY SUMMARY (pre-ALL_FILES flatten)` (`scripts/validate_outputs.py`) | Sum of the per-course pre-flatten counts. |
| `PUBLISHED/ total files (recursive, includes ALL_FILES/ duplicates)` ([`publish.py`](../../../publish.py)) | Final on-disk count after `ALL_FILES/` has been populated; this is roughly double the validation total because every file is duplicated into `ALL_FILES/`. |

This is why a single run can show both `Total files: 421` (validation) and `Total files in PUBLISHED: 845` (publish summary) without inconsistency.

## Configuration (`config.py`)

| Constant | Purpose |
|---|---|
| `ALL_SUPPORTED_FORMATS` | Every format the validator understands. |
| `DEFAULT_REQUIRED_FORMATS` | Used when no `formats` is supplied (`pdf`, `docx`). |
| `STUDY_GUIDE_BASE_TYPES` | `keys-to-success`, `questions`. |
| `LAB_OUTPUT_FORMATS` | Legacy default for lab output counting (`pdf`, `html`). |
| `LAB_RENDERABLE_FORMATS` | Full set of formats the lab pipeline can produce (`pdf`, `docx`, `html`, `md`, `txt`). |
| `SYLLABUS_REQUIRED_FORMATS` / `SYLLABUS_OPTIONAL_FORMATS` | Per-format expectations for `syllabus/output/`. |
| `EXPECTED_WEBSITE_FILES` | `index.html`. |
| `OUTPUT_DIRS` | Logical → directory-name mapping. |
| `COURSE_CONFIG` | Per-course expected module count (BIOL-1: 16, BIOL-8: 17). |
| `PUBLISHED_DIR_NAME` | `PUBLISHED`. |

Helpers:

- `get_expected_study_guide_files(formats)` → list like `["keys-to-success.pdf", "questions.docx", ...]`.
- `get_syllabus_required_formats(formats)` → renderable subset of requested formats.
- `get_lab_output_formats(formats)` → renderable subset for labs (returns the legacy default when `formats is None`).
- `get_dashboard_config(course_name)` → dict with `default_per_lab` (int), `overrides` (`{int: int}`), and `exempt` (`List[int]`) used by `check_dashboard_invariant`.

## Usage

### Command line

```bash
cd software
uv run python scripts/validate_outputs.py --course all
uv run python scripts/validate_outputs.py --course biol-8 --formats pdf,docx,md
uv run python scripts/validate_outputs.py --course biol-8 --max-lab biol-8:14 --verbose
uv run python scripts/validate_outputs.py --course all --strict-dashboards
```

### Programmatic

```python
from src.validation import validate_outputs, generate_validation_report

results = validate_outputs(
    "../course_development/biol-8",
    formats=["pdf", "docx", "md"],
)
labs = results["labs"]
print(
    f"Labs: {labs['source_labs']} markdown "
    f"({labs['source_labs_numbered']} numbered + "
    f"{labs['source_labs_supplemental']} supplemental); "
    f"outputs: {labs['output_files']}"
)

report = generate_validation_report("biol-8", formats=["pdf", "docx", "md"])
print(report["summary"])
```

## Output Format

### `validate_outputs()` result

```json
{
    "valid": true,
    "course": "biol-8",
    "formats_validated": ["pdf", "docx", "md"],
    "timestamp": "2026-04-21 05:12:14",
    "modules_checked": 17,
    "modules_valid": 17,
    "modules": [...],
    "syllabus_valid": true,
    "labs": {
        "source_labs": 19,
        "source_labs_numbered": 18,
        "source_labs_supplemental": 1,
        "formats_checked": ["pdf", "docx", "md"],
        "output_files": {"pdf": 19, "docx": 19, "md": 19},
        "dashboards": 19,
        "missing_outputs": [],
        "issues": []
    },
    "issues": []
}
```

### `validate_published()` result

```json
{
    "valid": true,
    "path": "/path/to/PUBLISHED",
    "timestamp": "2026-04-21 05:12:14",
    "courses": {
        "biol-1": {"files_by_type": {"pdf": 32, "docx": 32, "md": 32, "html": 16, "...": "..."}, "total_files": 196, "modules": [...]},
        "biol-8": {"files_by_type": {"pdf": 34, "docx": 34, "md": 34, "html": 17, "...": "..."}, "total_files": 225, "modules": [...]}
    },
    "total_files": 421,
    "issues": []
}
```

`total_files` is the **pre-`ALL_FILES/` flatten** count; the post-flatten total appears in `publish.py`'s `PUBLISH COMPLETE` block.
