"""File generator for cpp-constitution init."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

import jinja2
from jinja2 import Environment, BaseLoader

from .prompts import InitConfig, interactive_prompt


class PackageLoader(BaseLoader):
    """Load templates from the cpp_constitution/templates package directory."""

    def __init__(self):
        self.path = Path(__file__).parent / "templates"
        if not self.path.exists():
            raise FileNotFoundError(f"Templates not found at {self.path}")

    def get_source(self, environment, template):
        path = self.path / template
        if not path.exists():
            raise jinja2.TemplateNotFound(template)
        mtime = path.stat().st_mtime
        source = path.read_text(encoding="utf-8")
        # Return source, filename, uptodate callable
        return source, str(path), lambda: path.stat().st_mtime == mtime



def _get_template_env() -> Environment:
    return Environment(loader=PackageLoader(), keep_trailing_newline=True)


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


# Where each platform stores its skill files
PLATFORM_SKILL_PATHS = {
    "opencode": [".opencode/skills/cpp-core-review"],
    "claude-code": [".claude/skills/cpp-core-review"],
    "trae": [".trae/skills/cpp-core-review"],
    "codebuddy": [".codebuddy/skills/cpp-core-review"],
    "gemini-cli": [".gemini/skills/cpp-core-review"],
    # Rule-type platforms (no skill directory)
    "cursor": [],
    "windsurf": [],
    "copilot": [],
    "amazonq": [],
    "lingma": [],
    "void": [],
    "codex-cli": [],
    "generic": [],
}

PLATFORM_RULE_FILE = {
    "opencode": None,
    "claude-code": "CLAUDE.md",
    "trae": None,
    "codebuddy": None,
    "gemini-cli": None,
    # Rule-type platforms
    "cursor": ".cursor/rules/cpp-review.mdc",
    "windsurf": ".windsurfrules",
    "copilot": ".github/copilot-instructions.md",
    "amazonq": ".amazonq/rules/cpp-review.md",
    "lingma": ".lingma/rules/cpp-review.md",
    "void": ".void/rules/cpp-review.md",
    "codex-cli": None,
    "generic": None,
}


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
    template_dir = Path(__file__).parent / "templates"
    created_files = []

    # === 1. CONSTITUTION.md (minimal project config) ===
    _render_template(env, "constitution.md.j2", ctx, target / "CONSTITUTION.md")
    created_files.append("CONSTITUTION.md")

    # === 2. AGENTS.md (minimal, just points to skill) ===
    _render_template(env, "agents.md.j2", ctx, target / "AGENTS.md")
    created_files.append("AGENTS.md")

    # === 3. Skill file OR Rule file (the core) ===
    skill_paths = PLATFORM_SKILL_PATHS.get(config.platform, [])
    rule_file = PLATFORM_RULE_FILE.get(config.platform)

    if skill_paths:
        # Skill-type platform: generate SKILL.md (references .cpp-constitution/)
        for skill_dir in skill_paths:
            skill_file = target / skill_dir / "SKILL.md"
            _render_template(env, "skill.md.j2", ctx, skill_file)
            created_files.append(f"{skill_dir}/SKILL.md")
    elif rule_file:
        # Rule-type platform: generate self-contained rule file
        # Find the Jinja2 template for this platform
        platform_dir = template_dir / "platforms" / config.platform
        # Find template file
        template_found = None
        for t in platform_dir.iterdir():
            if t.suffix == '.j2' and t.is_file():
                template_found = t
                break
        if template_found:
            # Get relative template name for Jinja2
            rel_path = template_found.relative_to(template_dir)
            _render_template(env, str(rel_path), ctx, target / rule_file)
            created_files.append(rule_file)
    else:
        # Generic: put skill in skills/ directory
        skill_file = target / "skills" / "cpp-core-review" / "SKILL.md"
        _render_template(env, "skill.md.j2", ctx, skill_file)
        created_files.append("skills/cpp-core-review/SKILL.md")

    # === 4. Platform additional files (CLAUDE.md, .cursorrules, etc.) ===
    # For skill-type platforms that also have a rule file (e.g. Claude Code)
    if skill_paths and rule_file:
        platform_dir = template_dir / "platforms" / config.platform
        candidates = [
            platform_dir / rule_file,
            platform_dir / rule_file.lstrip("."),
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

    # Platform-specific structure (agents → .cpp-constitution/agents/)
    platform_dir = template_dir / "platforms" / config.platform
    if platform_dir.exists():
        agents_dir = platform_dir / "agents"
        if agents_dir.exists():
            copied = _copy_tree(agents_dir, target / ".cpp-constitution" / "agents")
            created_files.extend(copied)
        for cfg in platform_dir.glob("*.example"):
            dst_name = cfg.name.replace(".example", "")
            shutil.copy2(cfg, target / dst_name)
            created_files.append(dst_name)

    # === 5. Runtime files → .cpp-constitution/ (hidden, clean layout) ===
    runtime_dir = Path(__file__).parent / "runtime"
    runtime_target = target / ".cpp-constitution"
    for item in ["references", "config", "GOTCHAS.md"]:
        src = runtime_dir / item
        if src.exists():
            if src.is_dir():
                copied = _copy_tree(src, runtime_target / item)
            else:
                _ensure_dir((runtime_target / item).parent)
                shutil.copy2(src, runtime_target / item)
                copied = [f".cpp-constitution/{item}"]
            created_files.extend(copied)

    # === 6. validate.sh → .cpp-constitution/scripts/ ===
    _render_template(env, "build_validate.sh.j2", ctx, runtime_target / "scripts" / "validate.sh")
    (runtime_target / "scripts" / "validate.sh").chmod(0o755)
    created_files.append(".cpp-constitution/scripts/validate.sh")

    # === 7. Build system skeleton ===
    if config.build != "none":
        build_file_map = {
            "cmake": "CMakeLists.txt",
            "make": "Makefile",
            "xmake": "xmake.lua",
            "meson": "meson.build",
            "autotools": "configure.ac",
        }
        build_template = f"build_{config.build}.j2"
        output_name = build_file_map.get(config.build)
        if output_name and (template_dir / build_template).exists():
            output_path = target / output_name
            if not output_path.exists():
                _render_template(env, build_template, ctx, output_path)
                created_files.append(output_name)
                print(f"  📦 Created {output_name} (skeleton)")
            else:
                print(f"  ⏭️  Skipped {output_name} (already exists)")

    # === 8. No README overwrite ===
    # Do NOT generate README.md in user's project root
    # Runtime docs go to .cpp-constitution/README.md only if no root README exists

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
