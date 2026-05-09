# Classes

## Rules

- Rule of zero: if you can avoid writing any special member function, do it.
- Rule of five: if you write one, write all five (destructor, copy ctor, copy assign, move ctor, move assign).
- Never call virtual functions from constructors or destructors.
- Prefer composition over inheritance.
- Keep inheritance hierarchies shallow (max 3 levels unless domain requires more).

## Common AI Mistakes

- Adding virtual destructor to every class, even final leaf classes with no base.
- Deep inheritance trees where composition or variant/visit would be cleaner.
- Protected data members (use private + accessors).
- Making everything a class when a free function + struct suffices.
- Forgetting `override` on virtual function overrides.

## Value Types vs Polymorphic Types

**Value type**: Small, copyable, no virtual functions. Pass by value or const reference.
**Polymorphic type**: Base class with virtual functions. Pass by `unique_ptr<Base>` or reference.

Do not mix value semantics with polymorphism.
