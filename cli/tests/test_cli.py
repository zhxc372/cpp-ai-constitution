"""Tests for cpp-constitution CLI."""

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


def test_generate_opencode_cmake():
    """OpenCode + cmake should generate skill in .opencode/skills/."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="opencode-test")

        # Core files
        assert (target / "CONSTITUTION.md").exists()
        assert (target / "AGENTS.md").exists()

        # Skill in opencode structure
        skill = target / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md"
        assert skill.exists(), f"Skill not found at {skill}"

        # Skill content includes project config
        content = skill.read_text()
        assert "c++20" in content
        assert "cmake" in content
        assert "review" in content.lower()

        # Constitution is minimal
        constitution = (target / "CONSTITUTION.md").read_text()
        assert "c++20" in constitution
        assert len(constitution.splitlines()) < 20  # should be ~10 lines


def test_generate_no_exceptions():
    """No-exceptions should be reflected in skill."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="noexc-test", exceptions=False, build="make")

        constitution = (target / "CONSTITUTION.md").read_text()
        assert "disabled" in constitution.lower()

        skill = target / ".opencode" / "skills" / "cpp-core-review" / "SKILL.md"
        content = skill.read_text()
        assert "DISABLED" in content
        assert "no throw" in content.lower()


def test_generate_xmake_cursor():
    """Cursor + xmake should generate _cursorrules + xmake.lua."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(
            tmp, name="xmake-test",
            platform="cursor", build="xmake", std="c++23"
        )

        assert (target / "xmake.lua").exists()
        content = (target / "xmake.lua").read_text()
        assert "c++23" in content

        # Cursor rules file (hidden file .cursorrules)
        assert (target / ".cursorrules").exists(), f".cursorrules not found, files: {list(target.iterdir())}"


def test_generate_generic():
    """Generic platform should put skill in skills/ directory."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="generic-test", platform="generic")

        skill = target / "skills" / "cpp-core-review" / "SKILL.md"
        assert skill.exists(), f"Skill not found at {skill}"


def test_validate_script():
    """Validate script should be generated and executable."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="val-test")

        script = target / ".cpp-constitution" / "scripts" / "validate.sh"
        assert script.exists()
        assert script.stat().st_mode & 0o111  # executable


def test_clean_layout():
    """Default layout should be clean — runtime hidden in .cpp-constitution/."""
    with tempfile.TemporaryDirectory() as tmp:
        target = _run_generate(tmp, name="clean-test")

        # These should be in root
        assert (target / "AGENTS.md").exists()
        assert (target / "CONSTITUTION.md").exists()

        # These should NOT be in root
        assert not (target / "GOTCHAS.md").exists(), "GOTCHAS.md should be hidden"
        assert not (target / "references").is_dir(), "references/ should be hidden"
        assert not (target / "config").is_dir(), "config/ should be hidden"
        assert not (target / "scripts").is_dir(), "scripts/ should be hidden"
        assert not (target / "agents").is_dir(), "agents/ should be hidden"
        assert not (target / "README.md").exists(), "README.md should not be generated"

        # These should be in .cpp-constitution/
        assert (target / ".cpp-constitution" / "GOTCHAS.md").exists()
        assert (target / ".cpp-constitution" / "references").is_dir()
        assert (target / ".cpp-constitution" / "config").is_dir()
        assert (target / ".cpp-constitution" / "scripts" / "validate.sh").exists()


if __name__ == "__main__":
    tests = [
        test_generate_opencode_cmake,
        test_generate_no_exceptions,
        test_generate_xmake_cursor,
        test_generate_generic,
        test_validate_script,
    ]
    for t in tests:
        t()
        print(f"✅ {t.__name__}")
    print("\n🎉 All tests passed!")
