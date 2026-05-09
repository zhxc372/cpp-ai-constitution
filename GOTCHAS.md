# GOTCHAS.md

AI failures observed in C++ code generation and review.

## Ownership

- Replacing every raw pointer with `unique_ptr` or `shared_ptr` without classifying ownership intent.
- Introducing `shared_ptr` to silence ownership uncertainty instead of clarifying the design.
- Forgetting that `shared_ptr` circular references cause memory leaks (use `weak_ptr`).
- Assuming `const` implies thread safety. It does not.

## Lifetime

- `string_view` pointing to a temporary that gets destroyed.
- `span` outliving the container it references.
- Returning reference to local or moved-from object.
- Lambda capturing references that dangle after the enclosing scope ends.
- Storing `this` pointer in lambda or callback without lifetime guarantee.
- `auto` deducing `const char*` from string literal but storing as `std::string` copy unexpectedly.

## RAII

- Wrapping C API handles without checking copy/move semantics of the wrapper.
- Double-free when RAII wrapper coexists with manual cleanup in legacy code.
- RAII destructor calling into already-destroyed subsystem during shutdown.
- Forgetting that move-from object is in valid but unspecified state.

## Exceptions

- Introducing exceptions into codebases compiled with `-fno-exceptions`.
- Throwing from destructors.
- Mixing error codes and exceptions within the same module without clear boundary.
- Assuming exception safety level without auditing constructors.

## Concurrency

- Capturing by reference in async tasks that outlive the caller.
- Claiming thread safety from `const` member functions that return iterators or references.
- Deadlock from inconsistent lock ordering.
- Recommending lock-free structures without evidence that locking is the bottleneck.
- Forgetting that `static` local variables have hidden synchronization overhead.
- Data race in lazy initialization without proper synchronization.

## Templates

- Over-constraining template parameters when concepts would clarify intent.
- Writing SFINAE when `if constexpr` suffices.
- Template bloat from header-only implementations in hot paths.
- Ignoring compilation error readability when designing template interfaces.

## Modernization

- Applying `auto` everywhere, hiding surprising type deductions.
- Replacing `NULL` with `nullptr` but missing implicit bool conversions.
- Using structured bindings with types that have surprising `get<>` behavior.
- "Modernizing" working legacy code without tests.
- Recommending `std::optional` without checking the contained type's overhead.

## Performance

- Replacing low-level hot-path code without measurement.
- Assuming abstraction cost is zero (virtual dispatch, `shared_ptr` atomic ops, `function` type erasure).
- Ignoring cache locality when recommending data structure changes.
- Premature pessimization: unnecessary copies, heap allocations, atomic operations.
- ABI constraints preventing certain refactors in library interfaces.
