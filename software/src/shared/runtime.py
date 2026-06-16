"""Runtime environment helpers shared by CLI entrypoints and tests."""

import os
import sys


def configure_runtime_environment() -> None:
    """Configure process-level environment needed by renderer dependencies.

    WeasyPrint loads Cairo/Pango/GObject dynamically. On macOS with Homebrew,
    those shared libraries live under ``/opt/homebrew/lib`` and must be visible
    before importing modules that import WeasyPrint.
    """
    if sys.platform != "darwin":
        return

    homebrew_lib = "/opt/homebrew/lib"
    current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    paths = [p for p in current.split(":") if p]
    if homebrew_lib not in paths:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join([homebrew_lib, *paths])
