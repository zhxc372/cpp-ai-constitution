---
name: cpp-core-review
description: Load when reviewing, refactoring, modernizing, debugging, or designing non-trivial C++ code where ownership, lifetime, RAII, concurrency, templates, interfaces, exceptions, or Core Guidelines compliance may affect correctness, safety, maintainability, or performance.
---
<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->


# C++ Core Review

## Review Priority

Review C++ code in this order:

1. Correctness and undefined behavior
2. Ownership and lifetime
3. RAII and resource release
4. Concurrency and shared state
5. Exception safety and error handling
6. API/interface design
7. Performance-sensitive code
8. Style and readability

Never mix safety-critical changes with style rewrites.

## Tool First

Before subjective review, discover project tooling:

1. `compile_commands.json`
2. `CMakeLists.txt` or build system config
3. `.clang-tidy` config
4. Compiler warning flags
5. Test commands
6. Sanitizer setup

Prefer tool-backed findings when available. Run `clang-tidy` before eyeballing code.

## Ownership Classification

Do not mechanically replace raw pointers. Classify first:

1. Owning pointer
2. Non-owning observer
3. Borrowed parameter
4. Nullable optional reference
5. C API boundary
6. Legacy escape hatch

Only change ownership types after confirming construction, destruction, transfer, aliasing, and ABI constraints.

## Modernization Discipline

Separate changes into:

1. Safety fixes (do first)
2. Behavior-preserving refactors
3. Style improvements (do last)
4. Performance changes

Do not modernize code before preserving behavior.
Do not replace legacy code just because it looks old.

## Condition Loading

Not all rules apply to all projects.

- If project has concurrency → read `references/concurrency.md`
- If project has custom error handling → read `references/error-handling.md`
- If project has template metaprogramming → read `references/templates.md`
- If project has performance-critical hot paths → read `references/performance.md`
- For ownership and lifetime questions → read `references/lifetime.md`
- For full rule map → read `references/rule-map.md`

## Gotchas

Read `GOTCHAS.md` for AI failure patterns in C++.

These come from real model mistakes, not from textbooks.

## Output Format

Categorize findings by severity:

- **UB/Safety**: Undefined behavior, memory corruption, data races
- **Ownership**: Lifetime bugs, resource leaks, dangling references
- **Correctness**: Logic errors, wrong API usage
- **Modernization**: Style/style improvements, modern C++ opportunities
- **Style**: Naming, formatting, readability

Actionable comments only. No style nitpicks without engineering value.

## Constitution

1. This Skill is not a C++ textbook.
2. It exists to prevent high-impact mistakes that models often miss.
3. Root SKILL.md stays short. Heavy material goes to `references/`.
4. Prefer mechanical checks over subjective review.
5. Never apply Core Guidelines mechanically without understanding context.
6. Every new rule must come from: repeated model failure, known safety hazard, project constraint, eval failure, or tool-detectable issue.
7. **PROJECT_CONSTITUTION.md is the highest constraint.** All adapters must follow ADAPTER_POLICY.md.
8. AI may not self-approve rule changes. Human review required for all core changes.
