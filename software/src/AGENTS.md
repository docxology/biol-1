# Source Code Technical Documentation

## Code Structure

### Module Organization

Each module follows a consistent structure:

```
[module_name]/
├── __init__.py          # Module initialization and exports
├── main.py              # Core functionality (or [module_name].py)
├── utils.py             # Utility functions
└── config.py            # Configuration management
```

### Function Signatures

#### Markdown to PDF Module

**File**: `src/markdown_to_pdf/main.py`

```python
def render_markdown_to_pdf(input_path: str, output_path: str, css_content: Optional[str] = None, pdf_options: Optional[Dict[str, Any]] = None) -> None:
    """
    Convert a Markdown file to PDF format.
    
    Args:
        input_path: Path to input Markdown file
        output_path: Path for output PDF file
        css_content: Optional custom CSS content
        pdf_options: Optional PDF options
    """
    pass

def batch_render_markdown(directory: str, output_dir: str) -> List[str]:
    """
    Batch convert all Markdown files in a directory to PDF.
    
    Args:
        directory: Directory containing Markdown files
        output_dir: Output directory for PDF files
    
    Returns:
        List of output file paths
    """
    pass

def configure_pdf_options(template: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Configure PDF rendering options.
    
    Args:
        template: Template name or path
        options: Dictionary of rendering options
    
    Returns:
        Configured options dictionary
    """
    pass
```

#### Text-to-Speech Module

**File**: `src/text_to_speech/main.py`

```python
def generate_speech(text: str, output_path: str, voice: str = "default", lang: Optional[str] = None, slow: bool = False) -> None:
    """
    Generate speech audio from text.
    
    Args:
        text: Text content to convert
        output_path: Path for output audio file
        voice: Voice identifier (default: "default")
        lang: Language code (default: "en")
        slow: Whether to speak slowly (default: False)
    """
    pass

def batch_generate_speech(input_dir: str, output_dir: str) -> List[str]:
    """
    Batch generate speech from text files in a directory.
    
    Args:
        input_dir: Directory containing text files
        output_dir: Output directory for audio files
    
    Returns:
        List of output file paths
    """
    pass

def configure_voice_settings(voice: str, speed: float, pitch: float) -> Dict[str, Any]:
    """
    Configure voice settings for speech generation.
    
    Args:
        voice: Voice identifier
        speed: Speech speed (0.5-2.0)
        pitch: Speech pitch adjustment
    
    Returns:
        Configuration dictionary
    """
    pass
```

#### Format Conversion Module

**File**: `src/format_conversion/main.py`

```python
def convert_file(input_path: str, output_format: str, output_path: str) -> None:
    """
    Convert a file from one format to another.
    
    Args:
        input_path: Path to input file
        output_format: Target format (e.g., "pdf", "docx")
        output_path: Path for output file
    """
    pass

def batch_convert(directory: str, input_format: str, output_format: str) -> List[str]:
    """
    Batch convert files in a directory.
    
    Args:
        directory: Directory containing files to convert
        input_format: Source file format
        output_format: Target file format
    
    Returns:
        List of output file paths
    """
    pass

def get_supported_formats() -> Dict[str, List[str]]:
    """
    Get list of supported file formats.
    
    Returns:
        Dictionary mapping input formats to supported output formats
    """
    pass

def get_conversion_path(input_path: str, output_format: str) -> str:
    """
    Generate output path for file conversion.
    
    Args:
        input_path: Path to input file
        output_format: Target format (without dot)
    
    Returns:
        Output file path with new extension
    """
    pass
```

**File**: `src/format_conversion/utils.py`

```python
def convert_markdown_to_docx(input_path: Path, output_path: Path) -> None:
    """
    Convert Markdown file to DOCX.
    
    Args:
        input_path: Path to input Markdown file
        output_path: Path to output DOCX file
    """
    pass

def convert_pdf_to_text(input_path: Path, output_path: Path) -> None:
    """
    Convert PDF file to text.
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to output text file
    """
    pass

def convert_audio_to_text(input_path: Path, output_path: Path) -> None:
    """
    Convert audio file to text using speech-to-text.
    
    Args:
        input_path: Path to input audio file
        output_path: Path to output text file
    """
    pass
```

#### Module Organization Module

**File**: `src/module_organization/main.py`

```python
def create_module_structure(course_path: str, module_number: int) -> str:
    """
    Create standard module folder structure.
    
    Args:
        course_path: Path to course directory
        module_number: Module number
    
    Returns:
        Path to created module directory
    """
    pass

def create_next_module(course_path: str) -> str:
    """
    Create the next module in sequence for a course.
    
    Args:
        course_path: Path to course directory
    
    Returns:
        Path to created module directory
    """
    pass

def validate_module_structure(module_path: str) -> bool:
    """
    Validate that module structure matches requirements.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        True if structure is valid, False otherwise
    """
    pass

def initialize_module_files(module_path: str, template: str) -> None:
    """
    Initialize module with template files.
    
    Args:
        module_path: Path to module directory
        template: Template identifier or path
    """
    pass

def list_course_modules(course_path: str) -> List[str]:
    """
    List all modules in a course.
    
    Args:
        course_path: Path to course directory
    
    Returns:
        List of module directory paths as strings, sorted by module number
    """
    pass

def get_module_statistics(module_path: str) -> Dict[str, Any]:
    """
    Get statistics about a module.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        Dictionary with module statistics including:
        - module_number: Module number
        - total_files: Total number of files
        - total_directories: Total number of directories
        - assignment_count: Number of assignment files
        - has_readme: Whether README.md exists
        - has_agents: Whether AGENTS.md exists
        - is_valid: Whether module structure is valid
    """
    pass
```

