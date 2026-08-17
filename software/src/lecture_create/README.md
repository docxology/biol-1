# LectureCreate Integration

Generates LectureCreate-compatible YAML manifests from BIOL-1 structured module.toml files and invokes LectureCreate to render deterministic, versioned lecture videos.

## Design

cr-bio → module.toml → YAML manifest → LectureCreate → MP4 video

Each BIOL-1 module produces one lecture video with a complete, paginated beat
sequence. Key terms are split across recap cards so long definitions remain
readable. The canonical render target is approximately 4–5 minutes per module
at 1920×1080
with DejaVu Sans, using `src/lecture_create/biol-1.yaml`. The sequence includes:
- Title card
- Learning objectives
- Topic sequence
- Concept map (SVG → PNG)
- Process model (SVG → PNG)
- Apply the idea (module-specific claim/evidence example)
- Key terms recap (all terms, paginated at three definitions per card)
- Lab connection
- Retrieval card (SVG → PNG)
- Practice quiz bridge
- Study move (actionable study sequence and exit question)
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
uv run python scripts/generate_module_videos.py --all --render \
  --config src/lecture_create/biol-1.yaml

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
