# Documentation Standards and Processes

> **Navigation**: [← README](README.md) | [Architecture](ARCHITECTURE.md) | [Orchestration](ORCHESTRATION.md) | [Quick Start](QUICKSTART.md)

This document defines documentation standards for the cr-bio software project.

---

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
| [ORCHESTRATION.md](ORCHESTRATION.md) | Multi-module workflows | Developers |
| [QUICKSTART.md](QUICKSTART.md) | Installation, quick commands | New users |

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
| [README.md](README.md) | Documentation overview |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Workflow patterns |
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide |
| [../AGENTS.md](../AGENTS.md) | API reference |

---

## Version History

| Date | Changes |
|------|---------|
| 2026-01-15 | Removed unverified statistics, focused on documentation standards |
| 2026-01-09 | Complete rewrite with comprehensive standards |
| 2026-01-08 | Added navigation headers |
| 2026-01-01 | Initial documentation standards |
