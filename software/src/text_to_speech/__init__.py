"""Text-to-speech generation utilities."""

from .main import (
    batch_generate_speech,
    generate_speech,
)

__all__ = [
    "generate_speech",
    "batch_generate_speech",
]
