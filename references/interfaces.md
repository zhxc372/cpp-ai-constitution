# Interfaces

## Design Rules

- Keep interfaces small. Prefer minimal, composable APIs.
- Prefer return values over output parameters.
- Mark single-argument constructors `explicit`.
- Mark read-only member functions `const`.
- Use `std::span` and `std::string_view` for non-owning parameters.
- Prefer `std::optional<T>` over sentinel values.

## Common AI Mistakes

- Adding boolean flag parameters instead of named enums or separate functions.
- Making interfaces "convenient" with 10 overloads when 2 well-named functions suffice.
- Returning raw pointers when `optional<reference_wrapper<T>>` or `T*` with null semantics is clearer.
- Forgetting `noexcept` on move constructors and swap operations.
- Making virtual functions in templates (vtable bloat).

## API Boundary Patterns

```cpp
// Input: non-owning, non-null
void process(const std::string& data);

// Input: non-owning, nullable
void process(const std::string* data);  // nullptr = no data

// Input: taking ownership
void process(std::unique_ptr<Data> data);

// Output: returning value
std::string compute();

// Output: returning optional
std::optional<Result> try_compute();

// Output: returning reference to internal state (dangerous, document lifetime)
const Config& config() const;
```
