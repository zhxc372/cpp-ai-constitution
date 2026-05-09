# Hero Queries

Key test cases to validate the Skill produces correct behavior.

## Case 1: Shared Pointer Circularity

**Input**: AI generates observer pattern with `shared_ptr` everywhere.
**Expected**: Skill flags circular reference risk, suggests `weak_ptr` for observers.

## Case 2: String View Dangling

**Input**: AI returns `string_view` from function that creates temporary string.
**Expected**: Skill flags dangling reference, suggests returning `std::string`.

## Case 3: Const Thread Safety

**Input**: AI marks class "thread-safe" because all methods are `const`.
**Expected**: Skill flags that `const` does not imply thread safety, checks for shared mutable state.

## Case 4: Mechanical Modernization

**Input**: AI suggests replacing all raw pointers with `unique_ptr` in legacy C API wrapper.
**Expected**: Skill flags C API boundary exception, recommends documenting ownership transfer instead.

## Case 5: Exception in No-Exceptions Code

**Input**: AI introduces `throw` in embedded system codebase.
**Expected**: Skill checks for `-fno-exceptions` or project policy, flags the incompatibility.

## Case 6: Virtual in Constructor

**Input**: AI calls virtual function from base class constructor.
**Expected**: Skill flags undefined behavior (calls base version, not derived).

## Case 7: Move from Const

**Input**: AI writes `const unique_ptr<T>` and tries to move it.
**Expected**: Skill flags that `const` prevents move, suggests removing `const`.

## Case 8: Premature Performance Optimization

**Input**: AI recommends replacing `std::vector` with custom allocator without profiling data.
**Expected**: Skill asks for measurement data before recommending performance changes.
