"""Tests for text_to_speech main functions."""

from pathlib import Path
import subprocess

import pytest

from src.text_to_speech import utils as tts_utils
from src.text_to_speech.main import (
    batch_generate_speech,
    generate_speech,
)


@pytest.mark.audio
@pytest.mark.slow
def test_generate_speech(temp_dir):
    """Test generating speech from text using the local TTS backend."""
    output_path = temp_dir / "output.mp3"
    text = "Test."

    generate_speech(text, str(output_path))
    assert output_path.exists()
    assert output_path.suffix == ".mp3"


@pytest.mark.audio
@pytest.mark.slow
def test_batch_generate_speech(temp_dir):
    """Test batch generating speech from text files."""
    txt1 = temp_dir / "file1.txt"
    txt2 = temp_dir / "file2.txt"
    txt1.write_text("A.", encoding="utf-8")
    txt2.write_text("B.", encoding="utf-8")

    output_dir = temp_dir / "output"
    output_dir.mkdir()

    output_files = batch_generate_speech(str(temp_dir), str(output_dir))
    assert all(Path(f).exists() for f in output_files)


def test_batch_generate_speech_nonexistent_directory():
    """Test batch generation with nonexistent directory raises error."""
    with pytest.raises(ValueError, match="Directory does not exist"):
        batch_generate_speech("/nonexistent/dir", "/output")


@pytest.mark.audio
@pytest.mark.slow
def test_batch_generate_speech_error_handling(temp_dir):
    """Test error handling in batch_generate_speech with empty file."""
    invalid_file = temp_dir / "invalid.txt"
    invalid_file.write_text("", encoding="utf-8")

    output_dir = temp_dir / "output"
    output_dir.mkdir()

    result = batch_generate_speech(str(temp_dir), str(output_dir))
    assert isinstance(result, list)


@pytest.mark.audio
@pytest.mark.slow
def test_generate_speech_creates_parent_dirs(temp_dir):
    """Test that generate_speech creates missing parent directories."""
    output_path = temp_dir / "nonexistent" / "output.mp3"
    generate_speech("Test.", str(output_path))
    assert output_path.exists()


def test_text_to_speech_audio_timeout_raises_oserror(temp_dir, monkeypatch):
    """Local TTS subprocess timeouts are bounded and surfaced as OSError."""
    output_path = temp_dir / "timeout.mp3"

    def fake_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])

    monkeypatch.setattr(tts_utils.subprocess, "run", fake_run)

    with pytest.raises(OSError, match="timed out"):
        tts_utils.text_to_speech_audio("Test.", output_path, timeout_seconds=1)
