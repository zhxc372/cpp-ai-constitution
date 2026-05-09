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


def sync():
    if not CANONICAL.exists():
        print(f"Canonical source not found: {CANONICAL}")
        return 1

    updated = 0
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing = target.read_text()
            source = CANONICAL.read_text()
            if existing == source:
                print(f"  OK: {target.relative_to(ROOT)}")
                continue

        shutil.copy2(CANONICAL, target)
        print(f"  SYNCED: {target.relative_to(ROOT)}")
        updated += 1

    print(f"\n{updated} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync())
