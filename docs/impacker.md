# Using `impacker`

CKP is compatible with [impacker](https://github.com/123jimin/impacker), a tool for packing a code and its dependencies into one file. Therefore, CKP can be used for online judges which cannot accept more than one source file.

## Instruction

Assume that you've written a program using CKP like this.

```py
from ckp.number_theory.primality_test import is_prime_naive

N = int(input())
print(is_prime_naive(N))
```

First, install impacker.

```sh
# Using Poetry
poetry add git+https://github.com/123jimin/impacker.git
```

Then, run impacker (assuming that the source file is `code.py`, and you wish the result file's name to be `out.py`):

```sh
poetry run python -m impacker code.py out.py
```

`out.py` will contain the packed source code, submittable to online judges:

```py
import math

# From primality_test.py
def is_prime_naive(n: int) -> bool:
    """
        Naive primality testing.
        - Time: `O(sqrt(n))`
    """
    if n < 100:
        return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or (n % 7 == 0) or (n % 11 == 0):
        return False
    for p in range(13, math.isqrt(n) + 1, 6):
        if n % p == 0 or n % (p + 4) == 0:
            return False
    return True

# From test.py
N = int(input())
print(is_prime_naive(N))
```

Try running the following for available arguments:

```sh
poetry run python -m impacker -h
```

## Caveats

impacker is not a perfect solution, and there are many issues with it.

- impacker doesn't support global variables in imported modules.
  - Hence, CKP does not make use of any global variables.
  - Using global variables on main code file is fine.
- impacker may pack unused `import` statements.
  - If you don't care about unused code, then this issue can be ignored.
- If a class is being used, then impacker will pack all parts of the class.
  - Consider using imperative API over object-oriented API.
  - Again, if you don't care about unused code, then this issue can be ignored.