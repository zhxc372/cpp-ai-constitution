<!--
AUTOMATICALLY GENERATED FILE - DO NOT EDIT DIRECTLY
Edit project.yaml and templates/README.md.j2 instead.
Run scripts/build_readme.py to regenerate.
-->
# cpp-ai-constitution

**English** | [中文](README_CN.md)

Tool-agnostic C++ constraint system for AI coding agents


> ⚠️ 本项目受 [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md) 最高约束。
> 所有适配层必须遵守 [ADAPTER_POLICY.md](ADAPTER_POLICY.md)。
> 规则准入遵循 [RULE_ADMISSION.md](RULE_ADMISSION.md)。

Inspired by C++ Core Guidelines and [Perplexity's Skill design methodology](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity).




## What This Is Not

- A C++ tutorial
- A compressed copy of C++ Core Guidelines
- A "modernize everything" enforcement tool
- Something you load once and forget

## Compatibility

See [ADAPTER_MATRIX.md](ADAPTER_MATRIX.md) for full details.

| Platform | Support Level | Auto-load | Verified |
|----------|--------------|------------|----------|
| OpenCode | Officially Supported | ✅ | ✅ Structure Verified |
| Claude Code | Supported | ✅ | ✅ Structure Verified |
| OpenClaw | Supported | ✅ | ✅ Structure Verified |
| Cursor | Recipe Only | ⚠️ Manual | Manual only |
| Codex CLI | Recipe Only | ⚠️ Manual | Manual only |
| Gemini CLI | Recipe Only | ⚠️ Manual | Manual only |
| Any LLM | Level 1: Manual Copy | ❌ | Not applicable |

### Support Level Definitions

- **Officially Supported**: Has entry files, auto-load, eval tests, and manual verification
- **Supported**: Has entry files and sync verification
- **Recipe Only**: Has entry files but no automated verification
- **Level 1**: Manual copy, no tool integration


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

## Design Philosophy


### Concise is key
Default assumption is AI is already very smart. Only add context AI doesn't already have.

### Progressive loading
Only load relevant rules when needed, not everything upfront to save tokens.

### Script first, AI second
Deterministic tasks (static analysis, format checks) handled by scripts, AI only does judgment work.

### Tool backed
Prefer static analysis tool results over subjective AI opinions.


> **Strong constraints reduce entropy.**

This project converts C++ Core Guidelines into:
- AI-readable rules (not human documentation)
- Static analysis constraints (not style opinions)
- Engineering workflow hooks (not manual checklists)

Every rule must justify its token cost. If the model already knows it, delete it.

## Skills

| Skill ID | Name | Purpose | When to Use |
|----------|------|---------|-------------|
| `cpp-core-review` | C++ Core Review | Code review, safety audit, AI output validation | Reviewing any non-trivial C++ code |
| `cpp-modernize` | C++ Modernizer | C++ migration, systematic refactoring and modernization | Upgrading from older standards (C++98/C++11) to modern C++ |
| `cpp-debug-audit` | C++ Debug & Audit | Crash debugging, memory error detection, sanitizer analysis | Debugging undefined behavior, leaks, data races or crashes |


## Agent Roles

| Agent ID | Name | Role | How to Invoke |
|----------|------|------|---------------|
| `cpp-reviewer` | C++ Strict Reviewer | Read-only, strict C++ code reviewer | `@cpp-reviewer review src/foo.cpp` |
| `cpp-refactor-planner` | C++ Refactor Planner | Creates safe, step-by-step modernization plans | `@cpp-refactor-planner plan modernization` |
| `cpp-safety-auditor` | C++ Safety Auditor | Systematic safety audit using sanitizers and static analysis | `@cpp-safety-auditor audit src/` |


## Progressive Loading

The root `SKILL.md` (~1,500 tokens) is the only thing loaded by default. Everything else loads on demand:

| Condition | What loads |
|---|---|
| Reviewing ownership/lifetime code | `references/lifetime.md` |
| Multi-threaded code | `references/concurrency.md` |
| Custom error handling | `references/error-handling.md` |
| Template metaprogramming | `references/templates.md` |
| Performance-critical paths | `references/performance.md` |
| Full audit requested | All relevant `references/*.md` |

## Token Budget

| Layer | Content | Cost |
|---|---|---|
| Index | Name + description for skill routing | ~50 tokens |
| Load | Core SKILL.md rules | ~1,500 tokens |
| Runtime | Specific reference docs, script results | ~0-8,000 tokens (loaded on demand only) |


## clang-tidy Profiles

Three profiles for different project stages:

| Profile | Use Case | Command |
|---|---|---|
| `minimal` | CI baseline, low false positive rate | `--config-file=config/clang-tidy.minimal.yml` |
| `migration` | Legacy project migration | `--config-file=config/clang-tidy.migration.yml` |
| `strict` | New projects or strict safety reviews | `--config-file=config/clang-tidy.strict.yml` |


## Scripts

Run deterministic tasks without burning AI tokens:

```bash
# Detect C++ project structure and build system
python3 scripts/detect_cpp_project.py
# Locate or generate compile_commands.json for static analysis
python3 scripts/find_compile_commands.py
# Run clang-tidy with summary output for AI consumption
python3 scripts/run_clang_tidy.py
# Sync canonical skill files across multiple platform directories
python3 scripts/sync_skill_targets.py
# Validate repository structure, frontmatter, configs, and references
python3 scripts/validate_repo.py
# Run skill routing evals
## Eval Levels:
##   L1 (run_evals.py): keyword simulation — smoke test for rule definitions
##   L2 (run_evals_l2.py): adapter file consistency (structure + header + sync)
##   L3 (run_evals_l3.py): real agent smoke eval (requires live agent)
## L1 is NOT real platform routing verification. README must not claim otherwise.
python3 scripts/run_evals.py       # L1: keyword simulation
python3 scripts/run_evals_l2.py    # L2: adapter consistency
python3 scripts/run_evals_l3.py    # L3: real agent (manual mode if no agent)
# Generate GOTCHAS.md from structured gotchas.yaml
python3 scripts/build_gotchas_md.py

```

## Review Output Format

Findings categorized by severity:

- **Critical** : Undefined behavior, memory corruption, data races, dangling references
- **Major** : Fragile APIs, inconsistent error handling, hidden side effects
- **Minor** : Readability, naming, style, local simplifications
- **Do Not Change** : Items that should remain (ABI, legacy, performance constraints)

## Directory Structure

```text
cpp-ai-constitution/
├── AGENTS.md                       # Agent-neutral main entry (read this first)
├── SKILL.md                        # Root skill: routing, priorities, constitution
├── CLAUDE.md                       # Compact rule summary for Claude Code
├── GOTCHAS.md                      # AI failure patterns in C++ (highest value content)
├── opencode.json.example           # OpenCode configuration template
├── project.yaml                    # Project metadata (for README generation)
├── data/
│   └── gotchas.yaml                # Structured gotchas for automated generation
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
├── .opencode/skills/               # OpenCode skills (3)
│   ├── cpp-core-review/SKILL.md
│   ├── cpp-modernize/SKILL.md
│   ├── cpp-debug-audit/SKILL.md
├── .opencode/agents/               # OpenCode agents (3)
│   ├── cpp-reviewer.md
│   ├── cpp-refactor-planner.md
│   ├── cpp-safety-auditor.md
├── .claude/skills/                 # Claude Code compatibility
├── .agents/skills/                 # Generic agent compatibility
├── scripts/                        # Automation (7 scripts)
├── assets/                         # Templates
├── hooks/                          # Git hooks
├── config/                         # Tool configurations
├── prompts/                        # Reusable AI prompts
├── evals/                          # Skill routing tests
├── templates/                      # Jinja2 templates for documentation generation
├── .github/workflows/validate.yml  # CI validation
└── LICENSE
```

## Credits


- C++ Core Guidelines by Bjarne Stroustrup, Herb Sutter, et al.

- Perplexity Research - Designing, Refining, and Maintaining Agent Skills

- OpenClaw community for skill best practices


## License


MIT-0
