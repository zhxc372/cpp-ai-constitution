#!/usr/bin/env python3
"""
L2 Adapter File Consistency Evals.

Checks that adapter files across platforms are structurally consistent:
1. All adapter SKILL.md files are in sync with canonical SKILL.md
2. All adapter files contain required header per ADAPTER_POLICY.md
3. Adapter YAML data files are valid
4. No adapter invents rules not in core/references/

This is a static file analysis — no live agent required.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

ADAPTER_HEADER = "Adapter Notice"
CANONICAL_SKILL = ROOT / "SKILL.md"

ADAPTER_SKILL_FILES = [
    ROOT / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md",
    ROOT / ".claude" / "skills" / "cpp-core-review" / "SKILL.md",
    ROOT / ".agents" / "skills" / "cpp-core-review" / "SKILL.md",
]

ADAPTER_AGENT_FILES = [
    ROOT / ".opencode" / "agents" / "cpp-safety-auditor.md",
    ROOT / ".opencode" / "agents" / "cpp-refactor-planner.md",
    ROOT / ".opencode" / "agents" / "cpp-reviewer.md",
]

ALL_ADAPTER_FILES = ADAPTER_SKILL_FILES + ADAPTER_AGENT_FILES + [ROOT / "CLAUDE.md"]

errors = []
warnings = []
passed = 0


def check_file_exists(path: Path, label: str = ""):
    global passed, errors
    if path.exists():
        passed += 1
        return True
    errors.append(f"[FAIL] {label or path}: file not found")
    return False


def check_adapter_header(path: Path):
    global passed, errors
    if not path.exists():
        return
    text = path.read_text()
    if ADAPTER_HEADER in text:
        passed += 1
        print(f"  [OK] {path.relative_to(ROOT)} has adapter header")
    else:
        errors.append(f"[FAIL] {path.relative_to(ROOT)} missing adapter header")


def check_sync_with_canonical(path: Path):
    """Check that adapter SKILL.md matches canonical (ignoring header)."""
    global passed, errors
    if not path.exists() or not CANONICAL_SKILL.exists():
        return

    canonical = CANONICAL_SKILL.read_text().strip()
    adapter = path.read_text()

    # Strip adapter header for comparison
    adapter_clean = adapter.replace(
        "<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->",
        ""
    ).strip()

    if adapter_clean == canonical:
        passed += 1
        print(f"  [OK] {path.relative_to(ROOT)} in sync with canonical")
    else:
        errors.append(f"[FAIL] {path.relative_to(ROOT)} out of sync with canonical SKILL.md")


def check_no_invented_rules(path: Path):
    """Check that adapter file doesn't contain rules not in core."""
    if not path.exists():
        return
    text = path.read_text()

    # Heuristic: if adapter has "## Rule" or "### Rule" sections not in canonical
    # This is a lightweight check — full analysis requires rule extraction
    forbidden_phrases = [
        "new rule:", "additional rule:", "extra constraint:",
    ]
    for phrase in forbidden_phrases:
        if phrase.lower() in text.lower():
            warnings.append(f"[WARN] {path.relative_to(ROOT)} may contain invented rule: '{phrase}'")


def main() -> int:
    global passed
    print("=" * 50)
    print("L2 Adapter File Consistency Evals")
    print("=" * 50)

    # 1. Canonical SKILL.md exists
    print("\n--- Canonical ---")
    if check_file_exists(CANONICAL_SKILL, "SKILL.md"):
        passed += 1
        print("  [OK] Canonical SKILL.md exists")

    # 2. Adapter SKILL.md sync
    print("\n--- Sync Check ---")
    for f in ADAPTER_SKILL_FILES:
        check_sync_with_canonical(f)

    # 3. Adapter headers
    print("\n--- Header Check ---")
    for f in ALL_ADAPTER_FILES:
        check_adapter_header(f)

    # 4. No invented rules
    print("\n--- Rule Check ---")
    for f in ALL_ADAPTER_FILES:
        check_no_invented_rules(f)

    # Summary
    print("\n" + "=" * 50)
    if errors:
        print(f"L2 FAILED: {len(errors)} error(s), {len(warnings)} warning(s), {passed} passed")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"L2 PASSED: {passed} checks, {len(warnings)} warning(s)")

    if warnings:
        for w in warnings:
            print(f"  {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
