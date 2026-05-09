# cpp-ai-constitution

**English** | [中文](README_CN.md)

A tool-agnostic C++ constraint system for AI coding agents.

Not a compressed textbook — a judgment engine.

Inspired by C++ Core Guidelines and [Perplexity's Skill design methodology](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity).

**OpenCode-first, Agent-neutral, OpenClaw-compatible.**

## Compatibility

- OpenCode (primary)
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI
- OpenClaw
- Any agent that supports rules/skills

## What This Is

An AI-readable engineering constraint system that helps agents:

- Identify high-impact C++ mistakes (not recite C++ trivia)
- Classify ownership before changing pointer types
- Run mechanical checks before subjective review
- Separate safety fixes from style rewrites
- Know when exceptions to "modern C++" rules apply

## What This Is Not

- A C++ tutorial
- A compressed copy of C++ Core Guidelines
- A "modernize everything" enforcement tool
- Something you load once and forget

## Philosophy

From [Perplexity's Skill research](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity):

> If the implementation is easy to explain, the model already knows it. Delete it.
> Gotchas ARE the special cases. They're the highest-value content.

This project follows those principles:

- Skip what models already know
- Focus on AI failure patterns (gotchas)
- Progressive loading (not everything at once)
- Tool-backed checks over subjective review

## Directory Structure

```text
cpp-ai-constitution/
├── SKILL.md                    # Root: routing, priorities, constitution
├── CLAUDE.md                   # Compact rule summary for Claude Code
├── GOTCHAS.md                  # AI failure patterns in C++
├── references/                 # Detailed rules (loaded conditionally)
│   ├── rule-map.md             # Which rules apply when
│   ├── lifetime.md             # Ownership and lifetime hazards
│   ├── resource-management.md  # RAII patterns and traps
│   ├── concurrency.md          # Thread safety rules
│   ├── error-handling.md       # Exception and error strategy
│   ├── interfaces.md           # API design rules
│   ├── classes.md              # Class design rules
│   ├── templates.md            # Template and concept rules
│   └── performance.md          # Performance review checklist
├── scripts/                    # Automation
│   ├── detect_cpp_project.py   # Identify C++ project structure
│   ├── find_compile_commands.py # Locate or generate compile_commands.json
│   └── run_clang_tidy.py       # Run clang-tidy with summary
├── assets/                     # Templates
│   ├── review-report-template.md
│   ├── refactor-plan-template.md
│   └── risk-levels.md
├── hooks/                      # Git hooks
│   ├── pre-commit.sh           # Format + static analysis
│   └── ai-check.sh             # Pattern-based issue scanner
├── config/                     # Tool configs
│   ├── .clang-format
│   └── .clang-tidy
├── prompts/                    # AI prompts
│   ├── system-prompt.md
│   └── review-prompt.md
└── evals/                      # Skill routing tests
    ├── positive-load-cases.md
    ├── negative-load-cases.md
    ├── adjacent-skill-confusions.md
    └── hero-queries.md
```

## Quick Start

### Copy into your project

```bash
cp -r SKILL.md CLAUDE.md GOTCHAS.md references/ scripts/ assets/ hooks/ config/ prompts/ /your/project/
```

### Configure your AI tool

**Claude Code**: Point to `CLAUDE.md` + `SKILL.md`.

**Cursor**: Create `.cursor/rules/cpp.mdc` referencing `SKILL.md` and `references/`.

**OpenClaw**: Inject `SKILL.md` + `prompts/system-prompt.md` into system context.

### Run tooling

```bash
python3 scripts/detect_cpp_project.py
python3 scripts/find_compile_commands.py
python3 scripts/run_clang_tidy.py
```

## Progressive Loading

Not all rules apply to all projects. `SKILL.md` instructs the agent to conditionally load:

| Condition | Load |
|---|---|
| Multi-threaded code | `references/concurrency.md` |
| Custom error handling | `references/error-handling.md` |
| Template metaprogramming | `references/templates.md` |
| Performance-critical paths | `references/performance.md` |
| Ownership questions | `references/lifetime.md` |

## Token Budget

| Layer | Content | Approximate Cost |
|---|---|---|
| Index | name + description | ~50 tokens |
| Load | SKILL.md body | ~1,500 tokens |
| Runtime | references, scripts, assets | ~0-8,000 tokens (on demand) |

## Integration Modes

### OpenCode (recommended)

```bash
cp AGENTS.md /your/project/AGENTS.md
cp opencode.json.example /your/project/opencode.json
cp -r .opencode/ /your/project/.opencode/
```

### Claude Code

```bash
cp CLAUDE.md /your/project/CLAUDE.md
cp -r .claude/skills/ /your/project/.claude/skills/
```

### Generic AI Coding

Copy `AGENTS.md` and selected `references/*.md` into your agent context.

### OpenClaw

Use `SKILL.md` and rule files as reusable project skills.

## Multiple Skills

This project includes three specialized skills:

| Skill | Purpose |
|---|---|
| `cpp-core-review` | Code review, safety audit, AI output validation |
| `cpp-modernize` | C++ migration, systematic modernization |
| `cpp-debug-audit` | Crash debugging, memory errors, sanitizer-based auditing |

And three agent roles:

| Agent | Role |
|---|---|
| `cpp-reviewer` | Read-only strict reviewer |
| `cpp-refactor-planner` | Creates safe modernization plans |
| `cpp-safety-auditor` | Systematic safety audit with sanitizers |

## Sync Script

When maintaining multi-platform compatibility:

```bash
python3 scripts/sync_skill_targets.py
```

Syncs canonical `SKILL.md` to `.opencode/`, `.claude/`, `.agents/` directories.

## clang-tidy Profiles

| Profile | Use Case |
|---|---|
| `clang-tidy.minimal.yml` | CI baseline, low false-positive rate |
| `clang-tidy.migration.yml` | Legacy project migration |
| `clang-tidy.strict.yml` | New projects or strict review |

```bash
clang-tidy file.cpp --config-file=config/clang-tidy.minimal.yml -- -std=c++20
```

## Credits

- C++ Core Guidelines by Bjarne Stroustrup, Herb Sutter, et al.
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
