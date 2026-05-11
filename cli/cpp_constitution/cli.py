"""CLI entry point for cpp-constitution."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .generator import generate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cpp-constitution",
        description="Initialize C++ AI constitution for your project",
    )
    sub = parser.add_subparsers(dest="command")

    # init subcommand
    init = sub.add_parser("init", help="Initialize constitution in a project")
    init.add_argument("target", help="Target project directory")
    init.add_argument(
        "--platform", "-p",
        choices=["opencode", "claude-code", "trae", "codebuddy", "cursor", "windsurf", "copilot", "amazonq", "lingma", "void", "codex-cli", "gemini-cli", "generic"],
        default=None,
        help="AI coding platform",
    )
    init.add_argument(
        "--std", "-s",
        choices=["c++17", "c++20", "c++23"],
        default=None,
        help="C++ standard",
    )
    init.add_argument(
        "--build", "-b",
        choices=["cmake", "make", "xmake", "meson", "autotools", "none"],
        default=None,
        help="Build system",
    )
    init.add_argument(
        "--exceptions", dest="exceptions",
        action="store_true", default=None,
        help="Exceptions enabled (default)",
    )
    init.add_argument(
        "--no-exceptions", dest="exceptions",
        action="store_false",
        help="Exceptions disabled (-fno-exceptions)",
    )
    init.add_argument(
        "--project-name", "-n",
        default=None,
        help="Project name (default: directory name)",
    )
    init.add_argument(
        "--no-interact",
        action="store_true",
        help="Skip interactive prompts, use defaults",
    )

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "init":
        return generate(args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
