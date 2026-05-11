# Performance

## Rules

- Profile before optimizing. Always.
- Do not replace working hot-path code without measurement.
- Know the cost of abstractions: virtual dispatch, `shared_ptr` atomic ops, `std::function` type erasure, `std::any`, heap allocation.
- Check cache locality before recommending data structure changes.
- Consider ABI constraints in library interfaces.

## Common AI Mistakes

- Recommending algorithm changes without knowing the data size or access pattern.
- "Optimizing" by replacing `vector` with `unordered_map` for N<20 (linear scan is faster).
- Ignoring move semantics, causing unnecessary copies.
- Allocating in hot loops.
- Recommending lock-free structures without evidence of lock contention.

## Measurement Tools

- `perf` (Linux)
- `Instruments` (macOS)
- `VTune` (Intel)
- `google-benchmark`
- Compiler flags: `-O2 -march=native`, sanitizer benchmarks separately

## Hot Path Checklist

When reviewing performance-critical code:

1. Any heap allocations in the loop? Can they be pre-allocated?
2. Any copies that could be moves?
3. False sharing between threads?
4. Branch prediction misses? Can sort/predicate help?
5. Cache-friendly data layout?
6. Unnecessary synchronization?
