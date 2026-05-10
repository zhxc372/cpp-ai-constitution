#!/usr/bin/env python3
"""Sync canonical skill files to platform-specific directories."""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
CANONICAL = ROOT / "SKILL.md"

TARGETS = [
    ROOT / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md",
    ROOT / ".claude" / "skills" / "cpp-core-review" / "SKILL.md",
    ROOT / ".agents" / "skills" / "cpp-core-review" / "SKILL.md",
]


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


def sync():
    if not CANONICAL.exists():
        print(f"Canonical source not found: {CANONICAL}")
        return 1

    updated = 0
    source_text = add_adapter_header(CANONICAL.read_text())

    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing = target.read_text()
            if existing == source_text:
                print(f"  OK: {target.relative_to(ROOT)}")
                continue

        target.write_text(source_text)
        print(f"  SYNCED: {target.relative_to(ROOT)}")
        updated += 1

    print(f"\n{updated} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync())
