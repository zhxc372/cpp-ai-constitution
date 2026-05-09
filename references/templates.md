# Templates and Concepts

## Rules

- Use C++20 concepts instead of SFINAE when available.
- Use `if constexpr` instead of tag dispatch or specialization when possible.
- Keep template parameters minimally constrained.
- Design template interfaces for readable error messages.

## Common AI Mistakes

- Writing SFINAE in C++20 codebases that have concepts available.
- Over-constraining concepts so valid types are rejected.
- Header-only template implementations causing compile time and binary bloat in hot paths.
- Ignoring ADL (Argument-Dependent Lookup) when designing template interfaces.
- Not testing template code with the actual types that will be used.

## Patterns

```cpp
// Prefer concepts over SFINAE
template<std::ranges::range R>
auto process(R&& r);

// Prefer if constexpr over specialization
template<typename T>
auto serialize(const T& val) {
    if constexpr (std::is_arithmetic_v<T>) { ... }
    else if constexpr (std::is_same_v<T, std::string>) { ... }
    else { ... }
}
```
