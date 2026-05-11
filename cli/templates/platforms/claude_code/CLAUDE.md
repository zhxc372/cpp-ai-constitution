<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->
# C++ AI Constitution

## Ownership

- RAII for all resources. No raw `new`/`delete`.
- `unique_ptr` by default. `shared_ptr` only for genuine shared ownership.
- Raw pointers/references are non-owning.
- `span` and `string_view` for non-owning views. Watch lifetime.

## Concurrency

- No shared mutable state without protection.
- Prefer message passing over locks.
- No detached threads.
- Document lock ordering.

## Error Handling

- One strategy per module: exceptions, `expected`, `Result`, or `error_code`.
- Never throw from destructors.
- Never silently swallow errors.

## Interfaces

- Small, explicit, `const`-correct.
- `explicit` on single-arg constructors.
- Return values over output parameters.

## Workflow

1. Check project tooling first (clang-tidy, compile_commands.json).
2. Classify ownership before changing pointer types.
3. Safety fixes before style changes.
4. Run format + static analysis before commit.
5. Profile before optimizing.
