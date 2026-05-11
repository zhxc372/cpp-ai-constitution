"""CLI entry point for cpp-constitution."""

from __future__ import annotations

import argparse
import sys

from .generator import generate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cpp-constitution",
        description="Install C++ AI review skill into your project",
    )
    sub = parser.add_subparsers(dest="command")

    # install subcommand (primary)
    install = sub.add_parser("install", help="Install C++ review skill")
    install.add_argument("target", nargs="?", default=".", help="Target project directory (default: .)")
    install.add_argument(
        "--platform", "-p",
        choices=["opencode", "claude-code", "trae", "codebuddy", "cursor", "windsurf", "copilot", "amazonq", "lingma", "void", "codex-cli", "gemini-cli", "generic"],
        default=None,
        help="AI coding platform",
    )
    install.add_argument(
        "--std", "-s",
        choices=["c++17", "c++20", "c++23"],
        default=None,
        help="C++ standard",
    )
    install.add_argument(
        "--build", "-b",
        choices=["cmake", "make", "xmake", "meson", "autotools", "none"],
        default=None,
        help="Build system",
    )
    install.add_argument(
        "--exceptions", dest="exceptions",
        action="store_true", default=None,
        help="Exceptions enabled (default)",
    )
    install.add_argument(
        "--no-exceptions", dest="exceptions",
        action="store_false",
        help="Exceptions disabled (-fno-exceptions)",
    )
    install.add_argument(
        "--project-name", "-n",
        default=None,
        help="Project name (default: directory name)",
    )
    install.add_argument(
        "--no-interact",
        action="store_true",
        help="Skip interactive prompts, use defaults",
    )

    # init as alias for install (backward compat)
    init = sub.add_parser("init", help="Alias for 'install'")
    init.add_argument("target", nargs="?", default=".", help="Target project directory")
    init.add_argument("--platform", "-p", choices=["opencode", "claude-code", "trae", "codebuddy", "cursor", "windsurf", "copilot", "amazonq", "lingma", "void", "codex-cli", "gemini-cli", "generic"], default=None)
    init.add_argument("--std", "-s", choices=["c++17", "c++20", "c++23"], default=None)
    init.add_argument("--build", "-b", choices=["cmake", "make", "xmake", "meson", "autotools", "none"], default=None)
    init.add_argument("--exceptions", dest="exceptions", action="store_true", default=None)
    init.add_argument("--no-exceptions", dest="exceptions", action="store_false")
    init.add_argument("--project-name", "-n", default=None)
    init.add_argument("--no-interact", action="store_true")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    return generate(args)


if __name__ == "__main__":
    raise SystemExit(main())
