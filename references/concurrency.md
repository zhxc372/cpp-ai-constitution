# Concurrency

## Rules

- Shared mutable state must be protected. No exceptions.
- Prefer message passing and task queues over shared state with locks.
- Lock ordering must be documented and followed globally.
- Never call unknown code (callbacks, virtual functions) while holding a lock.
- Avoid detached threads. Use scoped joinable threads or task pools.

## Common AI Mistakes

- Claiming `const` member function is thread-safe. It is not if it returns mutable reference or iterator.
- Forgetting to protect lazy initialization: `if (!init) { init = true; setup(); }` is a data race even with `std::call_once`.
- Capturing `this` in lambda passed to async API without ensuring object lifetime.
- Recommending `std::atomic` for compound operations that need a mutex.
- Ignoring false sharing in performance-sensitive concurrent code.

## Patterns

### Prefer

- `std::jthread` (C++20) over `std::thread`
- `std::atomic` for simple flags and counters
- `std::mutex` + `std::lock_guard` for compound state
- Lock-free only when profiling proves lock contention is the bottleneck

### Avoid

- `std::shared_mutex` unless read-heavy workloads are measured
- Spin-locks in userspace
- Manual condition variable when `std::stop_source` or `std::latch` suffice
- `volatile` for synchronization (it is not atomic)
