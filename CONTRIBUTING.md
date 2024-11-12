# Contributing to CKP

## Code of Conduct

## Reporting Bugs

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

### No Name Collision

### Prefer Imperative over Object-Oriented
