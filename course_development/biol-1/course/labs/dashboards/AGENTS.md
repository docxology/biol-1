# Technical documentation: BIOL-1 `labs/dashboards/`

## Role

One **standalone HTML** file per numbered lab, named `lab-NN_description-dashboard.html`, shipped alongside the lab PDF. Open in a browser. Files are generated from the active BIOL-1 lab list by `software/scripts/generate_biol1_lab_dashboards.py`; edit that generator rather than hand-editing generated dashboard HTML. Content should align with the matching `../lab-NN_*.md`; exam-review worksheets live under `../../review_materials/` and do not have primary numbered dashboards.

## Invariant

With `strict_dashboards` in publish/validation, each numbered lab markdown file must have exactly one dashboard whose stem matches the lab markdown stem plus `-dashboard`. Example: `lab-04_liquid-chemistry.md` pairs with `lab-04_liquid-chemistry-dashboard.html`. See [dashboards/README.md](README.md) for the file list.

## Related

- [../AGENTS.md](../AGENTS.md) — full lab index and `lab_manual` usage
- [../../../../../software/docs/DASHBOARD_FORMAT.md](../../../../../software/docs/DASHBOARD_FORMAT.md) — shared authoring patterns (if referenced by BIOL-1)
