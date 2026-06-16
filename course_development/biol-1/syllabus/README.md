# BIOL-1 Syllabus

## Overview

This directory contains the course syllabus for BIOL-1 (General Biology at Pelican Bay, Fall 2026). The default publish profile renders PDF, DOCX, and MD copies; HTML, TXT, and MP3 are opt-in formats.

## Syllabus File

- **[BIOL-1_Fall-2026_Syllabus.md](BIOL-1_Fall-2026_Syllabus.md)**: Main syllabus document in Markdown format

## Available Formats

The syllabus is processed to the default local publish formats in the flat `output/` directory:

- **PDF**: `output/BIOL-1_Fall-2026_Syllabus.pdf` - Printable document format
- **DOCX**: `output/BIOL-1_Fall-2026_Syllabus.docx` - Microsoft Word format
- **MD**: `output/BIOL-1_Fall-2026_Syllabus.md` - Normalized Markdown copy

Optional profile outputs:

- **HTML**: `output/BIOL-1_Fall-2026_Syllabus.html` - Web format
- **TXT**: `output/BIOL-1_Fall-2026_Syllabus.txt` - Plain text format
- **MP3**: `output/BIOL-1_Fall-2026_Syllabus.mp3` - Audio format for listening

## Processing

The syllabus is processed using the same automated pipeline as module materials. Use `publish.toml` or `python publish.py --override-formats ...` to request opt-in formats.

## Documentation

- **[AGENTS.md](AGENTS.md)**: Technical documentation for syllabus processing and workflows
