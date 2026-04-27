# Technical documentation: BIOL-1 `labs/dashboards/`

## Role

One **standalone HTML** file per numbered lab, named `lab-NN_description-dashboard.html`, shipped alongside the lab PDF. Open in a browser; no build step. Content should align with the matching `../lab-NN_*.md` (or exam-review labs such as `lab-17_exam-03-review`).

## Invariant

With `strict_dashboards` in publish/validation, each numbered lab markdown file must have the expected count of `lab-NN_*-dashboard.html` files (for BIOL-8, lab 15 is an override—see that course; **BIOL-1** is **1** per lab by default). See [dashboards/README.md](README.md) for the file list.

## Related

- [../AGENTS.md](../AGENTS.md) — full lab index and `lab_manual` usage
- [../../../../../software/docs/DASHBOARD_FORMAT.md](../../../../../software/docs/DASHBOARD_FORMAT.md) — shared authoring patterns (if referenced by BIOL-1)
