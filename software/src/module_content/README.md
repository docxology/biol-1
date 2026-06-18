# module_content

Structured BIOL-1 module content tooling. The package reads each module's `module.toml`, validates the typed contract, and generates student-facing Markdown plus deterministic high-design SVG assets consumed by the publish pipeline.

```bash
cd software
uv run python scripts/generate_module_materials.py --course biol-1
```

## Visualization schema

Each active module must declare exactly three `[[generated_images]]` entries:

- `concept-map` with `central_claim`, `nodes`, `edges`, and optional `clusters`.
- `process-model` with ordered `stages`, `inputs`, `outputs`, `feedbacks`, and optional `constraints`.
- `retrieval-card` with `prompts`, `terms`, and `lab_connection`.

SVG files are local, deterministic, accessible (`role="img"`, `<title>`, `<desc>`), and written under `resources/generated/`. External image generation is not used.

The top-level `python publish.py` flow runs this generation before format conversion.
