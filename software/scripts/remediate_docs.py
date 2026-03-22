import os
import sys

def get_dir_context(path):
    """Determine context based on path to generate appropriate content."""
    parts = path.split(os.sep)
    
    context = {
        "title": os.path.basename(path).replace("-", " ").title(),
        "type": "generic",
        "parent": parts[-2] if len(parts) > 1 else "root"
    }
    
    if "software" in parts:
        context["type"] = "software"
        if "src" in parts:
            context["type"] = "software_src"
        elif "tests" in parts:
            context["type"] = "software_test"
    elif "biol-1" in parts or "biol-8" in parts:
        if "module-" in context["title"].lower():
            context["type"] = "module"
        elif "labs" in parts:
            context["type"] = "lab"
        elif "exams" in parts:
            context["type"] = "exam"
        elif "quizzes" in parts:
            context["type"] = "quiz"
        elif "resources" in parts:
            context["type"] = "resource"
            
    return context

def generate_readme(path, context, files_in_dir):
    """Generate README.md content based on context."""
    title = context["title"]
    dir_type = context["type"]
    
    content = f"# {title}\n\n"
    
    if dir_type == "module":
        content += f"## Overview\n\nThis directory contains the curriculum materials for {title}.\n\n"
        content += "## Contents\n\n"
        content += "- `keys-to-success.md`: Learning objectives and study tips.\n"
        content += "- `questions.md`: Study questions with continuous numbering.\n"
    elif dir_type == "software_src":
        content += f"## Overview\n\nThis directory contains the source code for the `{os.path.basename(path)}` module.\n\n"
        content += "## Components\n\n"
        for f in [x for x in files_in_dir if x.endswith(".py") and x != "__init__.py"]:
            content += f"- `{f}`\n"
    elif dir_type == "software_test":
        content += f"## Overview\n\nThis directory contains the test suite for the `{os.path.basename(path)}` module.\n\n"
        content += "> **Note**: All tests follow the 'Real Methods Policy' (no mocks/stubs).\n\n"
    elif dir_type == "lab":
        content += f"## Overview\n\nThis directory contains laboratory materials for {title}.\n\n"
        content += "Refer to the root `course/labs/README.md` for directive syntax.\n\n"
    else:
        content += f"## Overview\n\nThis directory contains resources for {title}.\n\n"
        
    if len(files_in_dir) > 0 and dir_type not in ["module", "software_src", "software_test"]:
        content += "## Contents\n\n"
        for f in sorted([x for x in files_in_dir if not x.startswith(".") and x not in ["README.md", "AGENTS.md"]]):
            content += f"- `{f}`\n"
            
    return content

def generate_agents(path, context):
    """Generate AGENTS.md content based on context."""
    title = context["title"]
    dir_type = context["type"]
    
    content = f"# Technical Documentation: {title}\n\n"
    
    if dir_type == "module":
        content += "## Automation and Pipeline\n\n"
        content += "This module is processed by `software/scripts/generate_all_outputs.py`.\n"
        content += "It is subject to the continuous numbering mandate for study questions.\n\n"
        content += "### Constraints\n\n"
        content += "- Do not include `for_upload` or `slides` directories.\n"
        content += "- Do not prefix filenames with the module number (e.g., use `questions.md`, not `module-01-questions.md`).\n"
    elif "software" in dir_type:
        content += "## Module Boundaries\n\n"
        content += f"**What this module does:**\n- Provides functionality for {title}\n\n"
        content += "## Dependencies\n\n"
        content += "Check inner Python file imports for specific dependencies.\n\n"
        content += "## Interface Contract\n\n"
        content += "See specific Python module docstrings for public API guarantees.\n"
    else:
        content += "## Technical Specifications\n\n"
        content += f"This directory follows the standard `cr-bio` repository structure for `{context['parent']}` items.\n"
        content += "No special processing rules apply beyond the standard automated multi-format export pipeline.\n"
        
    return content

def main():
    repo_root = "."
    skip_dirs = {".git", "__pycache__", "node_modules", "venv", "build", "dist", "assets", "media", "images", "output", "htmlcov", "PUBLISHED"}
    
    generated_count = 0
    
    for root, dirs, files in os.walk(repo_root):
        # filter out skip dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        
        # Don't generate for the root directory itself to be safe
        if root == ".":
            continue
            
        context = get_dir_context(root)
        
        readme_path = os.path.join(root, "README.md")
        agents_path = os.path.join(root, "AGENTS.md")
        
        # Check and create README.md
        if "README.md" not in files:
            content = generate_readme(root, context, files)
            with open(readme_path, "w") as f:
                f.write(content)
            print(f"Created {readme_path}")
            generated_count += 1
            
        # Check and create AGENTS.md
        if "AGENTS.md" not in files:
            content = generate_agents(root, context)
            with open(agents_path, "w") as f:
                f.write(content)
            print(f"Created {agents_path}")
            generated_count += 1
            
    print(f"\nSuccessfully generated {generated_count} documentation files.")

if __name__ == "__main__":
    main()
