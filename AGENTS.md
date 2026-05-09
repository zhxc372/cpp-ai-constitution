# C++ AI Constitution

This project uses a C++ AI Constitution. All AI coding agents must follow these rules when modifying, reviewing, or designing C++ code.

## Rule Loading

Load detailed rules only when relevant.

- Ownership and lifetime: `references/lifetime.md`
- RAII and resources: `references/resource-management.md`
- Concurrency: `references/concurrency.md`
- Error handling: `references/error-handling.md`
- API design: `references/interfaces.md`
- Classes: `references/classes.md`
- Templates: `references/templates.md`
- Performance: `references/performance.md`
- Known AI failures: `GOTCHAS.md`
- Full rule map: `references/rule-map.md`

Do not load every rule file at once unless explicitly asked for a full audit.

## Review Priority

Review C++ code in this order:

1. Correctness and undefined behavior
2. Ownership and lifetime
3. RAII and resource release
4. Concurrency and shared state
5. Error handling consistency
6. API and interface clarity
7. Performance-sensitive changes
8. Style and readability

## Critical Constraints

- Do not apply modern C++ rules mechanically.
- Do not replace raw pointers with smart pointers before classifying ownership.
- Do not introduce exceptions if the project disables exceptions.
- Do not change public APIs or ABI boundaries without an explicit migration plan.
- Do not mix safety fixes with large style rewrites.
- Prefer tool-backed checks when available.
