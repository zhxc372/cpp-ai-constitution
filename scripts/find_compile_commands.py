#!/usr/bin/env python3
"""Find or generate compile_commands.json for clang-tidy."""

import json
import os
import subprocess
import sys
from pathlib import Path


def find_existing():
    candidates = [
        Path("compile_commands.json"),
        Path("build/compile_commands.json"),
        Path("cmake-build-debug/compile_commands.json"),
        Path("cmake-build-release/compile_commands.json"),
    ]
    for c in candidates:
        if c.exists():
            print(f"Found: {c}")
            return str(c)
    return None


def generate_cmake():
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    cmd = ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", ".."]
    print(f"Running: {' '.join(cmd)} in {build_dir}")
    result = subprocess.run(cmd, cwd=build_dir, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"cmake failed: {result.stderr}")
        return None

    cc = build_dir / "compile_commands.json"
    if cc.exists():
        # Symlink to root for convenience
        target = Path("compile_commands.json")
        if not target.exists():
            target.symlink_to(cc)
        print(f"Generated: {cc}")
        return str(cc)

    return None


def main():
    existing = find_existing()
    if existing:
        return 0

    # Try to generate
    cmake_lists = Path("CMakeLists.txt")
    if cmake_lists.exists():
        result = generate_cmake()
        if result:
            return 0

    print("No compile_commands.json found and could not auto-generate.")
    print("Run: cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON")
    return 1


if __name__ == "__main__":
    sys.exit(main())
