#!/bin/bash
# Test runner script that sets up environment for WeasyPrint on macOS.
#
# Default mode is the fast, offline gate. Use --full for every test, or
# --audio for local TTS/audio tests.
set -euo pipefail

# Set library path for WeasyPrint on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
fi

mode="fast"
if [[ "${1:-}" == "--fast" || "${1:-}" == "--full" || "${1:-}" == "--audio" ]]; then
  mode="${1#--}"
  shift
fi

case "$mode" in
  fast)
    exec uv run pytest -m "not audio and not slow and not requires_internet and not requires_api" "$@"
    ;;
  full)
    exec uv run pytest "$@"
    ;;
  audio)
    exec uv run pytest -m "audio" "$@"
    ;;
  *)
    echo "Unknown test mode: $mode" >&2
    exit 2
    ;;
esac
