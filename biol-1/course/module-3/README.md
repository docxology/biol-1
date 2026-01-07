# Module 3

## Overview

Module 3 course materials for BIOL-1.

## Contents

### Assignments

Assignments for this module are located in the [`assignments/`](assignments/) directory. Assignment files are processed to multiple formats (PDF, MP3, DOCX, HTML, TXT) and organized in the `output/assignments/` directory.

### Course Materials

This module includes:

- **Lecture Content** (`sample_lecture-content.md`): Presentation materials for module topics
- **Lab Protocols** (`sample_lab-protocol.md`): Laboratory instructions and documentation
- **Study Guides** (`sample_study-guide.md`): Student study materials
- **Interactive Questions** (`questions/questions.json`): Interactive questions for engagement and assessment

All course materials are processed to multiple formats for accessibility.

## File Processing

### Source Files

Module materials are provided as Markdown files:

- `sample_lecture-content.md` - Lecture materials
- `sample_lab-protocol.md` - Laboratory protocols
- `sample_study-guide.md` - Study guides
- `assignments/*.md` - Assignment files
- `questions/questions.json` - Interactive questions (multiple choice, free response, true/false, matching)

### Processing Workflow

All markdown files are automatically processed to generate multiple output formats:

1. **PDF**: Printable document format via `markdown_to_pdf` module
2. **MP3**: Audio format via `text_to_speech` module
3. **DOCX**: Microsoft Word format via `format_conversion` module
4. **HTML**: Web format via `format_conversion` module
5. **TXT**: Plain text format via text extraction

### Output Organization

Processed files are organized by curriculum element type in the `output/` directory:

```
output/
├── assignments/        # Processed assignment files
├── lab-protocols/     # Processed lab protocol files
├── lecture-content/   # Processed lecture files
└── study-guides/      # Processed study guide files
```

Each subdirectory contains all format variants (PDF, MP3, DOCX, HTML, TXT) for that curriculum element type.

### Processing Scripts

Module materials are processed using:
- **Script**: `software/scripts/generate_module_renderings.py`
- **Function**: `process_module_by_type()` from `batch_processing` module

Module website with interactive questions is generated using:
- **Script**: `software/scripts/generate_module_website.py`
- **Function**: `process_module_website()` from `batch_processing` module

## File Naming Conventions

### Source Files

- **Assignments**: `module-3-assignment-[number]-[description].md`
  - Example: `module-3-assignment-1-introduction.md`
- **Lab Protocols**: `sample_lab-protocol.md`
- **Lecture Content**: `sample_lecture-content.md`
- **Study Guides**: `sample_study-guide.md`

### Output Files

Output files maintain the base filename with format-specific extensions:
- `[basename].pdf` - PDF format
- `[basename].mp3` - Audio format
- `[basename].docx` - Document format
- `[basename].html` - Web format
- `[basename].txt` - Text format

## Documentation

- **[AGENTS.md](AGENTS.md)**: Technical documentation for module structure, file processing, and workflows
