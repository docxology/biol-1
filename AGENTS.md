# Repository Technical Documentation

## Overview

This document provides technical documentation for the Biology courses repository structure, conventions, and automation processes.

## Repository Structure

### Directory Conventions

- **Root Folders**:
  - `course_development/`: "Back Office" for private curriculum work
  - `PUBLISHED/`: Public, ready-to-upload output files
  - `software/`: Automation tools and documentation

### File Organization

#### Course Development (`course_development/`)

- **Structure**: `biol-1/`, `biol-8/`
- **Course folders**: Contains `course/` (source), `syllabus/`, `private/`
- **Source of Truth**: All edits happen here.

#### Published Materials (`PUBLISHED/`)

- **Generated Outputs**: PDF, MP3, HTML, DOCX
- **Organization**: Mirror of course structure, but only final files.

#### Software Structure

- **Source code** (`software/src/`): Modular utilities organized by function
- **Tests** (`software/tests/`): Test files mirroring source structure
- **Documentation** (`software/docs/`): Technical documentation for software modules

## File Naming Conventions

### Course Materials

- **Assignments**:** Descriptive names with module prefix (e.g., `module-1-assignment-1.md`)
- **Lectures**:** Module and topic-based naming (e.g., `module-1-introduction.pdf`)
- **Lab Protocols**:** `lab-protocol-[number]-[topic].md`
- **Study Guides**:** `study-guide-module-[number].md`
- **Quizzes**:** `quiz-module-[number].md`

### Software Files

- **Source files**: Descriptive names matching module purpose
- **Test files**: Mirror source structure with `test_` prefix or `.test.` suffix
- **Documentation**: Markdown files with clear, descriptive names

## Documentation Standards

### README.md Files

- User-facing documentation
- Overview of folder contents
- Navigation links to related folders
- Mermaid diagrams for complex structures
- Clear, accessible language

### AGENTS.md Files

- Technical documentation
- Folder structure specifications
- File naming conventions
- Process documentation
- Automation and workflow details
- Function signatures and APIs (for software folders)

## Automation Processes

### Course Material Management

- **Module organization**: Automated structure creation for new modules
- **Canvas upload**: Scripts for batch uploading module materials
- **File validation**: Checks for required files in each module

### Software Development

- **Build processes**: Automated compilation and packaging
- **Testing**: Automated test execution and reporting
- **Documentation generation**: Automated API documentation from source code

### Content Generation

- **Markdown to PDF**: Automated conversion of course materials
- **Text-to-speech**: Automated generation of audio content from text
- **Format conversion**: Batch processing of file format conversions

## Workflow Processes

### Adding New Modules

1. Create module folder in `course/` directory
2. Initialize with standard structure (assignments/, README.md, AGENTS.md)
3. Add placeholder files for required materials
4. Update course-level README.md with module reference

### Managing Private Materials

1. Store in `private/` directory
2. Ensure proper access controls
3. Document in private/AGENTS.md
4. Never commit sensitive information

### Software Development

1. Follow modular structure in `src/`
2. Write tests in `tests/` mirroring source structure
3. Update documentation in `docs/`
4. Maintain function signatures in AGENTS.md files

## Security and Access

- **Private folder**: Contains sensitive materials (tests, answers, accommodations)
- **Access control**: Private materials not shared publicly or with students
- **Git ignore**: Sensitive files should be in `.gitignore` if appropriate
- **Documentation**: Security practices documented in private/AGENTS.md files

## Maintenance

### Regular Tasks

- Review and update documentation quarterly
- Validate folder structure consistency
- Update module references in course README files
- Maintain software dependencies and versions

### Validation

- Check for required README.md and AGENTS.md at each level
- Verify naming convention compliance
- Validate module structure completeness
- Test automation scripts regularly
