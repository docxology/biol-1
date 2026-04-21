# shared

Cross-cutting utilities used by multiple modules under `software/src/`. Keep this package small and dependency-free so any other module can import from it without creating cycles.

## Public API

```python
from src.shared.file_utils import (
    ensure_output_directory,
    read_markdown_file,
    find_files,
)
```

| Function | Purpose |
|---|---|
| `ensure_output_directory(path)` | Create the parent directory of a file path, or the directory itself if `path` has no suffix. |
| `read_markdown_file(path)` | Read a UTF-8 markdown file; raise `FileNotFoundError` with a clear message if missing. |
| `find_files(directory, patterns)` | Recursive glob across multiple patterns, returned as a sorted `list[Path]`. |

See `AGENTS.md` for signatures and downstream callers.
