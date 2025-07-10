# Using `impacker`

CKP is compatible with [impacker](https://github.com/123jimin/impacker), a tool for packing a code and its dependencies into one file. Therefore, CKP can be used for online judges which cannot accept more than one source file.

## Instruction

Assume that you've written a program using CKP like this.

```py
from ckp.number_theory.primality_test import is_prime_trial_division

N = int(input())
print(is_prime_trial_division(N))
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
from math import isqrt

# is_prime_trial_division | from primality_test.py, line 3
def is_prime_trial_division(n: int) -> bool:
    """ Primality testing using trial division. Slow but good enough for simple problems. """
    if n < 53:
        return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
    if not (n & 1 and n % 3 and n % 5 and n % 7 and n % 11 and n % 13):
        return False
    if n < 289:
        return True
    for p in range(17, isqrt(n) + 1, 6):
        if not (n % p and n % (p + 2)):
            return False
    return True

# From main code
N = int(input())
print(is_prime_trial_division(N))
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