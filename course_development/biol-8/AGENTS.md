# BIOL-8 Technical Documentation

## Course Structure

### Directory Organization

```
biol-8/
├── course/           # Public course materials
│   └── module-*/     # Individual course modules
│       ├── assignments/
│       ├── README.md
│       └── AGENTS.md
├── syllabus/         # Course syllabus materials
│   ├── README.md
│   ├── AGENTS.md
│   ├── *.md          # Syllabus markdown files
│   └── output/       # Processed syllabus outputs
├── private/          # Instructor-only materials
│   ├── README.md
│   └── AGENTS.md
└── resources/        # Supplementary resources
    ├── README.md
    └── AGENTS.md
```

### Syllabus Structure

The `syllabus/` directory contains:
- **README.md**: Syllabus overview and available formats
- **AGENTS.md**: Technical documentation for syllabus processing
- **Syllabus markdown files**: Main syllabus content
- **output/**: Processed syllabus files organized by format (pdf, mp3, docx, html, txt)

Syllabus files are processed using `process_syllabus()` from the batch_processing module, generating all export formats for accessibility.

### Module Structure

Each module in `course/` contains:
- **assignments/**: Assignment files for students
- **README.md**: Module overview and contents
- **AGENTS.md**: Module-specific technical documentation
- **Lecture Slides**: Presentation files
- **Lab Protocols and Notes**: Laboratory instructions
- **Study Guides**: Student study materials
- **Quizzes**: Assessment materials

## File Management

### Naming Conventions

- **Assignments**: `module-[N]-assignment-[number]-[description].md`
- **Lectures**: `module-[N]-lecture-[topic].pdf` or `.pptx`
- **Lab Protocols**: `module-[N]-lab-[number]-[topic].md`
- **Study Guides**: `module-[N]-study-guide.md`
- **Quizzes**: `module-[N]-quiz.md`

### File Organization

- All module materials follow consistent naming with module prefix
- Assignments are stored in dedicated `assignments/` subfolder
- Lecture materials use standard presentation formats (PDF, PPTX)
- Lab protocols are in Markdown format for easy editing

## Canvas Integration

### Upload Process

1. Module folders are uploaded to Canvas as complete units
2. Maintain folder structure when uploading
3. Ensure all required materials are present before upload
4. Update Canvas links in module README files

### Material Organization

- Public materials in `course/` are suitable for Canvas upload
- Private materials in `private/` are never uploaded to Canvas
- Module structure mirrors Canvas organization

## Workflow Processes

### Syllabus Processing

1. Create or update syllabus markdown file in `syllabus/` directory
2. Run processing script: `software/scripts/generate_syllabus_renderings.py`
3. Verify outputs in `syllabus/output/` directory organized by format
4. Upload processed syllabus to Canvas in appropriate format

### Module Creation

1. Create new module folder: `course/module-[N]/`
2. Initialize with standard structure:
   - `assignments/` folder
   - `README.md` with module overview
   - `AGENTS.md` with module documentation
3. Add placeholder files for required materials
4. Update course-level README.md with module reference

### Assignment Management

1. Create assignments in `module-[N]/assignments/`
2. Use consistent naming convention
3. Document in module README.md
4. Update assignment index in AGENTS.md

### Material Updates

1. Update materials in appropriate module folder
2. Maintain version control for major revisions
3. Update module README.md when adding new materials
4. Document changes in module AGENTS.md

## Quality Assurance

### Pre-Upload Checklist

- [ ] All required folders present (assignments/)
- [ ] README.md and AGENTS.md files exist
- [ ] File naming conventions followed
- [ ] Module structure matches standard template
- [ ] No private materials in course/ directory

### Validation

- Regular structure validation
- File naming convention compliance
- Documentation completeness checks
- Canvas upload readiness verification
