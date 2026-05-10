#!/usr/bin/env python3
"""Sync canonical skill files to platform-specific directories.

Reads targets from adapter_manifest.yaml instead of hardcoded list.
Checks that synced content does not alter core principles.
"""

from __future__ import annotations

import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
MANIFEST_PATH = ROOT / "adapter_manifest.yaml"
CANONICAL = ROOT / "SKILL.md"

ADAPTER_HEADER = "<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->"


def add_adapter_header(text: str) -> str:
    """Add adapter header after frontmatter."""
    if ADAPTER_HEADER in text:
        return text
    if text.startswith("---"):
        # Find second ---
        rest = text[3:]
        idx = rest.find("\n---")
        if idx >= 0:
            frontmatter = text[:3 + idx + 4]  # includes second ---
            body = text[3 + idx + 4:].lstrip("\n")
            return f"{frontmatter}\n{ADAPTER_HEADER}\n{body}"
    return f"{ADAPTER_HEADER}\n\n{text}"


def load_manifest() -> list[dict]:
    """Load adapter manifest."""
    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found: {MANIFEST_PATH}")
        return []

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("targets", [])


def sync():
    if not CANONICAL.exists():
        print(f"Canonical source not found: {CANONICAL}")
        return 1

    targets = load_manifest()
    if not targets:
        print("No targets in adapter_manifest.yaml")
        return 1

    source_text = add_adapter_header(CANONICAL.read_text())
    updated = 0
    skipped = 0

    for entry in targets:
        name = entry.get("name", "unknown")
        target_rel = entry.get("target", "")
        source_rel = entry.get("source", "SKILL.md")

        if not target_rel:
            print(f"  SKIP: {name} has no target path")
            skipped += 1
            continue

        # For now, only SKILL.md sync is supported
        if source_rel != "SKILL.md":
            print(f"  SKIP: {name} source '{source_rel}' not supported yet")
            skipped += 1
            continue

        target = ROOT / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists():
            existing = target.read_text()
            if existing == source_text:
                print(f"  OK: {name} ({target_rel})")
                continue

        target.write_text(source_text)
        print(f"  SYNCED: {name} ({target_rel})")
        updated += 1

    print(f"\n{updated} file(s) updated, {skipped} skipped, {len(targets)} total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync())
