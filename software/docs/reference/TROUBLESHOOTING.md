# Troubleshooting Guide

> **Navigation**: [← Reference Home](README.md) | [CLI Reference](CLI_REFERENCE.md) | [Config Reference](CONFIG_REFERENCE.md) | [Glossary](GLOSSARY.md)

Comprehensive troubleshooting guide for the cr-bio software. Each entry covers the symptom, root cause, and solution.

---

## Contents

- [PDF Generation Fails (pangocairo)](#pdf-generation-fails-pangocairo)
- [Audio Generation Fails (say/ffmpeg)](#audio-generation-fails-sayffmpeg)
- [ModuleNotFoundError: No module named 'src'](#modulenotfounderror-no-module-named-src)
- [Wrong Virtual Environment Gotcha](#wrong-virtual-environment-gotcha)
- [WeasyPrint CSS Warnings](#weasyprint-css-warnings)
- [Permission Errors](#permission-errors)
- [Memory Issues with Large Files](#memory-issues-with-large-files)
- [Pipeline Fails Mid-Way](#pipeline-fails-mid-way)
- [Slow Processing](#slow-processing)
- [repo_contracts Validation Failures](#repo_contracts-validation-failures)
- [Git Subtree Push Failures](#git-subtree-push-failures)
- [Module Not Found Errors](#module-not-found-errors)
- [Environment Verification Checklist](#environment-verification-checklist)

---

## PDF Generation Fails (pangocairo)

**Symptom**:
```
OSError: cannot load library 'pangocairo'
```

**Cause**: WeasyPrint requires the Cairo/Pango system libraries to render PDFs. On macOS, these are provided by Homebrew but the library path is not on the default search path.

**Solution**:

```bash
# 1. Install system dependencies
brew install cairo pango gdk-pixbuf glib

# 2. Set the library search path for Homebrew dylibs
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"

# 3. Add to ~/.zshrc for persistence
echo 'export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"' >> ~/.zshrc
source ~/.zshrc

# 4. Verify WeasyPrint can load
uv run python -c "from weasyprint import HTML; print('✓ WeasyPrint: OK')"
```

> **Note**: `publish.py` sets this variable automatically, but if you run scripts directly via `uv run python scripts/...` you must set it yourself. The `run_tests.sh` wrapper also handles this.

---

## Audio Generation Fails (say/ffmpeg)

**Symptom**:
```
# say command not found
say: command not found

# ffmpeg not installed
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

Or: the TTS/ffmpeg command times out or produces no output.

**Cause**: MP3 audio generation depends on the macOS `say` command and `ffmpeg`. Either is missing, or `say` is being run on a non-macOS system.

**Solution**:

```bash
# 1. Check say is available (macOS only)
say --version 2>/dev/null || echo "say not found (macOS only)"

# 2. Install ffmpeg
brew install ffmpeg

# 3. For routine local/publish gates, disable MP3
# In publish.toml:
# [publish.formats]
# mp3 = false
```

**Workarounds**:

- Use `--skip-mp3` with `publish_all.py` to skip audio generation
- Use `--formats pdf,docx,html,txt,md` (omit mp3) to exclude audio from specific runs
- Process smaller batches with `--module X` to limit scope
- The `gTTS` package is available as a fallback for non-macOS systems (requires internet)

---

## ModuleNotFoundError: No module named 'src'

**Symptom**:
```
ModuleNotFoundError: No module named 'src'
```

**Cause**: The script is being run from the wrong directory. The `src/` package is relative to the `software/` directory.

**Solution**:

```bash
# Always run from the software/ directory
cd /path/to/cr-bio/software

# Then run the script
uv run python scripts/generate_all_outputs.py --course biol-1
```

**Verify**:

```bash
# Confirm you're in the right place
pwd  # should end in /software

# Confirm src/ is importable
uv run python -c "from src import __version__; print(f'✓ cr-bio v{__version__}')"
```

---

## Wrong Virtual Environment Gotcha

**Symptom**: Scripts fail with import errors even though you're in the `software/` directory. Or: you installed packages but they aren't found.

**Cause**: You are using a system Python or a different virtual environment instead of the `uv`-managed environment. The `uv` tool creates and manages a virtual environment in `software/.venv/`.

**Solution**:

```bash
# 1. Always use `uv run` to execute scripts
cd software
uv run python scripts/generate_all_outputs.py --course biol-1

# 2. If issues persist, re-sync dependencies
uv sync --extra dev

# 3. Verify the environment
uv run python -c "import sys; print(sys.executable)"
# Should show something like: /path/to/cr-bio/software/.venv/bin/python
```

**Common mistake**:

```bash
# WRONG — uses system Python, not uv-managed
python scripts/generate_all_outputs.py

# WRONG — uses active venv if you activated one manually
python scripts/generate_all_outputs.py

# CORRECT — uses uv-managed environment
uv run python scripts/generate_all_outputs.py
```

---

## WeasyPrint CSS Warnings

**Symptom**:
```
WARNING:weasyprint:Ignored property `some-css-property`
```

**Cause**: WeasyPrint emits warnings for CSS properties it doesn't fully support. These are cosmetic and do not affect output.

**Solution**: These warnings are safe to ignore. Output PDFs are generated correctly. If you want to suppress them in logs:

```bash
# Reduce log level for weasyprint
uv run python -c "
import logging
logging.getLogger('weasyprint').setLevel(logging.ERROR)
from src.markdown_to_pdf.main import render_markdown_to_pdf
render_markdown_to_pdf('input.md', 'output.pdf')
"
```

---

## Permission Errors

**Symptom**:
```
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Cause**: File or directory permissions are incorrect — typically from cloning as a different user, copying from external drives, or Docker volume mounts.

**Solution**:

```bash
# Check file ownership
ls -la /path/to/file

# Fix file permissions
chmod 644 /path/to/file

# Fix directory permissions
chmod 755 /path/to/directory

# For entire output directories
chmod -R u+rw /path/to/cr-bio/course_development/biol-1/course/module-*/output/
```

---

## Memory Issues with Large Files

**Symptom**:
```
# Process killed or out of memory
Killed: 9
```

Or: the process hangs indefinitely during PDF or MP3 generation.

**Cause**: Processing many modules simultaneously, or processing large Markdown files with WeasyPrint/`say`, can exhaust available memory.

**Solution**:

```bash
# 1. Process modules one at a time
uv run python scripts/generate_module_renderings.py --course biol-1 --module 1

# 2. Disable audio generation (most memory-intensive)
# In publish.toml:
# [publish.formats]
# mp3 = false

# Or via CLI:
uv run python scripts/publish_all.py --skip-mp3

# 3. Limit modules processed
uv run python scripts/generate_all_outputs.py --course biol-1 --max-module biol-1:3

# 4. Close other memory-intensive applications
```

---

## Pipeline Fails Mid-Way

**Symptom**: `publish_all.py` or `publish.py` exits with a non-zero code partway through processing. Some outputs were generated; others were not.

**Cause**: An error in one module (missing file, rendering error, etc.) causes the pipeline to abort.

**Solution**:

```bash
# 1. Check the log file for the specific error
ls software/logs/  # find the most recent log
cat software/logs/generation_YYYY-MM-DD_HH-MM-SS.log | tail -50

# 2. Re-run with verbose output to see the error in real-time
uv run python scripts/publish_all.py --clean --verbose

# 3. Skip the failing stage to isolate the issue
uv run python scripts/publish_all.py --skip-generation   # test publish/validate only
uv run python scripts/publish_all.py --skip-publish      # test generation only
uv run python scripts/publish_all.py --skip-validate     # skip validation

# 4. Process just the failing module
uv run python scripts/generate_module_renderings.py --course biol-1 --module 12

# 5. After fixing, re-run the full pipeline
uv run python scripts/publish_all.py --clean --verbose
```

---

## Slow Processing

**Symptom**: The full publish pipeline takes longer than expected.

**Cause**: MP3 audio generation is the bottleneck (~12 min for a full course). PDF generation with WeasyPrint is also computationally intensive.

**Solutions**:

```bash
# 1. Skip MP3 for routine runs (~5 min instead of ~17 min)
uv run python scripts/publish_all.py --clean --skip-mp3

# 2. PDF-only for quick testing
uv run python scripts/publish_all.py --clean --formats pdf

# 3. Limit to a subset of modules
uv run python scripts/generate_all_outputs.py --course biol-1 --max-module biol-1:3

# 4. Skip labs for faster module/syllabus iteration
uv run python scripts/generate_all_outputs.py --course biol-1 --skip-labs

# 5. Use --skip-generation to re-publish existing outputs without regenerating
uv run python scripts/publish_all.py --skip-generation
```

**Typical timing**:

| Run Type | Duration | Formats |
|----------|----------|---------|
| Full publish with MP3 | ~17 min | pdf, docx, html, txt, md, mp3 |
| Full publish without MP3 | ~5 min | pdf, docx |
| PDF-only, single module | ~10 sec | pdf |
| Full publish, skip generation | ~30 sec | (copy/flatten/validate only) |

---

## repo_contracts Validation Failures

**Symptom**:
```bash
uv run python scripts/validate_repo_contracts.py
# Reports: status: FAIL
```

**Cause**: One or more repository invariants are violated.

**Solution**:

```bash
# 1. Run with plain output to see all issues
uv run python scripts/validate_repo_contracts.py

# 2. Or get JSON output for programmatic handling
uv run python scripts/validate_repo_contracts.py --json
```

**Common issues and fixes**:

| Issue | Fix |
|-------|-----|
| Missing `README.md` or `AGENTS.md` under `course_development/` or `software/src/` | Create the missing file using a sibling as template |
| Broken relative Markdown link in docs | Fix the link path |
| `publish.toml` module/lab count mismatch | Update `max_module` / `max_lab` to match source folder count |
| `PUBLISHED/` not tracked by git | `git add PUBLISHED/` — needed for subtree push |
| Production source has mock/test-double imports | Remove the import; production code uses real implementations (Real Methods Policy) |

---

## Git Subtree Push Failures

**Symptom**:
```
✗ Subtree split failed: ...
```
or
```
✗ Push failed: ...
```

**Cause**: Git remotes are not configured, or the subtree split encounters conflicts.

**Solution**:

```bash
# 1. Set up git remotes from publish.toml
python publish.py --setup-git

# 2. Verify remotes are configured
git remote -v

# 3. If subtree split fails, check PUBLISHED/ is tracked
git add PUBLISHED/
git commit -m "Track PUBLISHED/ for subtree publishing"

# 4. Manual subtree push for debugging
git subtree split --prefix=PUBLISHED/biol-1
git push biol-1 <split-sha>:main --force

# 5. Skip git entirely for local-only runs
python publish.py --skip-git
```

---

## Module Not Found Errors

**Symptom**:
```
ERROR: Module 5 not found in biol-1
ERROR: Available modules in biol-1:
  - module-01-exploring-life-science
  - module-02-chemistry-of-life
  ...
```

**Cause**: The module number specified doesn't match any module directory, or the course directory doesn't contain the expected `module-NN-*` folders.

**Solution**:

```bash
# 1. List available modules
ls course_development/biol-1/course/module-*/

# 2. Use the correct module number
uv run python scripts/generate_module_renderings.py --course biol-1 --module 3

# 3. Verify the course directory structure
ls course_development/biol-1/course/
```

---

## Environment Verification Checklist

Run these commands to verify your environment is set up correctly:

```bash
cd /path/to/cr-bio/software

# 1. Python version (should be 3.11+)
python --version

# 2. uv installed
uv --version

# 3. Dependencies synced
uv sync --extra dev

# 4. WeasyPrint working (requires DYLD_FALLBACK_LIBRARY_PATH on macOS)
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
uv run python -c "from weasyprint import HTML; print('✓ WeasyPrint: OK')"

# 5. Format conversion module importable
uv run python -c "from src.format_conversion.main import convert_file; print('✓ Format conversion: OK')"

# 6. Local audio tooling available
say --version 2>/dev/null || true
ffmpeg -version | head -1

# 7. All modules importable
uv run python -c "from src import __version__; print(f'✓ cr-bio v{__version__}')"

# 8. Tests passing (quick check)
uv run pytest tests/ -x -q --tb=no
```

**Expected output**: All checks should show ✓.

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [../QUICKSTART.md](../QUICKSTART.md) | Installation and quick commands (includes troubleshooting section) |
| [CLI_REFERENCE.md](CLI_REFERENCE.md) | Complete CLI reference for all scripts |
| [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) | Configuration reference |
| [../../scripts/README.md](../../scripts/README.md) | Scripts overview and dependencies |
