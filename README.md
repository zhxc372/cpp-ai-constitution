# cpp-ai-constitution

A lightweight AI-oriented C++ engineering constitution inspired by C++ Core Guidelines.

This project is NOT a C++ tutorial.

It is an engineering constraint system designed for:
- Claude Code
- Cursor
- OpenCode
- OpenClaw
- Gemini CLI
- Codex CLI
- AI-assisted software engineering workflows

The goal is:

- reduce AI randomness
- improve consistency
- enforce ownership semantics
- stabilize architecture
- reduce review cost
- reduce hallucinated coding patterns

---

# Philosophy

Strong constraints reduce entropy.

Large software systems usually fail because of:

- ownership confusion
- inconsistent interfaces
- architecture drift
- hidden side effects
- concurrency mistakes
- style fragmentation

NOT because developers lacked clever tricks.

This repository converts parts of the C++ Core Guidelines into:
- AI-readable rules
- static analysis constraints
- engineering workflow hooks

---

# Directory Structure

```text
cpp-ai-constitution/
├── CLAUDE.md
├── README.md
├── docs/rules/
│   ├── core-subset.md
│   ├── ownership.md
│   ├── concurrency.md
│   ├── error-handling.md
│   └── forbidden-patterns.md
├── hooks/
│   ├── pre-commit.sh
│   └── ai-check.sh
├── config/
│   ├── .clang-format
│   └── .clang-tidy
└── prompts/
    ├── system-prompt.md
    └── review-prompt.md
```

---

# What Each File Does

## CLAUDE.md

The shortest and most important rule summary.

Purpose:
- loaded into AI context
- controls generation behavior
- reduces randomness

Think of it as:
- engineering constitution
- coding contract
- AI behavior limiter

This file should stay SHORT.

Recommended:
- 20~80 lines
- only high-value constraints

---

## docs/rules/

Detailed engineering rules.

Split by domain:
- ownership
- concurrency
- API design
- error handling
- forbidden patterns

Purpose:
- readable by humans
- referenced by AI
- expandable over time

These files are intentionally longer than CLAUDE.md.

---

## config/.clang-format

Automatic code formatting rules.

Purpose:
- consistent style
- lower diff noise
- easier reviews

Usage:

```bash
clang-format -i file.cpp
```

---

## config/.clang-tidy

Static analysis configuration.

Purpose:
- detect dangerous patterns
- enforce modern C++
- reduce bugs

Checks include:
- cppcoreguidelines
- modernize
- performance
- concurrency
- bugprone

Usage:

```bash
clang-tidy file.cpp --config-file=config/.clang-tidy -- -std=c++20
```

---

## hooks/

Automation scripts.

Purpose:
- automatically run checks
- reduce human review burden
- create feedback loop for AI

### pre-commit.sh

Runs:
- clang-format
- clang-tidy

### ai-check.sh

Scans all cpp/hpp files.

Usage:

```bash
chmod +x hooks/*.sh
./hooks/pre-commit.sh
```

---

## prompts/

Reusable prompts for AI agents.

### system-prompt.md

Defines:
- coding style
- generation constraints
- engineering priorities

### review-prompt.md

Defines:
- review checklist
- architecture review logic
- ownership/concurrency checks

---

# Recommended Workflow

## Step 1 — Copy Files Into Your Project

Copy:

```text
CLAUDE.md
docs/rules/
config/
hooks/
```

Into your repository root.

Example:

```text
my-project/
├── CLAUDE.md
├── src/
├── docs/
├── config/
└── hooks/
```

---

# Step 2 — Configure Your AI Coding Tool

## Claude Code

Tell Claude:

```text
Follow CLAUDE.md and docs/rules/*.md.
```

---

## Cursor

Create:

```text
.cursor/rules/cpp.mdc
```

Reference:
- CLAUDE.md
- docs/rules/

---

## OpenCode / OpenClaw

Inject:
- CLAUDE.md
- prompts/system-prompt.md

Into system context.

---

# Step 3 — Install Toolchain

Linux/macOS:

```bash
sudo apt install clang-format clang-tidy
```

or:

```bash
brew install llvm
```

Verify:

```bash
clang-format --version
clang-tidy --version
```

---

# Step 4 — Run Hooks

```bash
chmod +x hooks/*.sh
./hooks/pre-commit.sh
```

Pipeline:

```text
AI generates code
↓
clang-format
↓
clang-tidy
↓
build/tests
↓
AI fixes issues
↓
commit
```

---

# Recommended AI Workflow

## Good Pattern

```text
spec
↓
architecture
↓
CLAUDE.md
↓
small task
↓
AI generates
↓
checks
↓
review
```

---

## Bad Pattern

```text
huge vague prompt
↓
AI writes 5000 lines
↓
no checks
↓
architecture chaos
```

---

# Important Design Principle

Do NOT put entire C++ Core Guidelines into context.

Too large.
Too noisy.
Too philosophical.

Instead:

```text
CppCoreGuidelines
↓
select
↓
compress
↓
convert into engineering constraints
↓
AI-readable constitution
```

---

# Best Practice

Use THREE layers:

| Layer | Purpose |
|---|---|
| CLAUDE.md | short high-value constraints |
| docs/rules | detailed engineering rules |
| Original Guidelines | human reference only |

---

# Future Extensions

You can evolve this into:

- embedded constitution
- game-server constitution
- async/coroutine constitution
- qt constitution
- low-latency constitution
- distributed-system constitution
- agent-neutral constitution

---

# Final Thought

The future of software engineering is not:

"AI writes everything."

It is:

"Humans define constraints.
AI operates inside them."
