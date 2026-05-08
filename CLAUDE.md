# C++ AI Constitution

## Core Rules

- Use RAII for all resource ownership.
- Do not use raw `new` / `delete` in application code.
- Prefer `std::unique_ptr` for ownership.
- Use `std::shared_ptr` only for real shared ownership.
- Raw pointers and references are non-owning.
- Prefer `std::span` and `std::string_view` for non-owning views.
- Avoid global mutable state.
- Prefer small, explicit interfaces.
- Prefer return values over output parameters.
- Mark single-argument constructors as `explicit`.
- Mark read-only member functions as `const`.
- Always initialize objects.
- Prefer standard library containers and algorithms.
- Use project-defined Result/expected style consistently.
- Avoid detached threads.
- Shared mutable state must be protected.
- `clang-format` and `clang-tidy` must pass before commit.

## Workflow

1. Read spec and architecture docs first.
2. Keep changes minimal and localized.
3. Run format + static analysis before finalizing.
4. Prefer readability over cleverness.
