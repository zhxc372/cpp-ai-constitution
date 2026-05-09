# Exceptions and Error Handling

## Rules

- Pick ONE error strategy per module: exceptions, `expected<T, Error>`, `Result<T>`, or `error_code`.
- Do not mix strategies within the same module.
- Errors must propagate. Do not silently swallow.
- Log at module boundaries.
- Destructors must never throw.

## Common AI Mistakes

- Introducing exceptions into `-fno-exceptions` codebases.
- Throwing in destructors.
- Mixing error codes and exceptions in the same call chain without a clear boundary.
- Assuming exception safety without auditing constructors (what if a member constructor throws?).
- Returning error codes but not checking them at the call site.
- Using `errno` without immediately capturing it after the failing call.

## Strategy Selection

| Context | Strategy |
|---|---|
| Application code, exceptions enabled | `throw` / `try-catch` at boundaries |
| Library code, exceptions enabled | Throw, document exception guarantees |
| No-exceptions codebase | `expected<T, Error>` or `Result<T>` |
| System/low-level code | `error_code` + return value |
| C API boundary | Return code + output parameter |

## Exception Safety Levels

1. **No guarantee**: Nothing. Fix immediately.
2. **Basic**: No leaks, invariants maintained. Minimum acceptable.
3. **Strong**: Operation succeeds or state is rolled back.
4. **No-throw**: Destructors, move constructors, swap. Must be `noexcept`.
