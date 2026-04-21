# Repo-level scripts

One-shot maintenance utilities that operate on the repository as a whole, distinct from the publish pipeline (`software/scripts/`).

## Contents

| Script | Purpose |
|---|---|
| `remediate_docs.py` | Sweep the repo and create a placeholder `README.md` and/or `AGENTS.md` in any directory missing them. Generates context-aware stubs (module / software / lab / generic). Writes nothing if both files already exist. |

## Usage

```bash
# Run from the repo root
python3 scripts/remediate_docs.py
```

The script is idempotent and safe to re-run; it only writes files that don't already exist.

## See also

- `software/scripts/` — pipeline scripts (publish, generate, validate).
