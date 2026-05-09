# AI Review Prompt

## Checklist (in priority order)

1. **UB/Safety**: Undefined behavior, memory corruption, data races, dangling references.
2. **Ownership**: Lifetime bugs, resource leaks, shared_ptr circular refs, RAII correctness.
3. **Correctness**: Logic errors, wrong API usage, missing error handling.
4. **Concurrency**: Shared mutable state protection, lock ordering, async lifetime.
5. **Exception safety**: Basic guarantee met? Destructors noexcept? Consistent strategy?
6. **Interface**: Small, explicit, const-correct, no boolean flags.
7. **Performance**: Measured? Hot path? Abstraction cost justified?
8. **Modernization**: Separate from safety fixes. Tests pass?

## Rules

- Prefer tool findings (clang-tidy) over subjective opinion.
- Actionable comments only. No style nitpicks without engineering value.
- If code is legacy without tests, flag but do not refactor.
- Check GOTCHAS.md for known AI failure patterns.
