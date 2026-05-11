"""Tests for cpp-constitution CLI — superpowers model (zero intrusion)."""

import tempfile
from pathlib import Path


def _run_generate(tmp, **kwargs):
    """Helper to run generate with given config."""
    target = Path(tmp) / kwargs.pop("name", "test-project")
    target.mkdir(exist_ok=True)

    from argparse import Namespace
    defaults = dict(
        target=str(target),
        platform="opencode",
        std="c++20",
        build="cmake",
        exceptions=True,
        project_name=target.name,
        no_interact=True,
    )
    defaults.update(kwargs)
    args = Namespace(**defaults)

    from cpp_constitution.generator import generate
    result = generate(args)
    assert result == 0, f"Generation failed for {target.name}"
    return target


def _list_root(target: Path) -> list[str]:
    """List top-level items in target directory."""
    return sorted(p.name for p in target.iterdir())


# ──────────────────────────────────────
# Skill-type platforms
# ──────────────────────────────────────

def test_opencode_skill_is_self_contained():
    """OpenCode: everything in .opencode/skills/cpp-core-review/, no AGENTS/CONSTITUTION at root."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="opencode-test")

        # Root should only have .opencode/ and opencode.json (platform config)
        root_items = _list_root(target)
        assert ".opencode" in root_items, f"Missing .opencode, got: {root_items}"
        assert "AGENTS.md" not in root_items
        assert "CONSTITUTION.md" not in root_items
        assert "GOTCHAS.md" not in root_items

        skill_dir = target / ".opencode" / "skills" / "cpp-core-review"
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "project-config.md").exists()
        assert (skill_dir / "GOTCHAS.md").exists()
        assert (skill_dir / "references").is_dir()
        assert (skill_dir / "config").is_dir()

        # project-config has C++ version
        config = (skill_dir / "project-config.md").read_text()
        assert "c++20" in config

        # SKILL.md has review logic
        skill = (skill_dir / "SKILL.md").read_text()
        assert "review" in skill.lower()


def test_opencode_no_exceptions():
    """OpenCode: no-exceptions flag in project-config.md."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="noexc-test", exceptions=False)

        config = (target / ".opencode" / "skills" / "cpp-core-review" / "project-config.md").read_text()
        assert "disabled" in config.lower() or "OFF" in config

        skill = (target / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md").read_text()
        assert "DISABLED" in skill or "no-exceptions" in skill.lower() or "no throw" in skill.lower()


def test_claude_code():
    """Claude Code: skill in .claude/skills/."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="claude-test", platform="claude-code")

        root_items = _list_root(target)
        assert root_items == [".claude"], f"Expected only .claude at root, got: {root_items}"

        skill_dir = target / ".claude" / "skills" / "cpp-core-review"
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "project-config.md").exists()
        assert (skill_dir / "references").is_dir()


def test_trae():
    """Trae: skill in .trae/skills/."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="trae-test", platform="trae")

        root_items = _list_root(target)
        assert root_items == [".trae"], f"Expected only .trae at root, got: {root_items}"

        skill_dir = target / ".trae" / "skills" / "cpp-core-review"
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "project-config.md").exists()


def test_codebuddy():
    """CodeBuddy: skill in .codebuddy/skills/."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="codebuddy-test", platform="codebuddy")

        root_items = _list_root(target)
        assert root_items == [".codebuddy"], f"Expected only .codebuddy at root, got: {root_items}"

        skill_dir = target / ".codebuddy" / "skills" / "cpp-core-review"
        assert (skill_dir / "SKILL.md").exists()


# ──────────────────────────────────────
# Rule-type platforms
# ──────────────────────────────────────

def test_cursor():
    """Cursor: self-contained .cursor/rules/cpp-review.mdc."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="cursor-test", platform="cursor", std="c++23", build="xmake")

        rule = target / ".cursor" / "rules" / "cpp-review.mdc"
        assert rule.exists(), f"Cursor rule not found, root: {_list_root(target)}"

        content = rule.read_text()
        assert "Review Priority" in content
        assert "c++23" in content

        # Should be self-contained — no references to .cpp-constitution/
        assert ".cpp-constitution" not in content


def test_copilot():
    """Copilot: self-contained .github/copilot-instructions.md."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="copilot-test", platform="copilot")

        rule = target / ".github" / "copilot-instructions.md"
        assert rule.exists()
        content = rule.read_text()
        assert "Review Priority" in content
        assert ".cpp-constitution" not in content


def test_windsurf():
    """Windsurf: self-contained .windsurfrules."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="windsurf-test", platform="windsurf")

        rule = target / ".windsurfrules"
        assert rule.exists()
        content = rule.read_text()
        assert "Review Priority" in content


def test_amazonq():
    """Amazon Q: self-contained .amazonq/rules/cpp-review.md."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="amazonq-test", platform="amazonq")

        rule = target / ".amazonq" / "rules" / "cpp-review.md"
        assert rule.exists()
        content = rule.read_text()
        assert "Review Priority" in content


def test_lingma():
    """通义灵码: self-contained .lingma/rules/cpp-review.md."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="lingma-test", platform="lingma")

        rule = target / ".lingma" / "rules" / "cpp-review.md"
        assert rule.exists()
        content = rule.read_text()
        assert "Review Priority" in content


def test_void():
    """Void: self-contained .void/rules/cpp-review.md."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="void-test", platform="void")

        rule = target / ".void" / "rules" / "cpp-review.md"
        assert rule.exists()
        content = rule.read_text()
        assert "Review Priority" in content


# ──────────────────────────────────────
# Generic platforms
# ──────────────────────────────────────

def test_generic():
    """Generic: AGENTS.md at root (only option for these platforms)."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="generic-test", platform="generic")

        assert (target / "AGENTS.md").exists()
        content = (target / "AGENTS.md").read_text()
        assert "review" in content.lower()


def test_codex_cli():
    """Codex CLI: AGENTS.md at root."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="codex-test", platform="codex-cli")

        assert (target / "AGENTS.md").exists()


# ──────────────────────────────────────
# Zero intrusion invariant
# ──────────────────────────────────────

def test_zero_intrusion_opencode():
    """OpenCode: root only has .opencode/ and opencode.json, no AGENTS/CONSTITUTION."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="clean-test")

        root_items = _list_root(target)
        assert ".opencode" in root_items
        assert "AGENTS.md" not in root_items
        assert "CONSTITUTION.md" not in root_items

        # These should NOT exist at root
        assert not (target / "AGENTS.md").exists()
        assert not (target / "CONSTITUTION.md").exists()
        assert not (target / "GOTCHAS.md").exists()
        assert not (target / "README.md").exists()
        assert not (target / ".cpp-constitution").is_dir()

        # Everything is inside the skill dir
        skill = target / ".opencode" / "skills" / "cpp-core-review"
        assert (skill / "SKILL.md").exists()
        assert (skill / "project-config.md").exists()
        assert (skill / "references").is_dir()
        assert (skill / "config").is_dir()
        assert (skill / "GOTCHAS.md").exists()


if __name__ == "__main__":
    tests = [
        # Skill-type
        test_opencode_skill_is_self_contained,
        test_opencode_no_exceptions,
        test_claude_code,
        test_trae,
        test_codebuddy,
        # Rule-type
        test_cursor,
        test_copilot,
        test_windsurf,
        test_amazonq,
        test_lingma,
        test_void,
        # Generic
        test_generic,
        test_codex_cli,
        # Zero intrusion
        test_zero_intrusion_opencode,
    ]
    for t in tests:
        t()
        print(f"✅ {t.__name__}")
    print(f"\n🎉 All {len(tests)} tests passed!")
