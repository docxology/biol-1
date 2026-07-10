# Testing Strategy

> **Navigation**: [← README](README.md) | [Layers](LAYERS.md) | [Dependency Graph](DEPENDENCY_GRAPH.md) | [../AGENTS.md](../AGENTS.md) | [../../tests/AGENTS.md](../../tests/AGENTS.md)

Architecture and strategy for the cr-bio test suite.

---

## Overview

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Test path** | `tests/` |
| **Test files** | 45+ files mirroring `src/` layout |
| **Coverage** | Reported per-module via `--cov-report=term-missing` |
| **Policy** | Real Methods Policy — no mocks in production code |

---

## Test File Naming Convention

Test files mirror the source package layout:

```
tests/
├── conftest.py                        # Shared fixtures
├── canvas_stub_server.py              # Local HTTP stub for Canvas API
├── test_<package>_main.py             # Public API tests per package
├── test_<package>_utils.py            # Utility function tests
├── test_<package>_orchestration.py    # Orchestration-level tests
├── test_integration.py                # Cross-module integration
├── test_cli.py                        # CLI subprocess tests
├── test_repo_contracts.py             # Repository invariant tests
├── test_edge_cases.py                 # Edge-case coverage (v0.1.3)
└── test_real_implementations.py       # Real library verification
```

---

## Test Categories

### Unit Tests

Test individual functions in isolation. Each test creates its own temp
directory and file fixtures. No shared mutable state.

```python
def test_render_markdown_to_pdf_success(temp_dir):
    """Test basic PDF generation."""
    input_file = temp_dir / "input.md"
    input_file.write_text("# Test\n", encoding="utf-8")
    output_file = temp_dir / "output.pdf"
    render_markdown_to_pdf(str(input_file), str(output_file))
    assert output_file.exists()
```

### Integration Tests

Test interactions between modules — e.g., `batch_processing` calling
`format_conversion` which calls `markdown_to_pdf`.

### CLI Tests

Test scripts as subprocesses to verify argument parsing and exit codes.

```python
def test_help_output():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate_all_outputs.py"), "--help"],
        capture_output=True, text=True, cwd=str(SOFTWARE_DIR),
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
```

### Repo Contract Tests

Validate repository-level invariants: documentation coverage, markdown
link integrity, publish.toml course counts, PUBLISHED/ git tracking,
production code free of test doubles.

---

## Test Markers

| Marker | Purpose | Default |
|--------|---------|---------|
| `@pytest.mark.audio` | Invokes local TTS/ffmpeg | Deselected |
| `@pytest.mark.slow` | Intentionally slow tests | Deselected |
| `@pytest.mark.requires_internet` | Needs network access | Deselected |
| `@pytest.mark.requires_api` | Needs external API key | Deselected |

Default fast gate:

```bash
uv run pytest -q --no-cov -m "not audio and not slow and not requires_internet and not requires_api"
```

---

## Real Methods Policy

Production code uses **real implementations** — no mocks, stubs, or fakes.

- All library calls use real libraries (WeasyPrint, python-docx, etc.)
- All file operations use the real file system
- Test doubles are allowed **only** at:
  - External service boundaries (Canvas API, Google Speech)
  - Expensive orchestration seams (subprocess calls in CLI tests)

The `test_real_implementations.py` suite verifies that real libraries
are importable and functional.

---

## Coverage

Coverage is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = ["--cov=src", "--cov-report=term-missing", "--cov-report=html"]
```

- Per-module coverage reported on every run
- Target: >= 85% total (v0.1.3), >= 90% for v1.0.0
- Check current: `uv run pytest --cov=src --cov-report=term-missing`

---

## conftest.py Fixtures

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `temp_dir` | function | Temporary directory for file operations |
| `sample_markdown_file` | function | Pre-filled `.md` file |
| `sample_text_file` | function | Pre-filled `.txt` file |
| `sample_module_structure` | function | Module dir with README, AGENTS, questions, keys |
| `sample_curriculum_files` | function | Files for each curriculum element type |

---

## Running Tests

```bash
cd software

# Fast offline gate (default)
./run_tests.sh
./run_tests.sh --fast

# Full suite including audio/slow
./run_tests.sh --full

# Specific module
uv run pytest tests/test_markdown_to_pdf_main.py -v

# With coverage report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Collect only (count tests)
uv run pytest --collect-only -q
```

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [../../tests/AGENTS.md](../../tests/AGENTS.md) | Test suite standards |
| [../../tests/README.md](../../tests/README.md) | Test suite overview |
| [../../.cursorrules](../../.cursorrules) | Real Methods Policy |
| [LAYERS.md](LAYERS.md) | Layer architecture |
