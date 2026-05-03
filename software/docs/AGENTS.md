# Documentation Standards and Processes

> **Navigation**: [← README](README.md) | [Architecture](ARCHITECTURE.md) | [Orchestration](ORCHESTRATION.md) | [Quick Start](QUICKSTART.md) | [API Reference](../AGENTS.md)

This document defines documentation standards for the cr-bio software project and provides output format reference.

## Contents

- [Documentation map](#documentation-map)
- [Required elements](#required-elements)
- [Formatting standards](#formatting-standards)
- [Output format reference](#output-format-reference)
- [Software module reference](#software-module-reference)
- [Lab directive syntax reference](#lab-directive-syntax-reference)
- [Related Documentation](#related-documentation)

## Project Statistics

Statistics are maintained in [README.md](README.md). This document focuses on documentation standards and processes.

---

## Documentation Map

### Root Level (`software/`)

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](../README.md) | Project overview, installation | All users |
| [AGENTS.md](../AGENTS.md) | Technical API reference | Developers |

### Documentation Directory (`software/docs/`)

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Documentation index | All users |
| [AGENTS.md](AGENTS.md) | Documentation standards (this file) | Contributors |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, diagrams | Developers |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Publish pipeline (**canonical** stage list), workflows | Developers |
| [QUICKSTART.md](QUICKSTART.md) | Installation, quick commands | New users |
| [LAB_FORMAT.md](LAB_FORMAT.md) | Lab protocol authoring | Authors |
| [DASHBOARD_FORMAT.md](DASHBOARD_FORMAT.md) | Lab dashboard HTML | Authors |
| [COURSE_STRUCTURE.md](COURSE_STRUCTURE.md) | `course_development/` layout | All |
| [OUTPUT_PDF.md](OUTPUT_PDF.md) | PDF / WeasyPrint | Developers |
| [OUTPUT_DOCX.md](OUTPUT_DOCX.md) | DOCX | Developers |
| [OUTPUT_HTML.md](OUTPUT_HTML.md) | HTML types + normalized MD study-guide copies (see guide) | Developers |
| [OUTPUT_AUDIO.md](OUTPUT_AUDIO.md) | MP3 / gTTS | Developers |

Root [`publish.toml`](../../publish.toml) remains the authoritative toggle file; prose summaries link here and to [ORCHESTRATION.md](ORCHESTRATION.md#the-publish-pipeline).

### Source Code (`software/src/`)

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](../src/README.md) | Source overview | Developers |
| [AGENTS.md](../src/AGENTS.md) | Module implementation details | Developers |

### Test Suite (`software/tests/`)

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](../tests/README.md) | Test suite overview | Contributors |
| [AGENTS.md](../tests/AGENTS.md) | Testing standards | Contributors |

---

## Required Elements

### Every Document Must Include

1. **Navigation Header**: Blockquote with links to related docs

   ```markdown
   > **Navigation**: [← Parent](parent.md) | [Sibling](sibling.md) | [Child →](child.md)
   ```

2. **Purpose Statement**: Brief overview of what the document covers

3. **Table of Contents** (for long docs): Anchor links to major sections

4. **Cross-References**: Links to related documentation

5. **Related Documentation Section**: Table linking to related docs

### API Documentation Must Include

1. **Function Signature**: Complete with type hints
2. **Parameters**: Description of each parameter
3. **Return Value**: Type and description
4. **Exceptions**: List of possible exceptions
5. **Example**: Working code example

---

## Formatting Standards

### Headers

```markdown
# Document Title (H1) - Only one per document
## Major Section (H2)
### Subsection (H3)
#### Detail Section (H4)
```

### Code Blocks

Always specify language for syntax highlighting:

````markdown
```python
from src.module.main import function
result = function(arg1, arg2)
```
````

### Tables

Use tables for structured data:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

### Links

- **Internal links**: Use relative paths

  ```markdown
  [Quick Start](QUICKSTART.md)
  [../AGENTS.md](../AGENTS.md)
  ```

- **Anchored links**: Use fragment identifiers

  ```markdown
  [Section](#section-name)
  ```

### Blockquotes

Use for navigation headers and important notes:

```markdown
> **Navigation**: [Link 1](doc1.md) | [Link 2](doc2.md)

> **Note**: Important information here.
```

### Emoji

Use sparingly for visual hierarchy:

| Emoji | Purpose |
|-------|---------|
| 📊 | Statistics/data |
| 📚 | Documentation/index |
| 🔧 | Configuration/technical |
| ⚡ | Quick/fast |
| 📦 | Prerequisites/packages |
| 🔗 | Links/references |
| 💡 | Tips/best practices |
| 📖 | Related docs |
| 📋 | Standards/checklists |

---

## Modular Documentation Standards

Every module's `AGENTS.md` file must document modularity aspects to enable maximum modular functionality.

### Required Sections

Each module `AGENTS.md` must include:

#### 1. Module Boundaries

Clearly define what the module does and does not do:

```markdown
## Module Boundaries

**What this module does:**
- Primary responsibility
- Core functionality
- Scope of operations

**What this module does NOT do:**
- Responsibilities handled by other modules
- Out-of-scope functionality
- Dependencies on other modules for these features
```

#### 2. Dependencies

Explicitly list all dependencies:

```markdown
## Dependencies

### Internal Dependencies (Other Modules)
- `module_name`: Purpose of dependency
- `another_module`: Purpose of dependency

### External Dependencies (Libraries)
- `library_name`: Purpose and version requirements

### System Dependencies
- System tools or libraries required
```

#### 3. Independent Usage

Document whether and how the module can be used standalone:

```markdown
## Independent Usage

**Can be used standalone**: Yes/No

**Standalone Example:**
```python
from src.module_name.main import primary_function
result = primary_function(arg1, arg2)
```

**Requirements for standalone use:**

- List any prerequisites
- External dependencies needed
- System requirements

```

#### 4. Integration Points

Document how other modules use this one:

```markdown
## Integration Points

**Used by:**
- `module_name`: How it uses this module
- `another_module`: How it uses this module

**Integration Pattern:**
- Sequential, parallel, or conditional composition
- Interface contract
```

#### 5. Interface Contract

Document the public API guarantees:

```markdown
## Interface Contract

**Public API:**
- Function signatures
- Return value guarantees
- Error handling behavior

**Side Effects:**
- File operations
- External API calls
- State changes

**Thread Safety:**
- Safe for concurrent use (if applicable)
```

### Documentation Checklist

When documenting a module, ensure:

- [ ] Module boundaries are clearly defined
- [ ] All dependencies are explicitly listed
- [ ] Independent usage is documented with examples
- [ ] Integration points with other modules are documented
- [ ] Interface contract is specified
- [ ] Public vs internal functions are clearly distinguished

---

## Module Documentation Format

### API Reference Format

```python
def function_name(
    arg1: str,
    arg2: Optional[int] = None,
    *,
    keyword_only: bool = False
) -> Dict[str, Any]:
    """Brief one-line description.

    Longer description if needed, explaining purpose,
    behavior, and important details.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2, defaults to None
        keyword_only: Description of keyword-only arg

    Returns:
        Dictionary containing:
        - key1: Description
        - key2: Description

    Raises:
        ValueError: When arg1 is invalid
        FileNotFoundError: When path doesn't exist

    Example:
        >>> result = function_name("input", arg2=42)
        >>> print(result["key1"])
    """
```

### Module Table Format

| Module | Key Function | Description | Standalone | Dependencies |
|--------|--------------|-------------|------------|--------------|
| module_name | `primary_function()` | Brief description | Yes/No | List dependencies |

---

## Quality Standards

### Accuracy

- [ ] All code examples are tested and working
- [ ] Function signatures match actual implementation
- [ ] Statistics are verified before inclusion
- [ ] Links are valid and not broken

### Completeness

- [ ] All public functions are documented
- [ ] All parameters are described
- [ ] Error conditions are documented
- [ ] Examples cover common use cases

### Clarity

- [ ] Language is simple and direct
- [ ] Technical terms are explained
- [ ] Complex concepts have examples
- [ ] Navigation is clear

### Consistency

- [ ] Header style is uniform
- [ ] Code block languages are specified
- [ ] Table formatting is consistent
- [ ] Link style is consistent

---

## Maintenance Process

### When Code Changes

1. Update affected API documentation in `AGENTS.md`
2. Update examples if signatures change
3. Verify and update statistics in `README.md` if changed
4. Review cross-references for accuracy

### Periodic Review

1. Verify all links still work
2. Measure and update statistics if changed
3. Check for outdated information
4. Review for clarity improvements

### Before Release

1. Full documentation review
2. All examples tested
3. Statistics verified and updated
4. Version history updated

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Documentation overview (includes course parity matrix) |
| [COURSE_STRUCTURE.md](COURSE_STRUCTURE.md) | Course directory layout and assessment scaffolding |
| [OUTPUT_PDF.md](OUTPUT_PDF.md) | PDF / WeasyPrint output |
| [OUTPUT_DOCX.md](OUTPUT_DOCX.md) | Word output |
| [OUTPUT_HTML.md](OUTPUT_HTML.md) | Study-guide HTML, sites, labs, dashboards, normalized MD copies |
| [OUTPUT_AUDIO.md](OUTPUT_AUDIO.md) | MP3 / gTTS output |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Workflow patterns, publish pipeline |
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide |
| [../AGENTS.md](../AGENTS.md) | API reference |
| [../scripts/README.md](../scripts/README.md) | CLI scripts documentation |
| [../tests/README.md](../tests/README.md) | Test suite documentation |

---

## Testing Standards

See [../tests/AGENTS.md](../tests/AGENTS.md) for complete testing documentation. Key standards summarized here.

### Test Organization

Tests mirror source code structure in `tests/`:

| Pattern | Example |
|---------|---------|
| Module main | `test_batch_processing_main.py` |
| Module utils | `test_batch_processing_utils.py` |
| Integration | `test_integration.py` |

### Real Methods Policy

**All tests use real implementations - no mocks, stubs, or fakes.**

- Real file operations
- Real library calls (gTTS, WeasyPrint, etc.)
- Real validation logic
- Temporary directories for isolation

### Test Markers

| Marker | Purpose |
|--------|---------|
| `requires_internet` | Tests requiring network (gTTS) |
| `requires_api` | Tests requiring external API |

### Fixtures (conftest.py)

| Fixture | Purpose |
|---------|---------|
| `temp_dir` | Temporary directory for test files |
| `sample_markdown_file` | Sample markdown for testing |
| `sample_module_structure` | Sample module directory |

---

## Documentation Checklist

Use this checklist when creating or updating documentation:

### New Document Checklist

- [ ] Navigation header with links to related docs
- [ ] Purpose statement (what does this document cover?)
- [ ] Appropriate heading hierarchy (single H1, logical H2/H3)
- [ ] Code blocks with language specifiers
- [ ] Working, tested code examples
- [ ] Cross-references to related documentation
- [ ] Tables for structured data where appropriate
- [ ] Related Documentation section at the end

### API Function Documentation

- [ ] Function signature with type hints
- [ ] Parameter descriptions
- [ ] Return value description
- [ ] Exceptions that may be raised
- [ ] Working code example
- [ ] Version info (when added, stability)

### Update Checklist

- [ ] Version history entry added
- [ ] Statistics updated if changed (test counts, coverage)
- [ ] Cross-references still valid
- [ ] Examples still work

---

## Output Format Reference

Detailed specifications for each output format generated by the system. For the input/output matrix, see [ARCHITECTURE.md#document-types](ARCHITECTURE.md#document-types).

### PDF

| Property | Value |
|----------|-------|
| **Generator** | `markdown_to_pdf` module (WeasyPrint) |
| **Extension** | `.pdf` |
| **Dependencies** | `weasyprint`, system libraries (cairo, pango) |
| **Features** | Custom CSS styling, header/footer, page numbers |
| **Known Limitations** | Requires macOS `DYLD_FALLBACK_LIBRARY_PATH` for WeasyPrint |

### DOCX

| Property | Value |
|----------|-------|
| **Generator** | `format_conversion` module (python-docx) |
| **Extension** | `.docx` |
| **Dependencies** | `python-docx` |
| **Features** | Microsoft Word compatible, preserves formatting |

### Markdown (study guides)

| Property | Value |
|----------|-------|
| **Generator** | `format_conversion` |
| **Extension** | `.md` |
| **Purpose** | Normalized Markdown copies beside other study-guide outputs |
| **Toggle** | `[publish.formats].md` in root [`publish.toml`](../../publish.toml) |
| **Details** | [OUTPUT_HTML.md#normalized-markdown-study-guides-not-html](OUTPUT_HTML.md#normalized-markdown-study-guides-not-html) |

### HTML

| Property | Value |
|----------|-------|
| **Generator** | `format_conversion` module (markdown2) |
| **Extension** | `.html` |
| **Dependencies** | `markdown2` |
| **Features** | Clean semantic HTML, CSS styling |

### TXT

| Property | Value |
|----------|-------|
| **Generator** | `format_conversion` module (built-in) |
| **Extension** | `.txt` |
| **Dependencies** | None (pure Python) |
| **Features** | Clean plain text, stripped formatting |

### MP3

| Property | Value |
|----------|-------|
| **Generator** | `text_to_speech` module (gTTS) |
| **Extension** | `.mp3` |
| **Dependencies** | `gtts` (requires internet) |
| **Known Limitations** | Rate limiting (~30s per file), requires internet |

### Interactive Website

| Property | Value |
|----------|-------|
| **Generator** | `html_website` module |
| **Extension** | `index.html` (per module directory) |
| **Dependencies** | `batch_processing`, `format_conversion`, `markdown_to_pdf` |
| **Features** | Split-view, dark mode, embedded audio, interactive quizzes |

See [ARCHITECTURE.md#interactive-website](ARCHITECTURE.md#interactive-website) for full feature list.

---

## Software Module Reference

Quick reference for which module handles each task:

| Task | Module | Key Function |
|------|--------|--------------|
| Markdown → PDF | `markdown_to_pdf` | `render_markdown_to_pdf()` |
| Text → Audio | `text_to_speech` | `generate_speech()` |
| Audio → Text | `speech_to_text` | `transcribe_audio()` |
| Any format conversion | `format_conversion` | `convert_file()` |
| Batch processing | `batch_processing` | `process_module_by_type()` |
| Website generation | `html_website` | `generate_module_website()` |
| Lab manual rendering | `lab_manual` | `render_lab_manual()` |
| Schedule processing | `schedule` | `process_schedule()` |
| File validation | `file_validation` | `validate_module_files()` |
| Output validation | `validation` | `validate_outputs()` |
| Module organization | `module_organization` | `create_module_structure()` |
| Publishing | `publish` | `publish_course()` |

See [../AGENTS.md](../AGENTS.md) for complete API documentation with function signatures.

---

## Lab Directive Syntax Reference

Lab protocols use special directives for interactive elements:

| Directive | Rendered As | Example |
|-----------|-------------|---------|
| `{fill:text}` | Single-line input field | Student name: `{fill:text}` |
| `{fill:textarea rows=N}` | Multi-line text area | `{fill:textarea rows=5}` |
| `<!-- lab:data-table rows=N -->` | Fillable data table | `<!-- lab:data-table rows=10 -->` |
| `<!-- lab:reflection prompt="Q" -->` | Reflection box | `<!-- lab:reflection prompt="What did you observe?" -->` |
| `<!-- lab:object-selection -->` | Selection dropdown | `<!-- lab:object-selection -->` |

These directives are processed by the `lab_manual` module. See [ORCHESTRATION.md#lab-manual-generation](ORCHESTRATION.md#lab-manual-generation) for generation commands.

---

## Known Limitations

| Format | Limitation | Workaround |
|--------|-----------|------------|
| **PDF** | WeasyPrint requires system dependencies | [QUICKSTART.md#prerequisites](QUICKSTART.md#-prerequisites) |
| **MP3** | gTTS rate limiting (~30s/file) | Set `mp3 = false` in `publish.toml` for faster runs |
| **DOCX** | Complex Markdown tables may lose structure | Simplify table markup |
| **Website** | Needs prior study-guide/audio passes for embeds | Run full `generate_all_outputs.py` (use `--no-website` to skip sites only, `--skip-labs` to skip lab manuals); see script `--help` |

---

## Version History

| Date | Changes |
|------|---------|
| 2026-02-08 | Added Output Format Reference, Software Module Reference, Lab Directive Syntax (consolidated from root docs) |
| 2026-02-04 | Documentation synchronization (date updates across root files) |
| 2026-02-01 | Added Testing Standards section |
| 2026-01-15 | Removed unverified statistics, focused on documentation standards |
| 2026-01-09 | Complete rewrite with comprehensive standards |
| 2026-01-08 | Added navigation headers |
| 2026-01-01 | Initial documentation standards |
