"""Interactive prompts for cpp-constitution init."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InitConfig:
    platform: str = "opencode"
    std: str = "c++20"
    build: str = "cmake"
    exceptions: bool = True
    project_name: str = ""


PLATFORMS = {
    "opencode": "OpenCode",
    "claude-code": "Claude Code",
    "cursor": "Cursor",
    "codex-cli": "Codex CLI",
    "gemini-cli": "Gemini CLI",
    "generic": "Generic (AGENTS.md only)",
}

STDS = ["c++17", "c++20", "c++23"]
BUILDS = ["cmake", "make", "xmake", "meson", "autotools", "none"]


def _ask_select(prompt: str, options: list[str] | dict, default: int = 0) -> str:
    """Ask user to select from options."""
    if isinstance(options, dict):
        keys = list(options.keys())
        labels = list(options.values())
    else:
        keys = options
        labels = options

    print(f"\n{prompt}")
    for i, label in enumerate(labels):
        marker = " →" if i == default else "  "
        print(f"  {marker} {i + 1}. {label}")

    while True:
        try:
            choice = input(f"  Select [{default + 1}]: ").strip()
            if not choice:
                return keys[default]
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                return keys[idx]
            print(f"  Please enter 1-{len(keys)}")
        except (ValueError, EOFError):
            return keys[default]


def _ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask yes/no question."""
    hint = "Y/n" if default else "y/N"
    while True:
        try:
            choice = input(f"  {prompt} [{hint}]: ").strip().lower()
            if not choice:
                return default
            if choice in ("y", "yes"):
                return True
            if choice in ("n", "no"):
                return False
            print("  Please enter y or n")
        except EOFError:
            return default


def interactive_prompt(project_name: str) -> InitConfig:
    """Run interactive prompts and return config."""
    print("=" * 50)
    print("🔧 C++ AI Constitution Initializer")
    print("=" * 50)
    print(f"\n  Target project: {project_name}")

    config = InitConfig(project_name=project_name)

    print("\n📋 Answer a few questions to generate your constitution:\n")

    config.platform = _ask_select(
        "Which AI coding platform?", PLATFORMS, default=0
    )

    std_default = STDS.index("c++20")
    config.std = _ask_select(
        "C++ standard?", STDS, default=std_default
    )

    build_default = BUILDS.index("cmake")
    config.build = _ask_select(
        "Build system?", BUILDS, default=build_default
    )

    config.exceptions = _ask_yes_no(
        "Exceptions enabled?", default=True
    )

    print("\n" + "=" * 50)
    print("📋 Configuration summary:")
    print(f"  Platform:   {PLATFORMS.get(config.platform, config.platform)}")
    print(f"  C++ std:    {config.std}")
    print(f"  Build:      {config.build}")
    print(f"  Exceptions: {'enabled' if config.exceptions else 'disabled'}")
    print("=" * 50)

    return config
