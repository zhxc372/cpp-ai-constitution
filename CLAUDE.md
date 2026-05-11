---
name: cpp-ai-constitution
description: Safety-first C++ code review skill with Tool First methodology, ownership classification, and progressive rule loading
---

# C++ AI Constitution

This project provides a C++ review skill (`cpp-core-review`) for AI coding agents.

## Quick Start

### Plugin install (Claude Code)
```
/install-plugin cpp-ai-constitution
```

### CLI install (any platform)
```bash
pipx install git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli
cpp-constitution install . --platform claude-code
```

## What the Skill Does

When reviewing C++ code, the `cpp-core-review` skill:

1. **Tool First**: Runs clang-tidy, cppcheck, clazy, iwyu before subjective review
2. **Priority review**: UB → Ownership → RAII → Concurrency → Error handling → API → Performance → Style
3. **Ownership classification**: Never blindly replace raw pointers — classify first (owning, observer, borrowed, nullable, C API, legacy)
4. **Progressive loading**: Detailed rules load on demand from `references/`
5. **Known AI failures**: Checks against GOTCHAS.md patterns

## Core Rules (Always Active)

### Ownership
- RAII for all resources. No raw `new`/`delete`.
- `unique_ptr` by default. `shared_ptr` only for genuine shared ownership.
- Raw pointers/references are non-owning.
- `span` and `string_view` for non-owning views. Watch lifetime.

### Concurrency
- No shared mutable state without protection.
- Prefer message passing over locks.
- No detached threads.
- Document lock ordering.

### Error Handling
- One strategy per module: exceptions, `expected`, `Result`, or `error_code`.
- Never throw from destructors.
- Never silently swallow errors.

### Interfaces
- Small, explicit, `const`-correct.
- `explicit` on single-arg constructors.
- Return values over output parameters.

## Workflow

1. Check project tooling first (clang-tidy, compile_commands.json).
2. Classify ownership before changing pointer types.
3. Safety fixes before style changes.
4. Run format + static analysis before commit.
5. Profile before optimizing.

## Output Language

Match the user's language. Chinese prompt → Chinese review. English → English.
Always keep code, identifiers, and technical terms in English.
