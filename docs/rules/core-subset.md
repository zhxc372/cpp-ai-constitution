# Core Subset

## Ownership

- Ownership must be explicit.
- Prefer RAII.
- Prefer stack allocation.
- Raw pointers are non-owning.

## Interfaces

- Keep interfaces small.
- Avoid hidden side effects.
- Prefer value returns.

## Functions

- One logical operation per function.
- Avoid boolean flag parameters.
- Prefer clear naming over comments.

## Concurrency

- Avoid shared mutable state.
- Prefer tasks/message passing.
- Lock ownership must be clear.

## Error Handling

- Use one consistent error strategy.
- Do not silently ignore errors.
