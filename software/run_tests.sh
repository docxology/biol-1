#!/bin/bash
# Test runner script that sets up environment for WeasyPrint on macOS

# Set library path for WeasyPrint on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
fi

# Run pytest with all arguments passed through
exec uv run pytest "$@"
