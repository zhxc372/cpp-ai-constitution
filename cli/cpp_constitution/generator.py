"""File generator for cpp-constitution install.

Superpowers model: zero intrusion into project root.
All skill files go into the platform's skill directory.
No AGENTS.md, no CONSTITUTION.md, no root-level pollution.
"""

from __future__ import annotations

import argparse
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
        return source, str(path), lambda: path.stat().st_mtime == mtime


def _get_template_env() -> Environment:
    return Environment(loader=PackageLoader(), keep_trailing_newline=True)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _copy_tree(src: Path, dst: Path) -> list[str]:
    """Copy directory tree, return list of relative paths created."""
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


# ============================================================
# Platform definitions
# ============================================================

# Skill-type platforms: SKILL.md + references + config → platform skill dir
PLATFORM_SKILL_DIR = {
    "opencode": ".opencode/skills/cpp-core-review",
    "claude-code": ".claude/skills/cpp-core-review",
    "trae": ".trae/skills/cpp-core-review",
    "codebuddy": ".codebuddy/skills/cpp-core-review",
    "gemini-cli": ".gemini/skills/cpp-core-review",
}

# Rule-type platforms: self-contained single file → project root relative path
PLATFORM_RULE_FILE = {
    "cursor": ".cursor/rules/cpp-review.mdc",
    "windsurf": ".windsurfrules",
    "copilot": ".github/copilot-instructions.md",
    "amazonq": ".amazonq/rules/cpp-review.md",
    "lingma": ".lingma/rules/cpp-review.md",
    "void": ".void/rules/cpp-review.md",
    "codex-cli": None,   # uses generic AGENTS.md
    "generic": None,     # uses generic AGENTS.md
}

# Platforms that also get a minimal CLAUDE.md pointing to the skill
PLATFORM_EXTRA_FILES = {
    "opencode": {"opencode.json": "platforms/opencode/opencode.json.example"},
}


def _get_skill_dir(platform: str) -> str | None:
    """Return the skill directory for a platform, or None for rule-type."""
    return PLATFORM_SKILL_DIR.get(platform)


def _get_rule_file(platform: str) -> str | None:
    """Return the rule file path for a rule-type platform, or None."""
    return PLATFORM_RULE_FILE.get(platform)


def generate(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()

    if not target.exists():
        print(f"❌ Target directory does not exist: {target}")
        return 1

    project_name = args.project_name or target.name

    # Interactive or non-interactive config
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
    runtime_dir = Path(__file__).parent / "runtime"
    created_files = []

    skill_dir_rel = _get_skill_dir(config.platform)
    rule_file_rel = _get_rule_file(config.platform)

    if skill_dir_rel:
        # ──────────────────────────────────────────────
        # Skill-type platform (OpenCode, Claude Code, Trae, etc.)
        # Everything goes into the skill directory.
        # Zero root-level files.
        # ──────────────────────────────────────────────
        skill_root = target / skill_dir_rel

        # 1. SKILL.md — the core review logic
        _render_template(env, "skill.md.j2", ctx, skill_root / "SKILL.md")
        created_files.append(f"{skill_dir_rel}/SKILL.md")

        # 2. project-config.md — replaces CONSTITUTION.md (inside skill dir)
        _render_template(env, "constitution.md.j2", ctx, skill_root / "project-config.md")
        created_files.append(f"{skill_dir_rel}/project-config.md")

        # 3. references/ — detailed C++ review rules
        ref_src = runtime_dir / "references"
        if ref_src.exists():
            copied = _copy_tree(ref_src, skill_root / "references")
            for f in copied:
                created_files.append(f"{skill_dir_rel}/references/{f}")

        # 4. config/ — clang-tidy configs
        cfg_src = runtime_dir / "config"
        if cfg_src.exists():
            copied = _copy_tree(cfg_src, skill_root / "config")
            for f in copied:
                created_files.append(f"{skill_dir_rel}/config/{f}")

        # 5. GOTCHAS.md — common failure modes
        gotchas_src = runtime_dir / "GOTCHAS.md"
        if gotchas_src.exists():
            shutil.copy2(gotchas_src, skill_root / "GOTCHAS.md")
            created_files.append(f"{skill_dir_rel}/GOTCHAS.md")

        # 6. Platform-specific extras (opencode.json, agents, etc.)
        platform_extras = PLATFORM_EXTRA_FILES.get(config.platform, {})
        for dst_name, src_rel in platform_extras.items():
            src_file = template_dir / src_rel
            if src_file.exists():
                _ensure_dir(target / skill_dir_rel)
                shutil.copy2(src_file, target / dst_name)
                created_files.append(dst_name)

        # 7. Platform agents (opencode-specific sub-agents)
        agents_src = template_dir / "platforms" / config.platform / "agents"
        if agents_src.exists():
            copied = _copy_tree(agents_src, skill_root / "agents")
            for f in copied:
                created_files.append(f"{skill_dir_rel}/agents/{f}")

    elif rule_file_rel:
        # ──────────────────────────────────────────────
        # Rule-type platform (Cursor, Copilot, Windsurf, etc.)
        # Self-contained rule file, no references dependency.
        # Zero root-level files (rule file is in hidden dir).
        # ──────────────────────────────────────────────
        platform_dir = template_dir / "platforms" / config.platform

        # Find Jinja2 template for this platform
        template_found = None
        for t in sorted(platform_dir.iterdir()):
            if t.suffix == '.j2' and t.is_file():
                template_found = t
                break

        if template_found:
            rel_path = template_found.relative_to(template_dir)
            _render_template(env, str(rel_path), ctx, target / rule_file_rel)
            created_files.append(rule_file_rel)
        else:
            print(f"⚠️  No template found for {config.platform}")
            return 1

    else:
        # ──────────────────────────────────────────────
        # Generic / Codex CLI — AGENTS.md only
        # ──────────────────────────────────────────────
        _render_template(env, "agents.md.j2", ctx, target / "AGENTS.md")
        created_files.append("AGENTS.md")

    # Summary
    print(f"\n✅ C++ review skill installed!")
    print(f"   Target: {target}")
    print(f"   Platform: {config.platform}")
    print(f"   C++ {config.std}, {config.build}, exceptions {'ON' if config.exceptions else 'OFF'}")
    print(f"   Files created: {len(created_files)}")
    print()
    for f in sorted(set(created_files)):
        marker = " ⭐" if "SKILL.md" in f else ""
        print(f"   • {f}{marker}")

    return 0
