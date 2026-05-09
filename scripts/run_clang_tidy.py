#!/usr/bin/env python3
"""Run clang-tidy on C++ files and summarize diagnostics."""

import json
import subprocess
import sys
from pathlib import Path


def find_files():
    root = Path(".")
    extensions = ("*.cpp", "*.hpp", "*.cc", "*.h")
    files = []
    for ext in extensions:
        files.extend(root.glob(f"**/{ext}"))
    # Exclude common non-source directories
    exclude = {".git", "build", "cmake-build-", "node_modules", "__pycache__"}
    files = [f for f in files if not any(e in f.parts for e in exclude)]
    return sorted(files)


def run_clang_tidy(filepath, config_file="config/.clang-tidy"):
    cmd = [
        "clang-tidy",
        str(filepath),
        "--config-file", config_file,
        "--",
        "-std=c++20",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except FileNotFoundError:
        return "ERROR: clang-tidy not found"
    except subprocess.TimeoutExpired:
        return "ERROR: clang-tidy timed out"


def summarize(output):
    severities = {"error": 0, "warning": 0, "note": 0}
    for line in output.splitlines():
        low = line.lower()
        if "error:" in low:
            severities["error"] += 1
        elif "warning:" in low:
            severities["warning"] += 1
        elif "note:" in low:
            severities["note"] += 1
    return severities


def main():
    files = find_files()
    if not files:
        print("No C++ files found.")
        return 0

    print(f"Found {len(files)} C++ files")

    total = {"error": 0, "warning": 0, "note": 0}
    results = []

    for f in files:
        print(f"Checking {f}...")
        output = run_clang_tidy(f)
        counts = summarize(output)
        for k in total:
            total[k] += counts[k]
        if counts["error"] > 0 or counts["warning"] > 0:
            results.append({"file": str(f), "counts": counts, "output": output})

    print(f"\n{'='*50}")
    print(f"Total: {total['error']} errors, {total['warning']} warnings, {total['note']} notes")

    if results:
        print(f"\nFiles with issues:")
        for r in results:
            print(f"  {r['file']}: {r['counts']['error']} errors, {r['counts']['warning']} warnings")

    return 1 if total["error"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
