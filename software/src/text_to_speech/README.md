# Text_To_Speech

## Overview

This directory contains the source code for the `text_to_speech` module. The current backend uses macOS `say` to produce AIFF audio and `ffmpeg` to encode MP3 output. Audio generation is intentionally excluded from the default fast test gate.

## Components

- `config.py`
- `utils.py`
- `main.py`
