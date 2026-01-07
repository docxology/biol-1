#!/usr/bin/env python3
"""Script to generate HTML website for a module."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.main import process_module_website


def main():
    """Generate HTML website for module-1."""
    # Paths
    module_path = Path(__file__).parent.parent.parent / "biol-1" / "course" / "module-1"

    if not module_path.exists():
        print(f"Error: Module path does not exist: {module_path}")
        return 1

    print(f"Generating website for module: {module_path}")

    try:
        html_file = process_module_website(str(module_path))
        print(f"\n✓ Website generated successfully!")
        print(f"Location: {html_file}")
        print(f"\nOpen in browser: file://{Path(html_file).absolute()}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
