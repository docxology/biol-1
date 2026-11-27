# Offline verification

Use a checkout containing the audited Git commit
`19b2fd0647ba55de77fbbb385eda7a4ba6fe05de`. The inventory reads tree entries
rather than opening file objects. A blobless sparse checkout with the root
documentation and `docs/` is sufficient. Keep teaching and bulk folders in
the Git index. They do not have to be materialized.

From the BIOL-1 checkout, use Git and Python 3 to write the inventory to stdout.

```bash
python3 docs/inventory.py
```

To stage the figure with Matplotlib and verify the manuscript, use a disposable
project checkout and a separate [Template checkout at `87704feae0a4490ef7dad9c931d268e8c30273c2`](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2).
Follow the [Template tool prerequisites](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md)
for Pandoc, pandoc-crossref, XeLaTeX, and BibTeX. Set `biol_checkout` to the
absolute path to a directory named `biol-1`. Run these commands from Template.

```bash
uv sync --locked --no-dev
uv run --no-sync python "$biol_checkout/docs/inventory.py" --stage
mkdir -p projects/working
ln -s "$biol_checkout" projects/working/biol-1
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/biol-1 --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/biol-1
```

In the project checkout, view the evidence in `output/inventory.json`, the PDF
in `output/pdf/biol-1_combined.pdf`, the HTML in `output/web/index.html`, and
the validation report in `output/reports/validation_report.json`. The staged
manuscript and figure are working products. The course and bulk publication
paths remain the original teaching distribution.
