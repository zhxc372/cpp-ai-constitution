#!/usr/bin/env python3
"""Run clang-tidy on C++ files with profile support and structured output.

Usage:
  python3 scripts/run_clang_tidy.py --profile minimal
  python3 scripts/run_clang_tidy.py --profile strict --compile-commands build/compile_commands.json
  python3 scripts/run_clang_tidy.py --std c++23 --changed-only --format json
  python3 scripts/run_clang_tidy.py --fail-on error --output results.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
PROFILES = {
    "minimal": "config/clang-tidy.minimal.yml",
    "migration": "config/clang-tidy.migration.yml",
    "strict": "config/clang-tidy.strict.yml",
}
STD_OPTIONS = ("c++17", "c++20", "c++23")
FAIL_OPTIONS = ("error", "warning", "none")


def find_files(changed_only: bool = False) -> list[Path]:
    """Find C++ source files to check."""
    root = Path(".")
    extensions = ("*.cpp", "*.hpp", "*.cc", "*.h", "*.cxx", "*.hxx")
    files = []
    for ext in extensions:
        files.extend(root.glob(f"**/{ext}"))

    exclude = {".git", "build", "cmake-build-", "node_modules", "__pycache__", "third_party", "vendor"}
    files = [f for f in files if not any(e in f.parts for e in exclude)]

    if changed_only:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD"],
                capture_output=True, text=True, timeout=10
            )
            changed = set(result.stdout.strip().splitlines())
            files = [f for f in files if str(f) in changed]
        except Exception:
            print("Warning: --changed-only requires git. Scanning all files.")

    return sorted(files)


def run_clang_tidy(
    filepath: str | Path,
    config_file: str,
    compile_commands: str | None = None,
    std: str = "c++20",
) -> dict:
    """Run clang-tidy on a single file and return structured result."""
    cmd = ["clang-tidy", str(filepath), "--config-file", config_file]

    if compile_commands:
        cmd.extend(["-p", compile_commands])

    cmd.extend(["--", f"-std={std}"])

    result_dict = {"file": str(filepath), "diagnostics": [], "error": None}

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
    except FileNotFoundError:
        result_dict["error"] = "clang-tidy not found"
        return result_dict
    except subprocess.TimeoutExpired:
        result_dict["error"] = "clang-tidy timed out"
        return result_dict

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if "error:" in low:
            result_dict["diagnostics"].append({"severity": "error", "line": line})
        elif "warning:" in low:
            result_dict["diagnostics"].append({"severity": "warning", "line": line})
        elif "note:" in low:
            result_dict["diagnostics"].append({"severity": "note", "line": line})

    return result_dict


def format_json(results: list[dict], total: dict, config: dict) -> str:
    """Format results as JSON."""
    return json.dumps({
        "timestamp": datetime.now().isoformat(),
        "config": config,
        "summary": total,
        "results": results,
    }, indent=2, ensure_ascii=False)


def format_markdown(results: list[dict], total: dict, config: dict) -> str:
    """Format results as Markdown."""
    lines = [
        "# clang-tidy Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Profile:** {config.get('profile', 'default')}",
        f"**Standard:** {config.get('std', 'c++20')}",
        f"**Files checked:** {config.get('file_count', 0)}",
        "",
        "## Summary",
        "",
        f"| Severity | Count |",
        f"|----------|-------|",
        f"| Error    | {total.get('error', 0)} |",
        f"| Warning  | {total.get('warning', 0)} |",
        f"| Note     | {total.get('note', 0)} |",
        "",
    ]

    issues = [r for r in results if r["diagnostics"] or r["error"]]
    if issues:
        lines.append("## Files with Issues")
        lines.append("")
        for r in issues:
            if r["error"]:
                lines.append(f"### {r['file']}")
                lines.append(f"**Error:** {r['error']}")
            else:
                lines.append(f"### {r['file']}")
                for d in r["diagnostics"]:
                    lines.append(f"- [{d['severity'].upper()}] {d['line']}")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run clang-tidy with profile support")
    parser.add_argument("--profile", choices=list(PROFILES.keys()),
                        help="Preset profile: minimal, migration, strict")
    parser.add_argument("--config-file", help="Custom config file path")
    parser.add_argument("--compile-commands", "-p",
                        help="Path to compile_commands.json directory")
    parser.add_argument("--std", choices=STD_OPTIONS, default="c++20",
                        help="C++ standard (default: c++20)")
    parser.add_argument("--changed-only", action="store_true",
                        help="Only check git-changed files")
    parser.add_argument("--fail-on", choices=FAIL_OPTIONS, default="error",
                        help="Exit with error code on: error, warning, none (default: error)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--output", "-o", help="Write output to file instead of stdout")
    args = parser.parse_args()

    # Determine config file
    if args.profile:
        config_file = PROFILES[args.profile]
    elif args.config_file:
        config_file = args.config_file
    else:
        config_file = "config/.clang-tidy"

    if not Path(config_file).exists():
        print(f"ERROR: config file not found: {config_file}")
        return 1

    files = find_files(changed_only=args.changed_only)
    if not files:
        print("No C++ files found.")
        return 0

    config_info = {
        "profile": args.profile or "default",
        "config_file": config_file,
        "std": args.std,
        "compile_commands": args.compile_commands,
        "file_count": len(files),
    }

    if args.format == "text":
        print(f"Profile: {args.profile or 'default'} → {config_file}")
        print(f"Standard: {args.std}")
        print(f"Files: {len(files)}")
        print()

    total = {"error": 0, "warning": 0, "note": 0}
    results = []

    for f in files:
        if args.format == "text":
            print(f"  Checking {f}...")

        r = run_clang_tidy(f, config_file, args.compile_commands, args.std)
        results.append(r)

        for d in r["diagnostics"]:
            total[d["severity"]] = total.get(d["severity"], 0) + 1

        if r["error"]:
            total["error"] = total.get("error", 0) + 1

    # Output
    if args.format == "json":
        output = format_json(results, total, config_info)
    elif args.format == "markdown":
        output = format_markdown(results, total, config_info)
    else:
        output = None
        print(f"\n{'='*50}")
        print(f"Total: {total['error']} errors, {total['warning']} warnings, {total['note']} notes")
        issues = [r for r in results if r["diagnostics"] or r["error"]]
        if issues:
            print(f"\nFiles with issues:")
            for r in issues:
                ec = sum(1 for d in r["diagnostics"] if d["severity"] == "error")
                wc = sum(1 for d in r["diagnostics"] if d["severity"] == "warning")
                extra = f" [{r['error']}]" if r["error"] else ""
                print(f"  {r['file']}: {ec} errors, {wc} warnings{extra}")

    if output:
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Output written to {args.output}")
        else:
            print(output)

    # Exit code
    if args.fail_on == "none":
        return 0
    if args.fail_on == "warning":
        return 1 if total["error"] > 0 or total["warning"] > 0 else 0
    return 1 if total["error"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
