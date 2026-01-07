# Module 1 Technical Documentation

## Module Structure

### Directory Organization

```
module-1/
├── assignments/           # Assignment source files
│   ├── *.md               # Assignment markdown files
│   ├── README.md          # Assignment directory overview
│   └── AGENTS.md          # Assignment technical docs
├── questions/             # Interactive questions
│   ├── questions.json     # Question data in JSON format
│   ├── README.md          # Questions directory overview
│   └── AGENTS.md          # Questions technical docs
├── output/                # Processed output files
│   ├── assignments/       # Processed assignments (PDF, MP3, DOCX, HTML, TXT)
│   ├── lab-protocols/     # Processed lab protocols
│   ├── lecture-content/   # Processed lecture materials
│   ├── study-guides/      # Processed study guides
│   └── website/           # HTML website with interactive features
│       └── index.html     # Enhanced website with resizable components and questions
├── sample_lab-protocol.md # Lab protocol source file
├── sample_lecture-content.md # Lecture content source file
├── sample_study-guide.md  # Study guide source file
├── README.md              # Module overview
└── AGENTS.md              # This file
```

### File Types

- **Assignments**: Markdown files in `assignments/` directory, processed to all formats
- **Lab Protocols**: Markdown files (e.g., `sample_lab-protocol.md`), processed to all formats
- **Lecture Content**: Markdown files (e.g., `sample_lecture-content.md`), processed to all formats
- **Study Guides**: Markdown files (e.g., `sample_study-guide.md`), processed to all formats
- **Questions**: JSON files in `questions/` directory, processed into interactive website elements

## File Processing Workflow

### Processing Function

**Module**: `software/src/batch_processing/main.py`

**Function**: `process_module_by_type(module_path: str, output_dir: str) -> Dict[str, Any]`

### Processing Pipeline

For each markdown file matching curriculum element types:

1. **File Detection**: Files starting with `sample_` are identified
2. **Type Classification**: Files are classified by filename pattern:
   - Contains `"assignment"` → `assignments/` output
   - Contains `"lab-protocol"` → `lab-protocols/` output
   - Contains `"lecture-content"` → `lecture-content/` output
   - Contains `"study-guide"` → `study-guides/` output
3. **Format Generation**: Each file generates:
   - **PDF**: Via `markdown_to_pdf.main.render_markdown_to_pdf()`
   - **MP3**: Via `text_to_speech.main.generate_speech()` (text extracted first)
   - **DOCX**: Via `format_conversion.main.convert_file()` (md->docx)
   - **HTML**: Via `format_conversion.main.convert_file()` (md->html)
   - **TXT**: Via text extraction from markdown
4. **Output Organization**: Files organized in type-specific subdirectories

### Output Structure

```
output/
├── assignments/
│   ├── [basename].pdf
│   ├── [basename].mp3
│   ├── [basename].docx
│   ├── [basename].html
│   └── [basename].txt
├── lab-protocols/
│   └── [same structure]
├── lecture-content/
│   └── [same structure]
└── study-guides/
    └── [same structure]
```

## File Naming Conventions

### Source Files

- **Assignments**: `module-1-assignment-[number]-[description].md`
  - Example: `module-1-assignment-1-introduction.md`
  - Located in `assignments/` subdirectory
- **Lab Protocols**: `sample_lab-protocol.md` (or `module-1-lab-[number]-[topic].md`)
- **Lecture Content**: `sample_lecture-content.md` (or `module-1-lecture-[topic].md`)
- **Study Guides**: `sample_study-guide.md` (or `module-1-study-guide.md`)

### Output Files

- **Base Name**: Derived from source markdown filename (without extension)
- **Extensions**: `.pdf`, `.mp3`, `.docx`, `.html`, `.txt`
- **Location**: Type-specific subdirectory within `output/`

## Processing Scripts

### Module Processing

**Script**: `software/scripts/generate_module_renderings.py`

**Usage**: Processes all sample markdown files in the module

**Output**: All format renderings organized by curriculum element type

### Website Generation

**Script**: `software/scripts/generate_module_website.py`

**Usage**: Generates HTML website with interactive features

**Output**: Enhanced website with:
- Resizable components (horizontal and vertical sliders per section)
- Collapsible sections
- Interactive questions from `questions/questions.json`
- Progress tracking
- State persistence (localStorage)

**Question Types Supported**:
- Multiple choice
- Free response
- True/False
- Matching

## Dependencies

### Software Modules

- **batch_processing**: Main orchestration module
- **markdown_to_pdf**: PDF generation from markdown
- **text_to_speech**: Audio generation from text
- **format_conversion**: Format conversions (DOCX, HTML)

### Utility Functions

- `find_markdown_files()`: Recursively find markdown files
- `should_process_file()`: Filter files to process
- `ensure_output_directory()`: Create output directories
- `extract_text_from_markdown()`: Extract plain text from markdown
- `read_text_file()`: Read file content

## Error Handling

- Individual file processing errors are caught and logged
- Errors are collected in `results["errors"]` list
- Processing continues for remaining files after errors
- Summary includes error count and details

## File Management

### Assignment Organization
- All assignments stored in `assignments/` subdirectory
- Numbered sequentially
- Descriptive names for easy identification
- Processed outputs in `output/assignments/`

### Material Updates
- Maintain version control for major revisions
- Update README.md when adding new materials
- Document file changes in this AGENTS.md
- Re-run processing script after source file updates

## Canvas Upload

### Preparation
- Verify all required files are present
- Check that output formats have been generated
- Ensure folder structure matches Canvas organization
- Validate that no private materials are included

### Upload Process
- Upload entire module folder to Canvas
- Include both source files and output formats
- Maintain folder structure
- Update Canvas links after upload
