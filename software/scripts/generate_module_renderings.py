#!/usr/bin/env python3
"""Script to generate all renderings for module 1 curriculum files."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processing.main import process_module_by_type


def main():
    """Generate all renderings for module 1."""
    # Paths
    module_path = Path(__file__).parent.parent.parent / "biol-1" / "course" / "module-1"
    output_dir = module_path / "output"

    if not module_path.exists():
        print(f"Error: Module path does not exist: {module_path}")
        return 1

    print(f"Processing module: {module_path}")
    print(f"Output directory: {output_dir}")

    try:
        results = process_module_by_type(str(module_path), str(output_dir))

        # Print summary
        print("\n=== Generation Summary ===")
        print(f"PDF files: {results['summary']['pdf']}")
        print(f"Audio files (MP3): {results['summary']['mp3']}")
        print(f"DOCX files: {results['summary']['docx']}")
        print(f"HTML files: {results['summary']['html']}")
        print(f"TXT files: {results['summary']['txt']}")

        print("\n=== Files by Type ===")
        for file_type, files in results["by_type"].items():
            if files:
                print(f"\n{file_type}/ ({len(files)} files):")
                for file_path in sorted(files):
                    print(f"  - {Path(file_path).name}")

        if results["errors"]:
            print("\n=== Errors ===")
            for error in results["errors"]:
                print(f"  - {error}")
            return 1

        print("\n✓ All renderings generated successfully!")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