**File**: `src/module_organization/utils.py`

```python
def get_module_number_from_path(module_path: Path) -> int:
    """
    Extract module number from module directory path.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        Module number
    """
    pass

def list_all_modules(course_path: Path) -> List[Path]:
    """
    List all module directories in a course.
    
    Args:
        course_path: Path to course directory
    
    Returns:
        List of module directory paths, sorted by module number
    """
    pass

def get_next_module_number(course_path: Path) -> int:
    """
    Get the next available module number for a course.
    
    Args:
        course_path: Path to course directory
    
    Returns:
        Next available module number (1 if no modules exist)
    """
    pass
```

#### Canvas Integration Module

**File**: `src/canvas_integration/main.py`

```python
def upload_module_to_canvas(module_path: str, course_id: str, api_key: str, domain: str = "canvas.instructure.com") -> Dict[str, Any]:
    """
    Upload module materials to Canvas LMS.
    
    Args:
        module_path: Path to module directory
        course_id: Canvas course ID
        api_key: Canvas API key
    
    Returns:
        Dictionary with upload results
    """
    pass

def validate_upload_readiness(module_path: str) -> List[str]:
    """
    Validate module is ready for Canvas upload.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        List of validation issues (empty if ready)
    """
    pass

def sync_module_structure(module_path: str, canvas_course_id: str, api_key: str, domain: str = "canvas.instructure.com") -> Dict[str, Any]:
    """
    Sync module structure with Canvas course.
    
    Args:
        module_path: Path to module directory
        canvas_course_id: Canvas course ID
    
    Returns:
        Dictionary with sync results
    """
    pass
```

#### File Validation Module

**File**: `src/file_validation/main.py`

```python
def validate_module_files(module_path: str) -> Dict[str, Any]:
    """
    Validate files in a module directory.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        Dictionary with validation results
    """
    pass

def check_naming_conventions(directory: str) -> List[str]:
    """
    Check file naming convention compliance.
    
    Args:
        directory: Directory to check
    
    Returns:
        List of files with naming convention violations
    """
    pass

def verify_required_structure(module_path: str) -> bool:
    """
    Verify module has required folder structure.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        True if structure is complete, False otherwise
    """
    pass

def validate_course_structure(course_path: str) -> Dict[str, Any]:
    """
    Validate entire course structure.
    
    Args:
        course_path: Path to course directory
    
    Returns:
        Dictionary with validation results for all modules
    """
    pass

def get_validation_report(module_path: str) -> Dict[str, Any]:
    """
    Get detailed validation report for a module.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        Dictionary with detailed validation report
    """
    pass

def find_missing_materials(module_path: str) -> Dict[str, Any]:
    """
    Find missing required materials in a module.
    
    Args:
        module_path: Path to module directory
    
    Returns:
        Dictionary with missing materials information
    """
    pass

def check_file_sizes(module_path: str, max_size: int = 50 * 1024 * 1024) -> List[str]:
    """
    Check for files that exceed maximum size.
    
    Args:
        module_path: Path to module directory
        max_size: Maximum file size in bytes
    
    Returns:
        List of files that exceed maximum size
    """
    pass
```

**File**: `src/file_validation/utils.py`

```python
def get_file_type(file_name: str) -> str:
    """
    Determine the type of course material file based on name.
    
    Args:
        file_name: File name to analyze
    
    Returns:
        File type: "assignment", "lecture", "lab", "study_guide", "quiz", or "unknown"
    """
    pass

def extract_module_number_from_filename(file_name: str) -> int:
    """
    Extract module number from a file name.
    
    Args:
        file_name: File name (e.g., "module-1-assignment-1.md")
    
    Returns:
        Module number
    """
    pass

def validate_file_name_structure(file_name: str) -> Dict[str, Any]:
    """
    Validate and analyze file name structure.
    
    Args:
        file_name: File name to validate
    
    Returns:
        Dictionary with validation results:
        - valid: bool indicating if name is valid
        - file_type: Type of file (assignment, lecture, etc.)
        - module_number: Extracted module number (if available)
        - issues: List of validation issues
    """
    pass
```

#### Speech-to-Text Module

**File**: `src/speech_to_text/main.py`

