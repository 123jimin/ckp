# Contributing to CKP

Feel free to send pull requests, but currently it's likely to be revised/rejected by me.

- I'm still coming up with better API.
- There are some atypical code guidelines.

## Priority

Here's the basic gist on priorities for developing CKP.

1. **MUST** be pure Python without **any** external dependency.
2. Time complexity must be as best as possible.
3. API must not feel too specific / dependant on implementation.
   - Check `ckp.number_theory.primality_test` for general vibe on providing implementation-specific APIs.
4. Code must not be overtly long.
5. Implementation must be as fast as possible.
6. Code must be written in an maintainable manner.

The first one is absolute, but the rests are not in a strict order. The most important thing is that the library should be useful for creating fast solutions of competitive programming problems in pure Python.

## Code Guidelines

### No Global Variables

Currently, impacker can't handle global variables.

Instead of using global variables, consider using one of the following methods.

- Provide a function that provides global variables.
- Use classes.
- Use memoization (using `functools.cache`).

### No Global Name Collision

Currently, impacker doesn't try to resolve name collisions, so there could be errors when names of functions or classes across two files collide.

- Consider prefixing general category name of functions and classes.
- Avoid generic names which can be accidentally used.

### Provide Imperative Interface

It is very hard to do dependency analysis on member functions. Moreover, using "raw" data types such as tuples and lists is usually faster than using objects.

- Prefer `foo_method(...)` over `Foo.method(...)`.
- Keep classes minimal, and mostly use it as named tuples / dataclasses.