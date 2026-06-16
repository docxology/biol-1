# Text-to-Speech Technical Documentation

## Overview

Text-to-speech generation utilities using local TTS tooling.

## Module Purpose

Generate audio content from text materials, supporting batch processing and Markdown text extraction.

## Function Signatures

### Main Functions

**File**: `src/text_to_speech/main.py`

#### `generate_speech(text: str, output_path: str, voice: str = "default", lang: Optional[str] = None, slow: bool = False) -> None`

Generate speech audio from text.

**Args**:
- `text`: Text content to convert
- `output_path`: Path for output audio file
- `voice`: Voice identifier (default: "default", currently reserved for future backend selection)
- `lang`: Language code (default: "en")
- `slow`: Whether to speak slowly (default: False)

**Raises**:
- `OSError`: If audio generation fails

**Dependencies**:
- macOS `say` command for local speech synthesis
- `ffmpeg` for MP3 encoding

#### `batch_generate_speech(input_dir: str, output_dir: str) -> List[str]`

Batch generate speech from text files in a directory.

**Args**:
- `input_dir`: Directory containing text files
- `output_dir`: Output directory for audio files

**Returns**:
- List of output file paths

**Raises**:
- `ValueError`: If directory doesn't exist
- `OSError`: If audio generation fails for any file

**Processes**:
- Text files (.txt)
- Markdown files (.md, .markdown) - extracts text first

#### `configure_voice_settings(voice: str, speed: float, pitch: float) -> Dict[str, Any]`

Configure voice settings for speech generation.

**Args**:
- `voice`: Voice identifier (currently reserved for future backend selection)
- `speed`: Speech speed (0.5-2.0, currently reserved for future backend selection)
- `pitch`: Speech pitch adjustment (currently reserved for future backend selection)

**Returns**:
- Configuration dictionary

**Note**:
- Parameters are stored for potential future use with configurable TTS backends

### Utility Functions

**File**: `src/text_to_speech/utils.py`

#### `text_to_speech_audio(text: str, output_path: Path, lang: str = "en", slow: bool = False, timeout_seconds: int = 30) -> None`

Generate speech audio from text using local `say` plus `ffmpeg`.

#### `read_text_file(file_path: Path) -> str`

Read text file content.

#### `extract_text_from_markdown(markdown_content: str) -> str`

Extract plain text from Markdown content, removing formatting.

#### `ensure_output_directory(output_path: Path) -> None`

Ensure output directory exists.

#### `get_output_path(input_file: Path, output_dir: Path) -> Path`

Generate output audio path from input text file.

## Configuration

**File**: `src/text_to_speech/config.py`

- `DEFAULT_VOICE_SETTINGS`: Dictionary of default voice settings:
  - `lang`: "en" (language code)
  - `voice`: "default"
  - `speed`: 1.0
  - `pitch`: 1.0

## Integration Points

### Dependencies on Other Modules

- None (standalone module)

### Used By

- **batch_processing**: Batch audio generation for modules
- **format_conversion**: Text to audio conversion
- Test orchestration workflows

### External Dependencies

- **say**: macOS system speech synthesis command
- **ffmpeg**: MP3 encoding
- **pydub**: Audio file handling for adjacent conversion workflows if needed

## Error Handling

- Validates input file existence
- Creates output directories automatically
- Continues batch processing after individual file errors
- Raises bounded `OSError` failures for local command errors or timeouts

## Generation Process

1. Read text content (from string or file)
2. Extract plain text from Markdown if needed
3. Generate AIFF speech using `say`
4. Convert AIFF to MP3 using `ffmpeg`

## Supported Input Formats

- Plain text (.txt)
- Markdown (.md, .markdown) - text is extracted first

## Output Format

- MP3 audio files

## Language Support

Language and voice arguments are accepted for API stability, but the current local backend uses the system voice defaults.
