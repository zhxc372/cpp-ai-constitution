# cpp-ai-constitution

**English** | [中文](README_CN.md)

A tool-agnostic C++ constraint system for AI coding agents. Not a compressed textbook — a judgment engine.

**OpenCode-first, Agent-neutral, OpenClaw-compatible.**

> ⚠️ 本项目受 [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md) 最高约束。
> 所有适配层必须遵守 [ADAPTER_POLICY.md](ADAPTER_POLICY.md)。
> 规则准入遵循 [RULE_ADMISSION.md](RULE_ADMISSION.md)。

Inspired by C++ Core Guidelines and [Perplexity's Skill design methodology](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity).

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

## Compatibility

- OpenCode (primary)
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI
- OpenClaw
- Any agent that supports rules/skills

## Quick Start

### 1. OpenCode (recommended)

```bash
# Copy the constitution into your C++ project
cp AGENTS.md /your-project/AGENTS.md
cp opencode.json.example /your-project/opencode.json
cp -r .opencode/ /your-project/.opencode/
cp -r references/ /your-project/references/
cp -r scripts/ /your-project/scripts/
cp -r config/ /your-project/config/
cp -r assets/ /your-project/assets/
cp GOTCHAS.md /your-project/GOTCHAS.md
```

Then in OpenCode, the skills auto-load when you review C++ code:

```
@cpp-reviewer review src/foo.cpp
@cpp-safety-auditor audit src/
```

### 2. Claude Code

```bash
cp CLAUDE.md /your-project/CLAUDE.md
cp -r .claude/skills/ /your-project/.claude/skills/
cp -r references/ /your-project/references/
cp -r scripts/ /your-project/scripts/
cp -r config/ /your-project/config/
```

Tell Claude: "Follow CLAUDE.md and references/*.md."

### 3. OpenClaw

```bash
clawhub install cpp-ai-constitution
```

Or copy `SKILL.md` and rule files into your workspace skills directory.

### 4. Generic AI Coding

Copy `AGENTS.md` and selected `references/*.md` into your agent context. Load only what you need.

### 5. Cursor

Create `.cursor/rules/cpp.mdc` referencing `AGENTS.md` and `references/`.

## Directory Structure

```text
cpp-ai-constitution/
├── AGENTS.md                       # Agent-neutral main entry (read this first)
├── SKILL.md                        # Root skill: routing, priorities, constitution
├── CLAUDE.md                       # Compact rule summary for Claude Code
├── GOTCHAS.md                      # AI failure patterns in C++ (highest value content)
├── opencode.json.example           # OpenCode configuration template
│
├── references/                     # Detailed rules (loaded conditionally)
│   ├── rule-map.md                 # Which rules apply when
│   ├── lifetime.md                 # Ownership and lifetime hazards
│   ├── resource-management.md      # RAII patterns and traps
│   ├── concurrency.md              # Thread safety rules
│   ├── error-handling.md           # Exception and error strategy
│   ├── interfaces.md               # API design rules
│   ├── classes.md                  # Class design rules
│   ├── templates.md                # Template and concept rules
│   └── performance.md              # Performance review checklist
│
├── .opencode/skills/               # OpenCode skills (3)
│   ├── cpp-core-review/SKILL.md    # Code review, safety audit
│   ├── cpp-modernize/SKILL.md      # C++ migration, modernization
│   └── cpp-debug-audit/SKILL.md    # Crash debugging, sanitizer audit
│
├── .opencode/agents/               # OpenCode agents (3)
│   ├── cpp-reviewer.md             # Read-only strict reviewer
│   ├── cpp-refactor-planner.md     # Safe modernization planner
│   └── cpp-safety-auditor.md       # Systematic safety audit
│
├── scripts/                        # Automation (0 token for deterministic tasks)
│   ├── detect_cpp_project.py       # Identify C++ project structure
│   ├── find_compile_commands.py    # Locate or generate compile_commands.json
│   ├── run_clang_tidy.py           # Run clang-tidy with summary output
│   ├── sync_skill_targets.py       # Sync skills across platforms
│   └── validate_repo.py            # Validate repo structure and configs
│
├── assets/                         # Templates
│   ├── review-report-template.md   # Structured review output
│   ├── refactor-plan-template.md   # Safe refactoring plan
│   └── risk-levels.md              # Critical/High/Medium/Low definitions
│
├── config/                         # Tool configurations
│   ├── .clang-format               # Code formatting rules
│   ├── clang-tidy.minimal.yml      # CI baseline (low false-positive)
│   ├── clang-tidy.migration.yml    # Legacy project migration
│   └── clang-tidy.strict.yml       # New projects, strict review
│
├── hooks/                          # Git hooks
│   ├── pre-commit.sh               # Format + static analysis
│   └── ai-check.sh                 # Pattern-based issue scanner
│
├── prompts/                        # Reusable AI prompts
│   ├── system-prompt.md            # Agent system prompt
│   └── review-prompt.md            # Code review checklist
│
├── evals/                          # Skill routing tests
│   ├── positive-load-cases.md      # Should load (10 cases)
│   ├── negative-load-cases.md      # Should NOT load (10 cases)
│   ├── adjacent-skill-confusions.md # Near-miss routing (10 cases)
│   └── hero-queries.md             # Key validation scenarios (8 cases)
│
├── .claude/skills/                 # Claude Code compatibility
├── .agents/skills/                 # Generic agent compatibility
└── .github/workflows/validate.yml  # CI validation
```

## How It Works

### Progressive Loading

The root `SKILL.md` (~1,500 tokens) is the only thing loaded by default. Everything else loads on demand:

| Condition | What loads |
|---|---|
| Reviewing ownership/lifetime code | `references/lifetime.md` |
| Multi-threaded code | `references/concurrency.md` |
| Custom error handling | `references/error-handling.md` |
| Template metaprogramming | `references/templates.md` |
| Performance-critical paths | `references/performance.md` |
| Full audit requested | All relevant `references/*.md` |

### Token Budget

| Layer | Content | Cost |
|---|---|---|
| Index | name + description | ~50 tokens |
| Load | SKILL.md body | ~1,500 tokens |
| Runtime | references, scripts, assets | ~0-8,000 tokens (on demand) |

### Multiple Skills

Three specialized skills for different tasks:

| Skill | Purpose | When to use |
|---|---|---|
| `cpp-core-review` | Code review, safety audit | Reviewing any non-trivial C++ |
| `cpp-modernize` | C++ migration, refactoring | Upgrading from C++98/11 to modern |
| `cpp-debug-audit` | Crash debugging, memory errors | Debugging UB, leaks, data races |

### Agent Roles

| Agent | What it does | How to invoke |
|---|---|---|
| `cpp-reviewer` | Read-only strict review | `@cpp-reviewer review src/foo.cpp` |
| `cpp-refactor-planner` | Create safe modernization plan | `@cpp-refactor-planner plan modernization` |
| `cpp-safety-auditor` | Systematic safety audit | `@cpp-safety-auditor audit src/` |

## clang-tidy Profiles

Three profiles for different project stages:

| Profile | Use Case | Command |
|---|---|---|
| `minimal` | CI baseline, low false-positive | `--config-file=config/clang-tidy.minimal.yml` |
| `migration` | Legacy project migration | `--config-file=config/clang-tidy.migration.yml` |
| `strict` | New projects or strict review | `--config-file=config/clang-tidy.strict.yml` |

## Scripts

Run deterministic tasks without burning AI tokens:

```bash
# Identify project structure
python3 scripts/detect_cpp_project.py

# Find or generate compile_commands.json
python3 scripts/find_compile_commands.py

# Run clang-tidy with AI-friendly summary
python3 scripts/run_clang_tidy.py

# Sync skills across platforms
python3 scripts/sync_skill_targets.py

# Validate repo integrity
python3 scripts/validate_repo.py
```

## Review Output Format

Findings categorized by severity:

- **Critical**: Undefined behavior, memory corruption, data races, dangling references
- **Major**: Fragile APIs, inconsistent error handling, hidden side effects
- **Minor**: Readability, naming, style, local simplifications
- **Do Not Change**: Items that should remain (ABI, legacy, performance constraints)

## Philosophy

> Strong constraints reduce entropy.

This project converts C++ Core Guidelines into:
- AI-readable rules (not human documentation)
- Static analysis constraints (not style opinions)
- Engineering workflow hooks (not manual checklists)

Every rule must justify its token cost. If the model already knows it, delete it.

## Credits

- C++ Core Guidelines — Bjarne Stroustrup, Herb Sutter, et al.
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
