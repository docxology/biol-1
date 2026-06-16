# shared

Cross-cutting utilities used by multiple modules under `software/src/`. Keep this package small and dependency-free so any other module can import from it without creating cycles.

## Public API

```python
from src.shared.file_utils import (
    ensure_output_directory,
    read_markdown_file,
    find_files,
)
from src.shared.runtime import configure_runtime_environment
from src.shared.course_config import (
    active_course_names,
    resolve_course_selection,
)
```

| Function | Purpose |
|---|---|
| `ensure_output_directory(path)` | Create the parent directory of a file path, or the directory itself if `path` has no suffix. |
| `read_markdown_file(path)` | Read a UTF-8 markdown file; raise `FileNotFoundError` with a clear message if missing. |
| `find_files(directory, patterns)` | Recursive glob across multiple patterns, returned as a sorted `list[Path]`. |
| `configure_runtime_environment()` | Add Homebrew library paths on macOS before importing renderer modules that load WeasyPrint dependencies. |
| `active_course_names(repo_root=None)` | Read `publish.toml` and return enabled active course ids. |
| `resolve_course_selection(course_arg, repo_root=None)` | Resolve `--course` CLI input; raises a clear error for archived/inactive courses. |

See `AGENTS.md` for signatures and downstream callers.
