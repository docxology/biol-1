# Lab dashboards (BIOL-1)

## Role

Standalone **HTML** files opened in a browser beside each numbered lab. They ship with lab materials and are generated from the active BIOL-1 lab list by [`../../../../../software/scripts/generate_biol1_lab_dashboards.py`](../../../../../software/scripts/generate_biol1_lab_dashboards.py). Content should match the ideas in the corresponding numbered protocol under [`../`](../) (`lab-NN_*.md`).

## Naming

Files follow:

`lab-NN_<slug>-dashboard.html`

Publish validation (`strict_dashboards` in the repo `publish.toml`) expects **one** file per numbered lab for BIOL-1 whose basename exactly matches the lab markdown stem:

- `lab-04_liquid-chemistry.md`
- `lab-04_liquid-chemistry-dashboard.html`

Do not reuse an old dashboard slug for a different active lab. If a lab is renamed, regenerate dashboards and rerun `cd software && uv run python scripts/validate_repo_contracts.py`.

## Authoring

Patterns for tables, reflections, and fillable UI live in [`../../../../../software/docs/DASHBOARD_FORMAT.md`](../../../../../software/docs/DASHBOARD_FORMAT.md) when referenced by this course. Lab markdown directive syntax is described in [`../README.md`](../README.md).

## Files

- `lab-01_measurement-methods-dashboard.html`
- `lab-02_probability-statistics-dashboard.html`
- `lab-03_microscopy-dashboard.html`
- `lab-04_liquid-chemistry-dashboard.html`
- `lab-05_viewing-life-dashboard.html`
- `lab-06_exam-review-dashboard.html`
- `lab-07_molecular-genetics-dashboard.html`
- `lab-08_cellular-genetics-dashboard.html`
- `lab-09_inheritance-genetics-dashboard.html`
- `lab-10_epigenetics-dashboard.html`
- `lab-11_genomics-biotechnology-dashboard.html`
- `lab-12_exam-02-review-dashboard.html`
- `lab-13_darwin-evolution-dashboard.html`
- `lab-14_how-populations-evolve-dashboard.html`
- `lab-15_macroevolution-dashboard.html`
- `lab-16_population-systems-ecology-dashboard.html`
- `lab-17_exam-03-review-dashboard.html`

## Related

- [AGENTS.md](AGENTS.md) — strict invariant and tooling
- [../AGENTS.md](../AGENTS.md) — full lab index
