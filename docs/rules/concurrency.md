# Concurrency Rules

- Shared mutable state must be minimized.
- Prefer task queues over manual thread management.
- Use RAII locking.
- Never call unknown code while holding locks.
- Avoid detached threads.
- Document lock ordering.
