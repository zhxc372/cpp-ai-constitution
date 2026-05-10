#!/usr/bin/env python3
"""
Generate README.md and README_CN.md from project.yaml and Jinja2 templates.
Edit project.yaml and templates, not READMEs directly.
"""

import yaml
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.parent
PROJECT_YAML = ROOT / "project.yaml"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_EN = ROOT / "README.md"
OUTPUT_ZH = ROOT / "README_CN.md"

def load_project_data() -> dict:
    """Load project metadata from YAML."""
    try:
        with open(PROJECT_YAML, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load project.yaml: {e}", file=sys.stderr)
        return {}

def generate_readme(template_name: str, output_path: Path, data: dict) -> bool:
    """Generate a single README file from template."""
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)
        template = env.get_template(template_name)
        content = template.render(**data)
        
        # Add warning header
        warning = f"""<!--
AUTOMATICALLY GENERATED FILE - DO NOT EDIT DIRECTLY
Edit {PROJECT_YAML.name} and {TEMPLATES_DIR.name}/{template_name} instead.
Run scripts/build_readme.py to regenerate.
-->
"""
        full_content = warning + content
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return True
    except Exception as e:
        print(f"❌ Failed to generate {output_path}: {e}", file=sys.stderr)
        return False

def main() -> int:
    """Main function."""
    data = load_project_data()
    if not data:
        return 1
    
    # Generate English README
    ok_en = generate_readme("README.md.j2", OUTPUT_EN, data)
    
    # Generate Chinese README
    ok_zh = generate_readme("README_CN.md.j2", OUTPUT_ZH, data)
    
    if ok_en and ok_zh:
        print(f"✅ Generated {OUTPUT_EN.name} and {OUTPUT_ZH.name} successfully")
        return 0
    else:
        print(f"❌ Failed to generate README files", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
