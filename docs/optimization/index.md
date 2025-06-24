# Optimizing CPython Code

Optimizing pure CPython code is far from intuitive.

In most other languages, you may rely on compilers for various small yet extremely useful optimizations, such as constant propagation, variable lookup, arithmetic operations etc.... However, CPython's bytecode compiler is doing a bare minimum job, without doing any significant optimizations.

## General Rules

These are the most important tips.

- **Always benchmark. Always mind that large fluctuations may exist between different invocations.**
- Function calls are expensive. Try to avoid them.
- Python loops are expensive. Try using "native" functions such as `sum` or `max`, for example.
- References are expensive. Try finding a way to avoid references.
- Try bringing variables to local scope, as local lookup is cheaper.

## Integer Arithmetic

Whether the absolute value of an integer is less than $2^{30}$ or not heavily affects the performance, as that's the size of a digit CPython uses. Hence, it is extremely important to distinguish between "small" integers (absolute value less than $2^{30}$) and "large" integers.

### Boolean Conversion

- Use `x` and `not x` for condition expressions.
- Use `not not x` to convert `x` to a boolean. Do not use `bool(x)`, nor `x != 0`.

### Bitwise Operations

- Except than `x&1`, refrain from using bitwise operations for small integers.
  - Prefer `%` and `//` over `&` and `>>`.
- *Do* use bitwise operations for large integers.

### DivMod

- Do *not* use `divmod` for small integers. (Function calls are really expensive.)
- Do *not* use `divmod` when the second argument is a power of 2.
- *Do* use `divmod` for large integers with non-power-of-2 second argument.

## Iteration

- Prefer `for _ in itertools.repeat(None, N)` over `for _ in range(N)`.
- If you need indices, prefer manual indices over `enumerate(A)` or `range(len(A))`.

## Containers
