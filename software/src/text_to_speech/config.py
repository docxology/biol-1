"""Configuration for text-to-speech generation."""

from typing import Any

# Default voice settings
DEFAULT_VOICE_SETTINGS: dict[str, Any] = {
    "voice": "en",
    "speed": 1.0,
    "pitch": 1.0,
    "lang": "en",
    "slow": False,
}

# Supported languages and voices
SUPPORTED_LANGUAGES: dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
}

# Default output format
OUTPUT_FORMAT: str = "mp3"

# Local command timeout for macOS ``say`` and ffmpeg conversion.
COMMAND_TIMEOUT_SECONDS: int = 30
