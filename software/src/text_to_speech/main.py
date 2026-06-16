"""Main functions for text-to-speech generation."""

from pathlib import Path
from typing import List, Optional

from . import config
from .utils import (
    extract_text_from_markdown,
    get_output_path,
    read_text_file,
    text_to_speech_audio,
)
from src.shared.file_utils import ensure_output_directory


def generate_speech(
    text: str,
    output_path: str,
    voice: str = "default",
    lang: Optional[str] = None,
    slow: bool = False,
) -> None:
    """Generate speech audio from text.

    Args:
        text: Text content to convert
        output_path: Path for output audio file
        voice: Voice identifier (default: "default", reserved for future backend selection)
        lang: Language code (default: "en")
        slow: Whether to speak slowly (default: False)

    Raises:
        OSError: If audio generation fails
    """
    output_file = Path(output_path)

    ensure_output_directory(output_file)

    # Use default language if not provided
    if lang is None:
        lang = config.DEFAULT_VOICE_SETTINGS["lang"]

    # Generate speech
    text_to_speech_audio(text, output_file, lang=lang, slow=slow)


def batch_generate_speech(input_dir: str, output_dir: str) -> List[str]:
    """Batch generate speech from text files in a directory.

    Args:
        input_dir: Directory containing text files
        output_dir: Output directory for audio files

    Returns:
        List of output file paths

    Raises:
        ValueError: If directory doesn't exist
        OSError: If audio generation fails for any file
    """
    source_dir = Path(input_dir)
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Directory does not exist: {input_dir}")

    output_directory = Path(output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    output_files = []

    # Find all text and markdown files
    text_files = (
        list(source_dir.glob("*.txt"))
        + list(source_dir.glob("*.md"))
        + list(source_dir.glob("*.markdown"))
    )

    for text_file in text_files:
        try:
            # Read file content
            content = read_text_file(text_file)

            # Extract text from markdown if needed
            if text_file.suffix in [".md", ".markdown"]:
                content = extract_text_from_markdown(content)

            # Generate output path
            output_path = get_output_path(text_file, output_directory)

            # Generate speech
            text_to_speech_audio(content, output_path)

            output_files.append(str(output_path))
        except Exception as e:
            # Log error but continue with other files
            print(f"Error generating speech for {text_file}: {e}")
            continue

    return output_files

