#!/usr/bin/env python3
"""Validate repository structure, frontmatter, configs, and file references."""

import json
import sys
import yaml
import py_compile
from pathlib import Path

ROOT = Path(__file__).parent.parent
errors = []
warnings = []

ADAPTER_HEADER = "<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->"


def add_adapter_header(text: str) -> str:
    """Add adapter header after frontmatter."""
    if ADAPTER_HEADER in text:
        return text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return f"---{parts[1]}---\n{ADAPTER_HEADER}\n{parts[2]}"
    return f"{ADAPTER_HEADER}\n\n{text}"


def check_frontmatter(filepath, label=""):
    """Check YAML frontmatter in a markdown file."""
    try:
        text = filepath.read_text()
        if not text.startswith("---"):
            errors.append(f"[FAIL] {label or filepath}: missing YAML frontmatter")
            return
        parts = text.split("---", 2)
        if len(parts) < 3:
            errors.append(f"[FAIL] {label or filepath}: malformed frontmatter")
            return
        try:
            yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            errors.append(f"[FAIL] {label or filepath}: invalid YAML - {e}")
            return
        print(f"[OK] {label or filepath} frontmatter valid")
    except Exception as e:
        errors.append(f"[FAIL] {label or filepath}: {e}")


def check_json(filepath, label=""):
    """Check valid JSON."""
    try:
        json.loads(filepath.read_text())
        print(f"[OK] {label or filepath} valid JSON")
    except json.JSONDecodeError as e:
        errors.append(f"[FAIL] {label or filepath}: invalid JSON - {e}")


def check_python(filepath, label=""):
    """Check Python syntax."""
    try:
        py_compile.compile(str(filepath), doraise=True)
        print(f"[OK] {label or filepath} compiles")
    except py_compile.PyCompileError as e:
        errors.append(f"[FAIL] {label or filepath}: {e}")


def check_file_exists(path, label=""):
    """Check file exists."""
    full = ROOT / path
    if full.exists():
        print(f"[OK] {label or path} exists")
    else:
        errors.append(f"[FAIL] {label or path}: file not found")


def check_sync_consistency():
    """Check canonical SKILL.md matches platform copies (after adding adapter header)."""
    canonical = ROOT / "SKILL.md"
    if not canonical.exists():
        return

    targets = [
        ROOT / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md",
        ROOT / ".claude" / "skills" / "cpp-core-review" / "SKILL.md",
        ROOT / ".agents" / "skills" / "cpp-core-review" / "SKILL.md",
    ]
    source = add_adapter_header(canonical.read_text())
    for t in targets:
        if not t.exists():
            warnings.append(f"[WARN] {t.relative_to(ROOT)} does not exist")
            continue
        if t.read_text() != source:
            errors.append(f"[FAIL] {t.relative_to(ROOT)} out of sync with SKILL.md")
        else:
            print(f"[OK] {t.relative_to(ROOT)} in sync")


def check_readme_references():
    """Check files mentioned in README actually exist."""
    for readme in ["README.md", "README_CN.md"]:
        path = ROOT / readme
        if not path.exists():
            continue
        text = path.read_text()
        import re
        refs = re.findall(r'`([^`]+\.(?:md|yml|yaml|json|py|sh))`', text)
        for ref in set(refs):
            # Strip common prefixes like --config-file= etc.
            ref = re.sub(r'^[\-\-]+[\w\-]*=', '', ref)
            # Skip globs
            if '*' in ref:
                continue
            # Try as-is, then with common prefixes
            candidates = [ref]
            if not ref.startswith('config/'):
                candidates.append(f'config/{ref}')
            found = any((ROOT / c).exists() for c in candidates)
            if found:
                print(f"[OK] {readme} → {ref} exists")
            else:
                errors.append(f"[FAIL] {readme} → {ref}: file not found")


def main():
    print("=" * 50)
    print("Validating cpp-ai-constitution repository")
    print("=" * 50)

    # 1. SKILL.md frontmatter
    check_frontmatter(ROOT / "SKILL.md", "SKILL.md")

    # 2. OpenCode agents frontmatter
    agents_dir = ROOT / ".opencode" / "agents"
    if agents_dir.exists():
        for f in agents_dir.glob("*.md"):
            check_frontmatter(f, f.relative_to(ROOT))

    # 3. OpenCode skills frontmatter
    for skill_dir in (ROOT / ".opencode" / "skills").glob("*"):
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            check_frontmatter(skill_md, skill_md.relative_to(ROOT))

    # 4. JSON configs
    check_json(ROOT / "opencode.json.example", "opencode.json.example")

    # 5. Python scripts
    scripts_dir = ROOT / "scripts"
    if scripts_dir.exists():
        for f in scripts_dir.glob("*.py"):
            check_python(f, f.relative_to(ROOT))

    # 6. Sync consistency
    check_sync_consistency()

    # 7. README references
    print("\n--- README References ---")
    check_readme_references()

    # 8. Essential files
    print("\n--- Essential Files ---")
    essentials = [
        "AGENTS.md", "CLAUDE.md", "SKILL.md", "GOTCHAS.md",
        "README.md", "README_CN.md",
        "references/rule-map.md",
        "config/.clang-format",
    ]
    for f in essentials:
        check_file_exists(f)

    # 9. Governance files
    print("\n--- Governance Files ---")
    gov_files = [
        "PROJECT_CONSTITUTION.md",
        "DECISION_RIGHTS.md",
        "ADAPTER_POLICY.md",
        "RULE_ADMISSION.md",
        "evals/adapter-consistency.yaml",
    ]
    for f in gov_files:
        check_file_exists(f)

    # 10. Governance references in key files
    print("\n--- Governance References ---")
    gov_refs = {
        "README.md": "PROJECT_CONSTITUTION.md",
        "SKILL.md": "PROJECT_CONSTITUTION.md",
        "AGENTS.md": "PROJECT_CONSTITUTION.md",
    }
    for f, kw in gov_refs.items():
        path = ROOT / f
        if path.exists():
            text = path.read_text()
            if kw in text:
                print(f"[OK] {f} references {kw}")
            else:
                errors.append(f"[FAIL] {f} does not reference {kw}")
        else:
            errors.append(f"[FAIL] {f}: file not found")

    # 11. Adapter header check
    print("\n--- Adapter Headers ---")
    adapter_files = list((ROOT / ".opencode" / "skills").rglob("SKILL.md"))
    adapter_files += list((ROOT / ".opencode" / "agents").rglob("*.md"))
    adapter_files += list((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    adapter_files += list((ROOT / ".agents" / "skills").rglob("SKILL.md"))
    if (ROOT / "CLAUDE.md").exists():
        adapter_files.append(ROOT / "CLAUDE.md")

    header_marker = "Adapter Notice"
    for af in adapter_files:
        text = af.read_text()
        if header_marker in text:
            print(f"[OK] {af.relative_to(ROOT)} has adapter header")
        else:
            errors.append(f"[FAIL] {af.relative_to(ROOT)} missing adapter header")

    # Summary
    print("\n" + "=" * 50)
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for e in errors:
            print(f"  {e}")
    else:
        print("ALL CHECKS PASSED")

    if warnings:
        print(f"\nWarnings: {len(warnings)}")
        for w in warnings:
            print(f"  {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
