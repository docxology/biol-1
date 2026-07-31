"""BIOL-1 module → LectureCreate video pipeline.

Generates deterministic, versioned lecture videos from structured
module.toml manifests using LectureCreate as the rendering backend.
"""

from .main import build_module_lecture_yaml, render_module_video

__all__ = ["build_module_lecture_yaml", "render_module_video"]
