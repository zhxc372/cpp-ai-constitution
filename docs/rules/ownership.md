# Ownership Rules

## Allowed

- std::unique_ptr
- std::shared_ptr (when truly shared)
- stack objects
- std::span
- std::string_view

## Forbidden

- raw new/delete
- malloc/free
- ownership ambiguity
- returning pointer to local object

## Design Principle

Ownership must be visible in types.
