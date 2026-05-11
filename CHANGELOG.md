# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-05-11

### Changed
- **BREAKING**: `init` renamed to `install` (init kept as alias)
- Superpowers model: zero root-level intrusion — all files in skill directory
- Skill-type platforms: SKILL.md + project-config.md + references/ + config/ + GOTCHAS.md inside platform skill dir
- Rule-type platforms: self-contained single file, no external references
- Static analysis tool matrix: clang-tidy → cppcheck → clazy → iwyu (was clang-tidy only)
- Clear degradation message when no tools available: "AI-only review — lower confidence"
- README rewritten (EN + CN): 13 platforms, tool matrix, zero intrusion, two install paths
- Branch strategy: master = stable, dev = development

### Added
- Platform adapters for Trae, CodeBuddy, Gemini CLI, Amazon Q, 通义灵码, Void (6 new)
- Total: 13 platforms (5 Skill-type, 6 Rule-type, 2 Generic)
- YAML frontmatter on SKILL.md (name + description)
- Compiler warning baseline suggestions in Tool First section
- `.claude-plugin/plugin.json` — Claude Code marketplace registration
- `.codex-plugin/plugin.json` — Codex CLI marketplace registration
- `.cursor-plugin/plugin.json` — Cursor marketplace registration
- `.opencode/INSTALL.md` — OpenCode install guide (plugin + CLI)
- GEMINI.md — Gemini CLI entry point
- 14 tests (up from 8) covering all 13 platforms + zero intrusion invariant
- `skills/` directory removed (single skill, no multi-skill layout needed)

## [0.1.1] - 2026-05-11

### Added
- Two-track adapter strategy: Skill-type vs Rule-type
- 13 platform adapters total
- `test_generate_trae`, `test_generate_copilot`, `test_clean_layout` tests
- Rule-type Jinja2 templates with inlined review priority, ownership, modernization
- Build system templates: cmake, xmake, make, meson, autotools, none

### Fixed
- xmake template: removed `add_headerfiles()`, only `add_includedirs("include")`
- Root directory layout: runtime files in `.cpp-constitution/` hidden directory

## [0.1.0] - 2026-05-11

### Added
- Initial CLI: `cpp-constitution init .`
- Interactive prompts for platform, C++ standard, build system, exceptions
- Non-interactive mode with `--no-interact`
- pipx install from git subdirectory
- Self-contained runtime assets bundled in wheel
- MANIFEST.in for reliable package data inclusion
- Custom PackageLoader for template resolution
- Flattened build templates for packaging reliability
- Phase 0 starter template (`templates/phase0-starter.md`)
- 8 tests covering core generation scenarios
- WSL + OpenCode full pipeline verified end-to-end

## [0.7.1-freeze] - 2026-05-10

### Note
Frozen baseline. Only P0/P1 fixes accepted. New features → ROADMAP.

### Added
- PROJECT_CONSTITUTION.md, DECISION_RIGHTS.md, ADAPTER_POLICY.md, RULE_ADMISSION.md
- Tiered evals: L1 (keyword sim), L2 (adapter consistency), L3 (real agent smoke)
- Adapter headers on all 9 adapter files
- Governance layer for interview-bible and cpp-ai-constitution

## [0.7.0] - 2026-05-10

### Added
- Merged `feature/scriptification-p2-p5` into master
- P2-P5 automation scripts
- CI validation workflow

---

[0.1.2]: https://github.com/zhxc372/cpp-ai-constitution/releases/tag/v0.1.2
[0.1.1]: https://github.com/zhxc372/cpp-ai-constitution/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/zhxc372/cpp-ai-constitution/releases/tag/v0.1.0
[0.7.1-freeze]: https://github.com/zhxc372/cpp-ai-constitution/releases/tag/v0.7.1-freeze
[0.7.0]: https://github.com/zhxc372/cpp-ai-constitution/releases/tag/v0.7.0
