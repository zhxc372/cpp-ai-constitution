# cpp-ai-constitution

**English** | [中文](README_CN.md)

Source-of-truth C++ rule system for constraining AI coding agents.

> **User-facing installer:** [cpp-constitution](https://github.com/zhxc372/cpp-constitution)
> **Source of truth:** this repository

---

## Quick Start

### Recommended: use the CLI

```bash
pipx install git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli
cd /your/cpp/project
cpp-constitution init .
```

Then ask your AI agent:
```
review src/main.cpp
```

### One-shot run (no install)

```bash
uvx --from git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli cpp-constitution init .
```

### Manual install (advanced)

```bash
cp AGENTS.md /your-project/
cp -r references/ /your-project/
cp -r config/ /your-project/
cp GOTCHAS.md /your-project/
```

---

## Repository Roles

| Repository | Role |
|------------|------|
| `cpp-ai-constitution` | Source of truth: rules, skills, references, adapters, evals, CLI source |
| `cpp-constitution` | Distribution mirror: pipx package, command entry point |

Do not edit generated files in `cpp-constitution` directly. All changes start here.

---

## What This Provides

- `cpp-core-review` skill — safety-first C++ code review
- C++ ownership and lifetime rules
- clang-tidy profiles (minimal / strict / migration)
- Runtime references (lifetime, RAII, concurrency, templates, etc.)
- Known AI failure patterns (GOTCHAS.md)
- Platform adapters (OpenCode, Claude Code, Cursor, Codex CLI, Gemini CLI)
- Evals and verification scripts
- Source for the `cpp-constitution` pipx CLI

---

## Design Philosophy

1. **Tool First** — clang-tidy and compiler warnings run before subjective review
2. **Progressive Loading** — CONSTITUTION.md is small; detailed rules load on demand
3. **Safety Before Style** — UB, lifetime, ownership, RAII come before naming or formatting
4. **One Source of Truth** — distribution is generated from this repository

---

## Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `cpp-core-review` | C++ review and safety audit | `review src/foo.cpp` |
| `cpp-debug-audit` | crash / sanitizer / UB audit | `debug this crash` |
| `cpp-refactor-planner` | safe refactor planning | `refactor this module` |

---

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| OpenCode | ✅ Verified | Auto-trigger tested, Chinese output supported |
| Claude Code | ✅ Supported | Skill directory generated |
| OpenClaw | ✅ Supported | Used for development |
| Cursor | Recipe | Rule file generated |
| Codex CLI | Recipe | Adapter generated |
| Gemini CLI | Recipe | Adapter generated |

---

## Distribution Strategy

| Command | Status | Purpose |
|---------|--------|---------|
| `pipx install cpp-constitution` | **Primary** | Persistent install |
| `uvx cpp-constitution init .` | Supported | One-shot execution |
| `npx cpp-constitution init .` | Planned | JS ecosystem thin wrapper |

`npx` will be a thin wrapper that delegates to `uvx` or `pipx`. It will NOT duplicate templates, references, or rule logic.

---

## Architecture

```
cpp-ai-constitution/
├── SKILL.md                    # Core review skill
├── AGENTS.md                   # Universal AI entry point
├── GOTCHAS.md                  # Known AI failure patterns
├── references/                 # Detailed C++ rules (9 files)
├── config/                     # clang-tidy profiles
├── scripts/                    # Validation and build scripts
├── evals/                      # Evaluation test cases
├── templates/                  # Phase 0 starter template
├── .opencode/                  # OpenCode adapter
├── .claude/                    # Claude Code adapter
├── cli/                        # cpp-constitution pipx CLI source
│   ├── cpp_constitution/       # Python package
│   ├── templates/              # Jinja2 templates (skill, constitution, etc.)
│   ├── tests/                  # 5 tests
│   └── MANIFEST.in             # Package data inclusion
└── PROJECT_CONSTITUTION.md     # Highest constraint
```

---

## What This Is Not

- Not a C++ tutorial
- Not a compressed copy of C++ Core Guidelines
- Not a "modernize everything" enforcement tool
- Not a replacement for clang-tidy, sanitizers, or tests

Every rule must justify its token cost.

---

## Verification

```bash
# CLI tests
cd cli && python3 tests/test_cli.py

# Repo validation
python3 scripts/validate_repo.py

# Generate a test project
cpp-constitution init /tmp/demo --platform opencode --std c++20 --build xmake --no-interact

# Verify runtime files
test -f /tmp/demo/config/clang-tidy.minimal.yml
test -f /tmp/demo/references/lifetime.md
test -f /tmp/demo/GOTCHAS.md
```

---

## License

MIT-0
