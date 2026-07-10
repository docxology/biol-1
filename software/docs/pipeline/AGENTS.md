# Pipeline — Technical Documentation

> **Navigation**: [← README](README.md) | [docs/](../README.md) | [AGENTS.md](../AGENTS.md)

## Purpose

This subfolder documents the cr-bio publish pipeline end-to-end: the
9-stage flow, internal generation mechanics, validation architecture,
git subtree publishing, and publish.toml configuration.

## File Inventory

| File | Topic |
|------|-------|
| [README.md](README.md) | Pipeline index + stage overview |
| [PUBLISH_PIPELINE.md](PUBLISH_PIPELINE.md) | 9-stage pipeline with CLI flags |
| [GENERATION_FLOW.md](GENERATION_FLOW.md) | Internal generation mechanics |
| [VALIDATION_FLOW.md](VALIDATION_FLOW.md) | 4-layer validation architecture |
| [GIT_SUBTREE.md](GIT_SUBTREE.md) | Git subtree push workflow |
| [CONFIGURATION.md](CONFIGURATION.md) | publish.toml deep dive |

## Related Documentation

| Document | Description |
|----------|-------------|
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Composition patterns |
| [../reference/CLI_REFERENCE.md](../reference/CLI_REFERENCE.md) | All script arguments |
| [../../publish.py](../../../publish.py) | Top-level pipeline entry point |