```python
def transcribe_audio(audio_path: str, output_path: str, language: str = "en") -> str:
    """
    Transcribe audio file to text using real speech recognition.
    
    Args:
        audio_path: Path to input audio file
        output_path: Path for output text file
        language: Language code (default: "en")
    
    Returns:
        Transcribed text content
    """
    pass

def batch_transcribe_audio(input_dir: str, output_dir: str) -> List[str]:
    """
    Batch transcribe audio files in a directory.
    
    Args:
        input_dir: Directory containing audio files
        output_dir: Output directory for text files
    
    Returns:
        List of output file paths
    """
    pass

def transcribe_from_markdown(markdown_path: str, output_path: str) -> str:
    """
    Extract text from Markdown and transcribe.
    
    Args:
        markdown_path: Path to Markdown file
        output_path: Path for output text file
    
    Returns:
        Extracted text content
    """
    pass
```

#### Batch Processing Module

**File**: `src/batch_processing/main.py`

```python
def process_module_to_pdf(module_path: str, output_dir: str) -> List[str]:
    """
    Convert all Markdown files in a module to PDF.
    
    Args:
        module_path: Path to module directory
        output_dir: Output directory for PDF files
    
    Returns:
        List of output PDF file paths
    """
    pass

def process_module_to_audio(module_path: str, output_dir: str) -> List[str]:
    """
    Convert all text/Markdown files in a module to audio.
    
    Args:
        module_path: Path to module directory
        output_dir: Output directory for audio files
    
    Returns:
        List of output audio file paths
    """
    pass

def process_module_to_text(module_path: str, output_dir: str) -> List[str]:
    """
    Transcribe all audio files in a module to text.
    
    Args:
        module_path: Path to module directory
        output_dir: Output directory for text files
    
    Returns:
        List of output text file paths
    """
    pass

def generate_module_media(module_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Generate all media formats for a module (PDF, audio, text transcriptions).
    
    Args:
        module_path: Path to module directory
        output_dir: Base output directory for all media
    
    Returns:
        Dictionary with results for each media type:
        - pdf_files: List of generated PDF files
        - audio_files: List of generated audio files
        - text_files: List of generated text transcriptions
        - errors: List of errors encountered
    """
    pass

def process_module_by_type(module_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Process module files by curriculum element type and generate all format renderings.
    
    Args:
        module_path: Path to module directory
        output_dir: Base output directory for all renderings
    
    Returns:
        Dictionary with results:
        - by_type: Dict mapping curriculum type to list of generated files
        - summary: Dict with counts of generated files by format
        - errors: List of errors encountered
    """
    pass

#### HTML Website Generation Module

**File**: `src/html_website/main.py`

```python
def generate_module_website(module_path: str, output_dir: Optional[str] = None, course_name: Optional[str] = None) -> str:
    """
    Generate HTML website for a module.
    
    Args:
        module_path: Path to module directory
        output_dir: Output directory (defaults to module_path/output/website)
        course_name: Course name for display (optional)
    
    Returns:
        Path to generated HTML file
    """
    pass
```

#### Schedule Processing Module

**File**: `src/schedule/main.py`

```python
def parse_schedule_markdown(schedule_path: str) -> Dict[str, Any]:
    """
    Parse schedule markdown file and extract structured data.
    
    Args:
        schedule_path: Path to schedule markdown file
    
    Returns:
        Dictionary with parsed schedule data:
        - entries: List of schedule entry dictionaries
        - sections: Dictionary with additional sections
        - metadata: Dictionary with file metadata
    """
    pass

def process_schedule(schedule_path: str, output_dir: str, formats: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Process schedule file and generate outputs in specified formats.
    
    Args:
        schedule_path: Path to schedule markdown file
        output_dir: Output directory for generated files
        formats: List of output formats (default: all supported formats)
    
    Returns:
        Dictionary with results:
        - outputs: Dictionary mapping format to list of output file paths
        - summary: Dictionary with counts of generated files by format
        - errors: List of errors encountered
    """
    pass

def generate_schedule_outputs(schedule_data: Dict[str, Any], output_dir: Path, base_name: str, formats: List[str]) -> Dict[str, List[str]]:
    """
    Generate schedule outputs in specified formats.
    
    Args:
        schedule_data: Parsed schedule data dictionary
        output_dir: Output directory
        base_name: Base name for output files
        formats: List of output formats to generate
    
    Returns:
        Dictionary mapping format to list of output file paths
    """
    pass

def batch_process_schedules(directory: str, output_dir: str, formats: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Batch process all schedule files in a directory.
    
    Args:
        directory: Directory containing schedule files
        output_dir: Output directory for generated files
        formats: List of output formats (default: all supported formats)
    
    Returns:
        Dictionary with results:
        - processed_files: List of processed schedule file paths
        - outputs: Dictionary mapping format to list of output file paths
        - summary: Dictionary with counts of generated files by format
        - errors: List of errors encountered
    """
    pass
```

## Code Organization Principles

### Modularity
- Each module is self-contained with clear boundaries
- Minimal dependencies between modules
- Shared utilities in common utility modules

### Reusability
- Functions designed for reuse across different contexts
- Configuration-driven behavior where appropriate
- Clear interfaces and abstractions

### Maintainability
- Consistent code structure across modules
- Comprehensive documentation
- Type hints for better IDE support and error detection

### Testing
- Unit tests for each function
- Integration tests for module interactions
- Test coverage targets maintained
