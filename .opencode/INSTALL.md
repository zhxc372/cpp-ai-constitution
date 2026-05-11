# Installing C++ AI Constitution for OpenCode

## Prerequisites

- [OpenCode](https://opencode.ai) installed

## Installation

### Option A: Plugin install (recommended)

Add to `opencode.json` (global or project-level):

```json
{
  "plugin": ["cpp-ai-constitution@git+https://github.com/zhxc372/cpp-ai-constitution.git"]
}
```

Restart OpenCode. The plugin registers the `cpp-core-review` skill.

Verify: ask your agent "Tell me about your C++ review skills"

### Option B: CLI install

```bash
pipx install git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli
cd /your/cpp/project
cpp-constitution install . --platform opencode
```

This generates skill files directly in `.opencode/skills/cpp-core-review/`.

## Usage

Ask your agent to review C++ code:

```
review src/main.cpp
```

The skill auto-triggers on C++ files. It will:
1. Run static analysis tools (clang-tidy, cppcheck, etc.)
2. Review by priority (UB → Ownership → RAII → Concurrency → ...)
3. Output findings with severity markers (🔴🟠🟡🔵⚪)

## Updating

For plugin installs, restart OpenCode. If changes don't appear, clear the package cache or reinstall.

For CLI installs:
```bash
pipx upgrade cpp-constitution
cpp-constitution install . --platform opencode
```

## Troubleshooting

### Plugin not loading

1. Check `opencode.json` has the correct plugin line
2. Run: `opencode run --print-logs "hello" 2>&1 | grep -i constitution`
3. Make sure you're on a recent OpenCode version

### Skill not triggering

Make sure your project has C++ files (`.cpp`, `.hpp`, `.h`, `.cc`, `.cxx`).
The skill triggers on review/audit/inspect keywords.
