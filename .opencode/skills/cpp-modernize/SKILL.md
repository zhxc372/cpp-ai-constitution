---
name: cpp-modernize
description: Load when modernizing, migrating, or upgrading C++ code from older standards (C++98/03/11/14) to modern C++ (17/20/23), or when applying systematic code improvements that preserve behavior.
license: MIT
compatibility: opencode
metadata:
  domain: cpp
  mode: refactor
  risk: behavior-preservation
---

# C++ Modernize Skill

Use this skill for C++ modernization, migration, and systematic refactoring.

## Critical Rule

**Do not modernize code before preserving behavior.**

Separate changes into:

1. Safety fixes (do first)
2. Behavior-preserving refactors
3. Style improvements (do last)
4. Performance changes (measure before and after)

Never mix safety-critical changes with large style rewrites.

## Before Starting

1. Confirm tests exist and pass.
2. Identify the current C++ standard.
3. Check build system and compiler flags.
4. Check for `-fno-exceptions` or other constraints.
5. Identify ABI boundaries that must not change.

## Common Modernization Paths

| From | To | Risk |
|---|---|---|
| Raw `new`/`delete` | RAII / smart pointers | Medium (classify ownership first) |
| Raw loops | Algorithms / ranges | Low (verify behavior) |
| `NULL` | `nullptr` | Low |
| `typedef` | `using` | Low |
| Manual resource management | RAII wrappers | Medium (check move semantics) |
| C-style arrays | `std::array` / `std::vector` | Medium (check sizeof, pointer arithmetic) |
| `boost::optional` | `std::optional` | Low (check API compatibility) |
| SFINAE | Concepts | Low (C++20+) |

## Gotchas

- Do not replace legacy code that works without tests.
- Do not change public ABI without a migration plan.
- `auto` can hide surprising type deductions.
- `std::string_view` does not own — check lifetime.
- Modern does not always mean better for embedded/constrained environments.
