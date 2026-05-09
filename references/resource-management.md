# Resource Management

## RAII Rules

Every resource (memory, file, socket, lock, handle) must be owned by exactly one object.

- Acquire in constructor, release in destructor.
- Make move semantics correct. Delete copy if not copyable.
- Never release manually if RAII wrapper owns it.
- Check C API boundaries: some resources need custom deleters.

## Custom Deleters

```cpp
// C file handle
auto file_closer = [](FILE* f) { if(f) fclose(f); };
std::unique_ptr<FILE, decltype(file_closer)> pipe(popen("cmd", "r"), file_closer);

// Platform handle
auto handle_closer = [](void* h) { CloseHandle(h); };
```

## Common Mistakes

- Wrapping a resource but forgetting the move constructor (double-free).
- RAII destructor calling into a subsystem that was already destroyed during shutdown.
- Using `shared_ptr` for resources that have single-owner semantics.
- Forgetting that `vector<bool>` is not a container of bools.

## Stack vs Heap

Prefer stack allocation:
- Deterministic destruction.
- No allocation overhead.
- Cache-friendly.

Use heap when:
- Lifetime exceeds scope.
- Size is runtime-dependent and large.
- Polymorphic ownership required.
- Move-only and non-copyable with uncertain lifetime.
