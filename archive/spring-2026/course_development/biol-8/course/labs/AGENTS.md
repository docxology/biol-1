# Technical documentation: BIOL-8 `labs/`

## Role

Lab protocols: `lab-NN_topic.md` plus per-lab generated outputs under `output/`. **Dashboards** live in `dashboards/` (see [dashboards/README.md](dashboards/README.md)). Lab 15 is special: two dashboard HTML files pair with the single `lab-15_cardiopulmonary-system.md` (cardiovascular + respiratory).

## Pipeline

- PDF/HTML via `lab_manual` (`render_lab_manual` / `batch_render_lab_manuals`); see [labs/README.md](README.md) for the directive vocabulary.
- **Strict dashboard count** (when validation uses `--strict-dashboards`): for each numbered `lab-NN_*.md`, the expected `lab-NN_*-dashboard.html` count comes from [validation config](../../../../software/src/validation/config.py) (BIOL-8 can expect **2** for lab 15).

## Related

- [../AGENTS.md](../AGENTS.md) — file naming and lab count (18 protocol files)
- [dashboards/AGENTS.md](dashboards/AGENTS.md) or [dashboards/README.md](dashboards/README.md) — per-file inventory
