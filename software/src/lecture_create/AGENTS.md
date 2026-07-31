# Technical Documentation: `src/lecture_create`

## Purpose

Generate LectureCreate-compatible YAML manifests from BIOL-1 structured
module.toml files and invoke LectureCreate via subprocess for deterministic
video rendering.

## Module: `main`

```python
def build_module_lecture_yaml(
    module_dir: Path | str,
    output_dir: Path | str,
    lecturecreate_config_path: Path | str | None = None,
) -> str
```
Build a LectureCreate YAML manifest from a BIOL-1 module manifest.
Returns the YAML string. Each manifest has 10 beats covering title,
objectives, topics, concept map, process model, key terms, lab
connection, retrieval, practice quiz, and synthesis.

```python
def build_combined_lecture_yaml(
    course_dir: Path | str,
    output_dir: Path | str,
    lecturecreate_config_path: Path | str | None = None,
) -> str
```
Build a single LectureCreate YAML with one section per BIOL-1 module
(16 sections for the full course). Reuses `build_module_lecture_yaml`
internally to avoid duplication.

```python
def enrich_narrations_with_llm(module: ModuleContent) -> ModuleContent
```
Enrich narration scripts via an LLM pass that reads full module content
(objectives, terms, topics, contents, quiz data) and generates richer,
more natural narration. Stores results in `module.narration_cache` dict.
Gracefully falls back to template defaults if LLM is unavailable.

```python
def render_module_video(
    yaml_path: Path | str,
    output_dir: Path | str,
    config_path: Path | str | None = None,
    lecturecreate_bin: str | None = None,
    qr: bool = False,
    backend: str = "system",
) -> subprocess.CompletedProcess[str]
```
Invoke LectureCreate to render a YAML manifest to video via subprocess.
- `qr`: Pass `--qr` to lecturecreate for per-slide QR codes.
- `backend`: TTS backend (`system`, `edge`, `silent`, `kokoro`, `clone`, `elevenlabs`).

## Script

`scripts/generate_module_videos.py` — CLI orchestrator with these flags:
- `--module N` / `--all` / `--combined` — scope selection
- `--render` — render video after generating YAML
- `--dry-run` — write YAML only
- `--qr` — add per-slide QR codes
- `--backend {auto,system,edge,...}` — TTS backend (default: auto detects edge)
- `--llm-narration` — enrich narration with LLM pass

## Dependencies

- `src/module_content` — reads module.toml manifests
- LectureCreate (external, invoked via subprocess, requires Python >=3.12)

## Conventions

- YAML generation is pure-cr-bio (runs under Python 3.11)
- Video rendering subprocess invokes lecturecreate in its own venv
- SVG assets are referenced by path; PNG conversion is handled externally
- Voice backend is set via YAML `voice:` field (profile name), NOT the backend type;
  backend name is passed via `--backend` CLI flag
- Image aspect ratio: SVGs are 1200×720 (5:3), converted to 1920×1152 via
  `rsvg-convert -w 1920 --keep-aspect-ratio`
