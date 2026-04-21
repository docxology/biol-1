# Technical Documentation: `scripts/`

Repo-level maintenance scripts. Distinct from `software/scripts/` (which contains the publish pipeline) — these utilities perform repo-wide bookkeeping.

## Files

### `remediate_docs.py`

Walks the repository and creates a placeholder `README.md` and/or `AGENTS.md` in any directory that is missing one.

**Functions**

- `get_dir_context(path: str) -> dict` — classify a directory by its path. Returns `{"title", "type", "parent"}` where `type` is one of `module`, `software`, `software_src`, `software_test`, `lab`, `exam`, `quiz`, `resource`, or `generic`.
- `generate_readme(path: str, context: dict, files_in_dir: list[str]) -> str` — render a README body appropriate to the directory's type, listing relevant child files.
- `generate_agents(path: str, context: dict) -> str` — render an AGENTS body. For module dirs it emits the continuous-numbering and naming constraints; for software dirs it emits placeholder boundary/dependency sections.
- `main()` — walk the repo (skipping `.git`, `__pycache__`, `node_modules`, `venv`, `build`, `dist`, `assets`, `media`, `images`, `output`, `htmlcov`, `PUBLISHED`, hidden dirs) and write any missing files.

**Behavior**

- Idempotent: only writes if a file does not already exist.
- Skips the repo root (`.`).
- Prints each created file path and a summary count.

**When to run**

After adding many new directories at once (e.g. when bulk-importing modules) to backfill placeholder docs. Generated stubs are intentionally minimal — replace them with real content as the directory matures.

## Conventions

- Repo-level scripts live here. Pipeline scripts (anything that touches `course_development/` or `PUBLISHED/`) live in `software/scripts/`.
- Use plain `python3` for top-level scripts; `software/scripts/` uses `uv run`.
