"""File generator for cpp-constitution init."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .prompts import InitConfig, interactive_prompt

# Source of truth: this repo (cli/ is part of cpp-ai-constitution)
_PACKAGE_DIR = Path(__file__).parent
_PROJECT_DIR = _PACKAGE_DIR.parent  # cli/
_REPO_ROOT = _PROJECT_DIR.parent  # repo root
_TEMPLATE_CANDIDATES = [
    _PACKAGE_DIR / "templates",  # cpp_constitution/templates/ (packaged)
    _PROJECT_DIR / "templates",  # cli/templates/ (editable dev)
]

# Where each platform stores its skill files
PLATFORM_SKILL_PATHS = {
    "opencode": [".opencode/skills/cpp-core-review"],
    "claude-code": [".claude/skills/cpp-core-review"],
    "cursor": [],
    "codex-cli": [],
    "gemini-cli": [".gemini/skills/cpp-core-review"],
    "generic": [],
}

PLATFORM_RULE_FILE = {
    "opencode": None,  # uses .opencode/ structure
    "claude-code": "CLAUDE.md",
    "cursor": ".cursorrules",
    "codex-cli": None,  # uses AGENTS.md
    "gemini-cli": None,
    "generic": None,
}


def _get_template_dir() -> Path:
    for d in _TEMPLATE_CANDIDATES:
        if d.exists() and (d / "constitution.md.j2").exists():
            return d
    raise FileNotFoundError(
        f"Templates not found. Searched: {[str(d) for d in _TEMPLATE_CANDIDATES]}"
    )


def _get_template_env() -> Environment:
    template_dir = _get_template_dir()
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        keep_trailing_newline=True,
    )


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _copy_tree(src: Path, dst: Path) -> list[str]:
    files = []
    if not src.exists():
        return files
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = dst / rel
            _ensure_dir(target.parent)
            shutil.copy2(item, target)
            files.append(str(rel))
    return files


def _render_template(env: Environment, name: str, context: dict, output: Path) -> str:
    template = env.get_template(name)
    content = template.render(**context)
    _ensure_dir(output.parent)
    output.write_text(content, encoding="utf-8")
    return content


def generate(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()

    if not target.exists():
        print(f"❌ Target directory does not exist: {target}")
        return 1

    project_name = args.project_name or target.name

    if args.no_interact:
        config = InitConfig(
            platform=args.platform or "opencode",
            std=args.std or "c++20",
            build=args.build or "cmake",
            exceptions=args.exceptions if args.exceptions is not None else True,
            project_name=project_name,
        )
    else:
        config = interactive_prompt(project_name)
        if args.platform:
            config.platform = args.platform
        if args.std:
            config.std = args.std
        if args.build:
            config.build = args.build
        if args.exceptions is not None:
            config.exceptions = args.exceptions

    ctx = {
        "project_name": config.project_name,
        "platform": config.platform,
        "std": config.std,
        "std_version": config.std.replace("c++", ""),
        "build": config.build,
        "exceptions": config.exceptions,
        "exceptions_flag": "" if config.exceptions else "-fno-exceptions",
    }

    env = _get_template_env()
    template_dir = _get_template_dir()
    created_files = []

    # === 1. CONSTITUTION.md (minimal project config) ===
    _render_template(env, "constitution.md.j2", ctx, target / "CONSTITUTION.md")
    created_files.append("CONSTITUTION.md")

    # === 2. AGENTS.md (minimal, just points to skill) ===
    _render_template(env, "agents.md.j2", ctx, target / "AGENTS.md")
    created_files.append("AGENTS.md")

    # === 3. Skill file (the core — rendered from skill.md.j2) ===
    skill_paths = PLATFORM_SKILL_PATHS.get(config.platform, [])
    if skill_paths:
        for skill_dir in skill_paths:
            skill_file = target / skill_dir / "SKILL.md"
            _render_template(env, "skill.md.j2", ctx, skill_file)
            created_files.append(f"{skill_dir}/SKILL.md")
    else:
        # Generic: put skill in skills/ directory
        skill_file = target / "skills" / "cpp-core-review" / "SKILL.md"
        _render_template(env, "skill.md.j2", ctx, skill_file)
        created_files.append("skills/cpp-core-review/SKILL.md")

    # === 4. Platform rule file (CLAUDE.md, .cursorrules, etc.) ===
    rule_file = PLATFORM_RULE_FILE.get(config.platform)
    if rule_file:
        # Platforms with a specific entry point file (CLAUDE.md, .cursorrules, etc.)
        platform_dir = template_dir / "platforms" / config.platform
        # Try multiple naming conventions
        candidates = [
            platform_dir / rule_file,
            platform_dir / rule_file.lstrip('.'),
            platform_dir / ("_" + rule_file.lstrip('.').replace('.', '_') + ".md"),
            platform_dir / (rule_file.lstrip('.').replace('.', '_') + ".md"),
        ]
        src_file = None
        for c in candidates:
            if c.exists():
                src_file = c
                break

        if src_file:
            dst = target / rule_file
            _ensure_dir(dst.parent)
            shutil.copy2(src_file, dst)
            created_files.append(rule_file)

    # Platform-specific structure (opencode agents, etc.)
    platform_dir = template_dir / "platforms" / config.platform
    if platform_dir.exists():
        agents_dir = platform_dir / "agents"
        if agents_dir.exists():
            copied = _copy_tree(agents_dir, target / "agents")
            created_files.extend(copied)
        # Copy config files
        for cfg in platform_dir.glob("*.example"):
            dst_name = cfg.name.replace(".example", "")
            shutil.copy2(cfg, target / dst_name)
            created_files.append(dst_name)

    # === 5. References (from repo root — single source of truth) ===
    shared_source = _REPO_ROOT
    for item in ["references", "config", "GOTCHAS.md"]:
        src = shared_source / item
        if src.exists():
            if src.is_dir():
                copied = _copy_tree(src, target / item)
            else:
                _ensure_dir((target / item).parent)
                shutil.copy2(src, target / item)
                copied = [item]
            created_files.extend(copied)

    # === 6. validate.sh ===
    _render_template(env, "build/validate.sh.j2", ctx, target / "scripts" / "validate.sh")
    (target / "scripts" / "validate.sh").chmod(0o755)
    created_files.append("scripts/validate.sh")

    # === 7. Build system skeleton (optional, non-overwriting) ===
    if config.build != "none":
        build_file_map = {
            "cmake": "CMakeLists.txt",
            "make": "Makefile",
            "xmake": "xmake.lua",
            "meson": "meson.build",
            "autotools": "configure.ac",
        }
        build_template = f"build/{config.build}.j2"
        output_name = build_file_map.get(config.build)
        if output_name and (template_dir / build_template).exists():
            output_path = target / output_name
            if not output_path.exists():
                _render_template(env, build_template, ctx, output_path)
                created_files.append(output_name)
                print(f"  📦 Created {output_name} (skeleton)")
            else:
                print(f"  ⏭️  Skipped {output_name} (already exists)")

    # === 8. README.md (usage guide) ===
    readme_path = target / "README.md"
    if not readme_path.exists():
        _render_template(env, "readme.md.j2", ctx, readme_path)
        created_files.append("README.md")

    # Summary
    print("\n✅ C++ review skill initialized!")
    print(f"   Target: {target}")
    print(f"   Platform: {config.platform}")
    print(f"   C++ {config.std}, {config.build}, exceptions {'ON' if config.exceptions else 'OFF'}")
    print(f"   Files created: {len(created_files)}")
    print()
    print("   Key files:")
    print(f"     • CONSTITUTION.md  (project config)")
    print(f"     • AGENTS.md        (entry point)")
    for f in sorted(set(created_files)):
        if "SKILL.md" in f:
            print(f"     • {f}  ⭐ (core skill)")
    print()
    print("   All files:")
    for f in sorted(set(created_files)):
        print(f"     • {f}")

    return 0
