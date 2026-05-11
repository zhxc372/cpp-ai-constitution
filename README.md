# cpp-ai-constitution

**English** | [中文](README_CN.md)

C++ review skill for AI coding agents. Install once, get safety-first code review everywhere.

Inspired by [superpowers](https://github.com/obra/superpowers) — markdown skills, thin adapters, no runtime.

---

## Install

```bash
pipx install git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli
cd /your/cpp/project
cpp-constitution install .
```

That's it. Ask your AI agent:
```
review src/main.cpp
```

### One-shot (no install)

```bash
uvx --from git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli cpp-constitution install .
```

---

## What It Does

**Zero intrusion.** `cpp-constitution install .` puts everything inside the platform's skill directory:

```
your-project/
├── .opencode/skills/cpp-core-review/    # ← all files here
│   ├── SKILL.md                         # review logic
│   ├── project-config.md                # C++ version, build, exceptions
│   ├── references/                      # detailed rules (9 files)
│   ├── config/                          # clang-tidy profiles
│   └── GOTCHAS.md                       # known AI failure patterns
└── opencode.json                        # platform config (OpenCode only)
```

No `AGENTS.md` at root. No `CONSTITUTION.md` at root. No pollution.

---

## Platform Support

| Platform | Type | Install Target |
|----------|------|---------------|
| **OpenCode** | Skill | `.opencode/skills/cpp-core-review/` |
| **Claude Code** | Skill | `.claude/skills/cpp-core-review/` |
| **Trae** | Skill | `.trae/skills/cpp-core-review/` |
| **CodeBuddy** | Skill | `.codebuddy/skills/cpp-core-review/` |
| **Gemini CLI** | Skill | `.gemini/skills/cpp-core-review/` |
| **Cursor** | Rule | `.cursor/rules/cpp-review.mdc` |
| **Windsurf** | Rule | `.windsurfrules` |
| **GitHub Copilot** | Rule | `.github/copilot-instructions.md` |
| **Amazon Q** | Rule | `.amazonq/rules/cpp-review.md` |
| **通义灵码** | Rule | `.lingma/rules/cpp-review.md` |
| **Void** | Rule | `.void/rules/cpp-review.md` |
| **Codex CLI** | Generic | `AGENTS.md` |
| **Generic** | Generic | `AGENTS.md` |

**Skill-type**: SKILL.md + references loaded on demand (richer, structured).
**Rule-type**: single self-contained file (works without skill loading).
**Generic**: AGENTS.md at root (only for platforms without skill/rule support).

---

## Tool First

The skill encourages AI agents to run static analysis before subjective review:

| Tool | What it catches | Command |
|------|----------------|---------|
| **clang-tidy** | Bug-prone patterns, modernization, readability | `clang-tidy -p build <file>` |
| **cppcheck** | Buffer overflows, leaks, undefined behavior | `cppcheck --enable=all <file>` |
| **clazy** | Qt-specific anti-patterns | `clazy -p build <file>` |
| **include-what-you-use** | Unnecessary includes, forward decls | `iwyu -p build <file>` |

No tools installed? The skill tells the user: *"AI-only review — lower confidence on mechanical issues. Recommend installing clang-tidy or cppcheck."*

---

## Design Philosophy

1. **Tool First** — static analysis before eyeballing code
2. **Safety Before Style** — UB, lifetime, ownership > naming, formatting
3. **Progressive Loading** — SKILL.md stays short; detailed rules load on demand
4. **Zero Intrusion** — all files in skill directory, nothing at project root
5. **One Source of Truth** — distribution mirrors generated from this repo

---

## Architecture

```
cpp-ai-constitution/                  # this repo
├── SKILL.md                          # core review skill definition
├── AGENTS.md                         # universal AI entry point (for this repo itself)
├── CLAUDE.md                         # Claude Code entry point (for this repo itself)
├── GOTCHAS.md                        # known AI failure patterns
├── references/                       # detailed C++ rules (9 files)
├── config/                           # clang-tidy profiles
├── scripts/                          # validation and build scripts
├── evals/                            # evaluation test cases
├── templates/                        # Phase 0 starter template
├── .opencode/                        # OpenCode adapter (for this repo itself)
├── .claude/                          # Claude Code adapter (for this repo itself)
└── cli/                              # cpp-constitution CLI source
    ├── cpp_constitution/
    │   ├── cli.py                    # entry: install command
    │   ├── generator.py              # file generation engine
    │   ├── prompts.py                # interactive prompts
    │   ├── runtime/                  # bundled assets (references, config, gotchas)
    │   └── templates/                # Jinja2 templates
    │       ├── skill.md.j2           # Skill-type SKILL.md template
    │       ├── agents.md.j2          # Generic AGENTS.md template
    │       ├── build/                # build system templates (cmake, xmake, etc.)
    │       └── platforms/            # platform-specific templates
    │           ├── opencode/         # OpenCode skill template
    │           ├── claude_code/      # Claude Code skill template
    │           ├── cursor/           # Cursor rule template
    │           ├── copilot/          # Copilot rule template
    │           └── ...               # 13 platforms total
    ├── tests/test_cli.py             # 14 tests
    ├── MANIFEST.in                   # package data inclusion
    └── pyproject.toml
```

---

## What This Is Not

- Not a C++ tutorial
- Not a compressed copy of C++ Core Guidelines
- Not a "modernize everything" enforcement tool
- Not a replacement for clang-tidy, sanitizers, or tests
- Not an agent framework

Every rule must justify its token cost.

---

## Verification

```bash
# CLI tests
cd cli && python3 tests/test_cli.py

# Repo validation
python3 scripts/validate_repo.py

# Generate a test project
cpp-constitution install /tmp/demo --platform opencode --std c++20 --build xmake --no-interact

# Verify zero intrusion
ls /tmp/demo/  # should only show .opencode/ (and opencode.json for OpenCode)
```

---

## Distribution

| Repository | Role |
|------------|------|
| `cpp-ai-constitution` | Source of truth: rules, skills, CLI source |
| `cpp-constitution` | Distribution mirror (synced automatically) |

| Channel | Status |
|---------|--------|
| `pipx install git+...#subdirectory=cli` | ✅ Primary |
| `uvx --from git+...#subdirectory=cli` | ✅ Supported |
| PyPI (`pip install cpp-constitution`) | Planned |
| ClawHub skill | Planned (after May 23) |
| `npx cpp-constitution` | Planned |

---

## License

MIT-0
