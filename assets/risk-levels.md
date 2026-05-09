# Risk Levels

## Critical (must fix before merge)

- Undefined behavior
- Memory corruption, use-after-free, double-free
- Data races
- Resource leaks in long-running processes
- Security vulnerabilities (buffer overflow, injection)
- Throwing from destructors

## High (fix soon)

- Ownership ambiguity that could lead to lifetime bugs
- Missing `noexcept` on move constructors in performance-critical code
- Exception safety violations (basic guarantee not met)
- Missing error handling on fallible operations
- Thread safety issues in shared state

## Medium (fix in next iteration)

- Style inconsistencies across a module
- Missing `explicit` on single-arg constructors
- Suboptimal API design (output parameters, boolean flags)
- Missing `const` correctness
- Unnecessary copies that are not in hot paths

## Low (nice to have)

- Naming convention deviations
- Comment style
- Include order
- Formatting not caught by clang-format
