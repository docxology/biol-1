# Biology at College of the Redwoods (Del Norte, CA)

This is a private repository for Biology courses at College of the Redwoods (Del Norte, CA), organized by Dr. Daniel Ari Friedman ([@docxology](https://github.com/docxology) on GitHub).

## Repository Structure

The repository is organized into three main areas:

1.  **`course_development/`**: The "Back Office" for private curriculum development.
2.  **`PUBLISHED/`**: Public, ready-to-upload course materials.
3.  **`software/`**: Automation tools and documentation.

```mermaid
graph TD
    Root[cr-bio/] --> Dev[course_development/]
    Root --> Pub[PUBLISHED/]
    Root --> Software[software/]
    
    Dev --> Biol1[biol-1/]
    Dev --> Biol8[biol-8/]
    
    Pub --> PubBiol1[biol-1/]
    Pub --> PubBiol8[biol-8/]
    
    Biol1 --> Biol1Source[Source Markdown & Private Files]
    Biol8 --> Biol8Source[Source Markdown & Private Files]
    
    PubBiol1 --> PubBiol1M[Generated Output: PDF, MP3, HTML]
    PubBiol8 --> PubBiol8M[Generated Output: PDF, MP3, HTML]
    
    style Root fill:#e1f5ff
    style Dev fill:#fff9c4
    style Pub fill:#c8e6c9
    style Software fill:#e8f5e9
```

---

## 🏗️ Course Development (`course_development/`)

This is the working directory for instructors. It contains the source of truth for all course content.

### Courses
- **[BIOL-1](course_development/biol-1/)**: Biology 1 at Pelican Bay Prison
- **[BIOL-8](course_development/biol-8/)**: Biology 8 at College of the Redwoods

### Structure
Each course folder contains:
- **`course/`**: Working modules with source Markdown files
- **`syllabus/`**: Syllabus source files
- **`private/`**: Instructor-only materials (Tests, Accommodations)
- **`resources/`**: References, Templates, Media

---

## 📤 Published Outputs (`PUBLISHED/`)

This directory contains the final, generated files ready for upload to Canvas. `software/scripts/publish_course.py` manages the export from `course_development/` to here.

### Structure
- **`biol-1/`**: Contains `module-*/` folders with Slides, Notes, etc.
- **`biol-8/`**: Contains `module-*/` folders with PDF, MP3, HTML, DOCX, etc.

**Note**: Do not edit files here directly. Edit the source in `course_development/` and regenerate.

---

## 🛠️ Software Utilities (`software/`)

The automation engine for the repository.

- **`src/`**: Python modules (markdown_to_pdf, text_to_speech, etc.)
- **`scripts/`**: CLI tools (generate_all_outputs.py, publish_course.py)
- **`docs/`**: [Documentation](software/docs/README.md) for the software system

### Key Scripts
```bash
# Generate outputs for a course
uv run python software/scripts/generate_all_outputs.py --course biol-8

# Publish generated outputs to PUBLISHED/
uv run python software/scripts/publish_course.py --course all
```

See [software/docs/README.md](software/docs/README.md) for comprehensive documentation.
