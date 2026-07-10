# Pipeline Documentation

> **Navigation**: [← Orchestration](../ORCHESTRATION.md) | [README](../README.md) | [Publish Pipeline](PUBLISH_PIPELINE.md) | [Generation Flow](GENERATION_FLOW.md) | [Validation Flow](VALIDATION_FLOW.md) | [Git Subtree](GIT_SUBTREE.md) | [Configuration](CONFIGURATION.md)

## Overview

The cr-bio publish pipeline transforms Markdown source files under `course_development/` into multi-format published artifacts under `PUBLISHED/`, then pushes them to public course repositories via git subtree. The pipeline is driven by [`publish.toml`](../../../publish.toml) and orchestrated by [`publish.py`](../../../publish.py) at the repository root.

The pipeline has **9 stages** executed by `software/scripts/publish_all.py`, followed by two root-level steps (`ALL_FILES/` flattening and git push) handled by `publish.py` itself.

```mermaid
flowchart LR
    CLN["1<br/>Clean Published"] --> CLNS["2<br/>Clean Source Outputs"]
    CLNS --> GEN["3<br/>Generate"]
    GEN --> PUB["4<br/>Publish Course"]
    PUB --> LBD["5<br/>Labs & Dashboards"]
    LBD --> SPT["6<br/>Slides & Practice Tests"]
    SPT --> FLAT["7<br/>Flatten Modules"]
    FLAT --> REO["8<br/>Reorganize Categories"]
    REO --> VAL["9<br/>Validate"]
    VAL --> ALLF["10<br/>ALL_FILES /"]
    ALLF --> GIT["11<br/>Git Commit & Push"]
```

## Document Index

| Document | Description |
|----------|-------------|
| [PUBLISH_PIPELINE.md](PUBLISH_PIPELINE.md) | Detailed 9-stage pipeline: each stage's purpose, script, inputs, outputs, and configuration. CLI flags for `publish.py`. |
| [GENERATION_FLOW.md](GENERATION_FLOW.md) | Internal generation mechanics: module materials, batch fan-out, format conversion, lab manuals, websites, slide decks. |
| [VALIDATION_FLOW.md](VALIDATION_FLOW.md) | Validation architecture: source-tree checks, published-tree checks, repo contracts, strict dashboard invariant. |
| [GIT_SUBTREE.md](GIT_SUBTREE.md) | Git subtree publishing: remote setup, split, force push, `ALL_FILES/` flattening, command sequences. |
| [CONFIGURATION.md](CONFIGURATION.md) | Deep dive into `publish.toml`: every config key, section, and example configurations for common scenarios. |

## Entry Points

| Entry | Responsibility |
|-------|----------------|
| **`python publish.py`** (repo root) | Loads `publish.toml`, builds CLI args, runs `publish_all.py`, then runs `ALL_FILES/` flattening and git commit/push on success. |
| **`software/scripts/publish_all.py`** | Executes Steps 1–9 (clean → generate → filesystem layout → validate). |
| **`software/scripts/generate_all_outputs.py`** | Called by Step 3 to render modules, syllabus, labs, practice tests, exams, slide decks. |
| **`software/scripts/validate_outputs.py`** | Called by Step 9 to verify expected artifacts exist. |

## Quick Reference

```bash
# Full pipeline (recommended)
python publish.py

# Preview without executing
python publish.py --dry-run

# Override formats on command line
python publish.py --override-formats pdf,docx,md

# Skip generation, only run git commit and push
python publish.py --git-only

# Run pipeline but skip git push
python publish.py --skip-git

# Configure git remotes from config and exit
python publish.py --setup-git
```

## Related Documentation

| Document | Description |
|----------|-------------|
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Orchestration patterns, CLI scripts, module dependency graph |
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | System design, module layers, document types |
| [../README.md](../README.md) | Documentation index, configuration reference |
| [../../../publish.toml](../../../publish.toml) | Live pipeline configuration |
