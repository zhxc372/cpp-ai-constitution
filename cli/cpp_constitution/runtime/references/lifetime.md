# Lifetime and Ownership

## Pointer Classification

Before touching any pointer, classify it:

**Owning**: Responsible for deletion. Use `unique_ptr`, `shared_ptr`, or container.
**Non-owning observer**: Just looking. Raw pointer or reference. Lifetime guaranteed by owner.
**Borrowed parameter**: Function argument, does not extend lifetime. Prefer reference, use pointer only if nullable.
**Nullable optional**: Use `std::optional<std::reference_wrapper<T>>` or raw pointer with null semantics.
**C API boundary**: Raw pointer required. Document ownership transfer clearly.
**Legacy escape hatch**: Document why, add TODO, contain the scope.

## Lifetime Hazards

### Dangling References

```cpp
// BAD: view outlives temporary
std::string_view sv = std::string("temp");  // dangling

// BAD: span outlives container
std::span<int> get_data() {
    std::vector<int> v = {1, 2, 3};
    return v;  // dangling
}

// BAD: lambda captures local reference
int x = 0;
int& ref = x;
auto lam = [&ref]() { return ref; };  // dangerous if lam outlives x
```

### Move Semantics

- After `std::move(x)`, `x` is in valid but unspecified state. Do not read from it.
- `const` prevents move: `const unique_ptr<T>` cannot be moved from.
- Returning `std::move(local)` is redundant and prevents copy elision (NRVO).

### shared_ptr Traps

- Circular reference: `A` holds `shared_ptr<B>`, `B` holds `shared_ptr<A>`. Use `weak_ptr`.
- Atomic reference count overhead in hot paths.
- `enable_shared_from_this` required when creating `shared_ptr` from `this`.

## Ownership Patterns

**Unique ownership** (default): `unique_ptr`, containers, value semantics.
**Shared ownership** (rare): `shared_ptr` only when ownership is genuinely shared across lifetimes.
**Non-owning**: Raw pointer, reference, `span`, `string_view`. Never delete these.
**Transfer**: Pass `unique_ptr` by value or rvalue reference. Never by const reference.
