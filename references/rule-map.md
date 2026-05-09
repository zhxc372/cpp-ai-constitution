# Rule Map

Quick reference for which rules apply when.

## Always Apply

- Ownership must be explicit in types.
- RAII for all resources.
- No undefined behavior.
- No resource leaks.
- Initialize all objects.
- No raw `new`/`delete` in application code.

## Conditionally Apply

| Condition | Read |
|---|---|
| Multi-threaded code | `concurrency.md` |
| Custom error handling | `error-handling.md` |
| Template-heavy code | `templates.md` |
| Performance-critical paths | `performance.md` |
| Ownership/lifetime questions | `lifetime.md` |
| API/interface design | `interfaces.md` |
| Class hierarchy design | `classes.md` |
| Resource management patterns | `resource-management.md` |

## Exception Policy

These situations warrant exceptions to "modern C++" rules:

- C API boundaries (raw pointers, manual lifetime)
- Legacy codebases without test coverage (do not touch without tests)
- Performance hot paths (profile before refactoring)
- ABI-stable library interfaces (virtual dispatch may be required)
- Embedded/constrained environments (exceptions may be disabled)
- Existing codebase conventions (consistency beats perfection)
