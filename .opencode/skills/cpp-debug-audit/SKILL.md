---
name: cpp-debug-audit
description: Load when debugging crashes, memory errors, data races, undefined behavior, or performance issues in C++ code, or when performing a systematic safety audit.
license: MIT
compatibility: opencode
metadata:
  domain: cpp
  mode: debug
  risk: safety-correctness
---
<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->


# C++ Debug & Audit Skill

Use this skill for debugging C++ issues and performing systematic safety audits.

## Debug Priority

When debugging crashes or memory issues, check in this order:

1. **Use-after-free / dangling references** — sanitizers first (`-fsanitize=address`)
2. **Buffer overflows** — `-fsanitize=undefined`
3. **Data races** — `-fsanitize=thread`
4. **Uninitialized reads** — `-fsanitize=memory` (Clang)
5. **Double-free** — check RAII ownership
6. **Stack overflow** — check recursion depth, large stack allocations
7. **ABI mismatch** — check linking, ODR violations

## Audit Checklist

For systematic safety audit:

- [ ] All raw pointers classified (owning vs non-owning)
- [ ] All resources wrapped in RAII
- [ ] No `new`/`delete` in application code
- [ ] No mutable global state without synchronization
- [ ] No detached threads
- [ ] Lock ordering documented
- [ ] Error handling strategy consistent per module
- [ ] No throwing from destructors
- [ ] Move semantics correct (no move-from-const)
- [ ] `string_view`/`span` lifetime verified
- [ ] No virtual calls in constructors/destructors

## Tool Usage

```bash
# Address sanitizer
clang++ -fsanitize=address -g -O1 source.cpp

# Thread sanitizer
clang++ -fsanitize=thread -g -O1 source.cpp

# Undefined behavior sanitizer
clang++ -fsanitize=undefined -g -O1 source.cpp

# Static analysis
clang-tidy source.cpp --config-file=config/.clang-tidy -- -std=c++20

# Run with Valgrind (Linux)
valgrind --leak-check=full --track-origins=yes ./program
```

## Output Format

### Root Cause Analysis
What is the most likely cause? What evidence supports it?

### Reproduction
Minimum steps to reproduce.

### Fix
Precise fix with explanation of why it works.

### Prevention
What rule or check would catch this class of bug in the future?
