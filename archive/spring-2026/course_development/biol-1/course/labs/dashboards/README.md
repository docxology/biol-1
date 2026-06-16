# Lab dashboards (BIOL-1)

## Role

Standalone **HTML** files opened in a browser beside each numbered lab. They ship with lab materials; there is no separate build step. Content should match the ideas in the corresponding numbered protocol under [`../`](../) (`lab-NN_*.md`).

## Naming

Files follow:

`lab-NN_<slug>-dashboard.html`

Publish validation (`strict_dashboards` in the repo `publish.toml`) expects **one** file per numbered lab for BIOL-1 whose name matches `lab-NN_*-dashboard.html`. The checker uses the **lab number** (`NN`), not the middle slug.

The slug in the dashboard filename may **differ** from the topic string in the markdown basename (for example `lab-04_liquid-chemistry.md` pairs with `lab-04_cells-dashboard.html` on disk). When editing, align **content** with the numbered `.md` lab, not with an old or alternate slug name.

## Authoring

Patterns for tables, reflections, and fillable UI live in [`../../../../../software/docs/DASHBOARD_FORMAT.md`](../../../../../software/docs/DASHBOARD_FORMAT.md) when referenced by this course. Lab markdown directive syntax is described in [`../README.md`](../README.md).

## Files

- `lab-01_measurement-methods-dashboard.html`
- `lab-02_probability-statistics-dashboard.html`
- `lab-03_microscopy-dashboard.html`
- `lab-04_cells-dashboard.html`
- `lab-05_membranes-dashboard.html`
- `lab-06_metabolism-dashboard.html`
- `lab-07_photosynthesis-dashboard.html`
- `lab-08_cellular-respiration-dashboard.html`
- `lab-09_cell-division-mitosis-dashboard.html`
- `lab-10_meiosis-reproduction-dashboard.html`
- `lab-11_mendelian-genetics-dashboard.html`
- `lab-12_gene-expression-dashboard.html`
- `lab-13_gene-regulation-dashboard.html`
- `lab-14_biotechnology-genomics-dashboard.html`
- `lab-15_darwin-evolution-dashboard.html`
- `lab-16_microevolution-dashboard.html`
- `lab-17_exam-03-review-dashboard.html`

## Related

- [AGENTS.md](AGENTS.md) — strict invariant and tooling
- [../AGENTS.md](../AGENTS.md) — full lab index
