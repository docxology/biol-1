# BIOL-1 Course Materials — Technical Documentation

## Overview

Technical documentation for BIOL-1 course materials organization, processing, and workflow management. This directory contains student-facing course materials organized by module.

## Directory Structure

```
course/
├── README.md                    # Course materials overview (student-facing)
├── AGENTS.md                    # This technical documentation
│
└── module-X/                    # 17 module directories
    ├── for_upload/              # Distribution-ready materials
    ├── output/                  # Generated outputs
    ├── resources/               # Supplementary materials
    └── slides/                  # Presentations
```

## Module Naming Convention

Modules follow the pattern: `module-NN-topic-name/` where NN is the zero-padded module number.

| Number | Directory Name |
|--------|----------------|
| 01 | `module-01-study-of-life` |
| 02 | `module-02-basic-chemistry` |
| 03 | `module-03-organic-molecules` |
| 04 | `module-04-cells` |
| 05 | `module-05-membranes` |
| 06 | `module-06-metabolism` |
| 07 | `module-07-photosynthesis` |
| 08 | `module-08-cellular-respiration` |
| 09 | `module-09-cell-division-mitosis` |
| 10 | `module-10-meiosis-reproduction` |
| 11 | `module-11-mendelian-genetics` |
| 12 | `module-12-gene-expression` |
| 13 | `module-13-gene-regulation` |
| 14 | `module-14-biotechnology-genomics` |
| 15 | `module-15-darwin-evolution` |
| 16 | `module-16-microevolution` |
| 17 | `module-17-speciation-macroevolution` |

## Module Content Specifications

### Resources Directory

Each module's `resources/` directory contains:

| File | Description |
|------|-------------|
| `module-X-comprehension-questions.md` | Study questions for the module |
| `module-X-keys-to-success.md` | Learning objectives and study tips |

### Output Directory

Generated outputs are organized by format:

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Printable documents |
| MP3 | `.mp3` | Audio versions for accessibility |
| DOCX | `.docx` | Editable Word documents |
| HTML | `.html` | Web-viewable versions |
| TXT | `.txt` | Plain text versions |

## File Naming Conventions

### Module Files

- **Resources**: `module-X-[description].md`
  - Example: `module-1-comprehension-questions.md`
  - Example: `module-1-keys-to-success.md`

### Generated Outputs

Output files maintain the source filename with the target extension:

- Source: `module-1-keys-to-success.md`
- Outputs: `module-1-keys-to-success.pdf`, `module-1-keys-to-success.mp3`, etc.

## Workflow Processes

### Content Development

1. Create/edit source Markdown files in module directories
2. Place distribution-ready files in `for_upload/`
3. Generate multi-format outputs using software tools
4. Outputs are saved to `output/` directory

### Output Generation

Use the software tools to generate outputs:

```bash
cd software
uv run python scripts/generate_all_outputs.py --course biol-1
```

### Module Processing

Individual modules can be processed:

```bash
uv run python scripts/generate_module_website.py \
    --module course_development/biol-1/course/module-1
```

## Validation Checklist

Before distribution, verify:

- [ ] All source Markdown files are complete
- [ ] Resources directory contains comprehension questions and keys to success
- [ ] Outputs are generated in all required formats
- [ ] Files in `for_upload/` are current
- [ ] File naming follows conventions

## Integration Points

### Software Dependencies

- **batch_processing**: Multi-format output generation
- **html_website**: Interactive module websites
- **format_conversion**: Format transformations
- **text_to_speech**: Audio generation

### Related Documentation

| Document | Description |
|----------|-------------|
| [../README.md](../README.md) | Course overview |
| [../AGENTS.md](../AGENTS.md) | Course-level technical docs |
| [../../software/AGENTS.md](../../software/AGENTS.md) | Software documentation |

## Quality Assurance

### Content Validation

- All Markdown files checked for proper formatting
- Links validated for accessibility
- File names follow naming conventions

### Output Verification

- PDF files render correctly
- Audio files are audible and complete
- HTML files display properly
