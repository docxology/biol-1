# LectureCreate Integration

Generates LectureCreate-compatible YAML manifests from BIOL-1 structured module.toml files and invokes LectureCreate to render deterministic, versioned lecture videos.

## Design

cr-bio → module.toml → YAML manifest → LectureCreate → MP4 video

Each BIOL-1 module produces one lecture video (10 beats) with:
- Title card
- Learning objectives
- Topic sequence
- Concept map (SVG → PNG)
- Process model (SVG → PNG)
- Key terms recap
- Lab connection
- Retrieval card (SVG → PNG)
- Practice quiz bridge
- Synthesis / exit ticket

## Dependencies

Requires LectureCreate (`>=0.5.0`) installed in a separate Python >=3.12 environment.
cr-bio invokes it via subprocess so the Python version mismatch (3.11 vs 3.12) is not a problem.

## Usage

```bash
cd software

# Generate YAML for a single module
uv run python scripts/generate_module_videos.py --module 1

# Generate YAML for all 16 modules (dry-run)
uv run python scripts/generate_module_videos.py --all --dry-run

# Generate and render all 16 modules with system TTS
export LECTURECREATE_BIN="/path/to/lecturecreate/.venv/bin/lecturecreate"
uv run python scripts/generate_module_videos.py --all --render

# Use edge-tts for neural-quality voice (auto-detected when available)
uv run python scripts/generate_module_videos.py --all --render --backend edge

# Add per-slide QR codes
uv run python scripts/generate_module_videos.py --module 1 --render --qr

# Generate a combined full-course lecture (16 sections)
uv run python scripts/generate_module_videos.py --combined --render

# Validate generated lectures
uv run python scripts/validate_outputs.py --course biol-1 --validate-lectures

# Regenerate and copy to Downloads
rm -rf ../output/lectures/module-*
uv run python scripts/generate_module_videos.py --all --render
```
