# CKP - Code Kit for Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [한국어](README.ko-KR.md)

> [!CAUTION]
> This library is currently work-in-progress. Any API may change.

CKP is a collection of **no-dependency, pure Python implementations** of various algorithms for competitive programming.

CKP aims to provide versatile interface, without hurting performance.

CKP is compatible with [impacker](https://github.com/123jimin/impacker), a tool for packing a code and its dependencies into one file. Therefore, CKP can be used for online judges which cannot accept more than one source file.

## Examples

For the full list of functions, refer to the document (TO-DO).

### Segment Tree

```py
from ckp.data_structure import SimpleSegmentTree
from ckp.number_theory import PrimeSieve

tree = SimpleSegmentTree(list(PrimeSieve(10_000_000).primes()), op=lambda x,y: (x*y)%1_000_000, e=1)
print(len(tree)) # 664579
print(tree.reduce()) # 668970 (last 6 digits of product of all primes <= 10_000_000)
print(tree.reduce_range(12345, 67890)) # 830967

tree[20000] = 100
print(tree.reduce_range(12345, 67890)) # 596900
```

### Factoring

```py
from ckp.number_theory import factor

# [3250204337, 9181271329]
print(sorted(factor(29841007892689553873)))
```

## Notes

Implementations of `SortedList` and `SortedDict` are based on `sortedcontainers` (<https://github.com/grantjenks/python-sortedcontainers>), which is originally under Apache License, version 2.0 (<http://www.apache.org/licenses/LICENSE-2.0>).

Using CKP for purposes other than competitive programming is not recommended. This library is (and *must* be) written in pure Python, which is a huge restriction on performance.

If your application doesn't require you to write code in pure Python, then *please* implement your own C extensions, use another library, or use another language.

## To-Do List

- [x] `automata`
- [ ] `data_structure`
  - [x] `disjoint_set`
  - [x] `graph`
  - [ ] `segment_tree`
  - [x] `sorted_containers`
- [ ] `fourier`
  - [x] `complex`
  - [ ] `ntt`
- [x] `geometry`
  - [x] `circumcircle`
  - [x] `circumsphere`
  - [x] `convex_hull`
  - [ ] `delaunay`
- [ ] `graph_theory`
  - [ ] `bipartite_matching`
  - [x] `ford_fulkerson`
  - [ ] `strongly_connected_components`
- [ ] `language`
- [x] `linear_algebra`
- [x] `nimber`
- [x] `number_theory`
- [ ] `polynomial`
- [ ] `string`
  - [x] `kmp`
  - [ ] `suffix_array`

## Usage

### Installing

I *strongly* recommend using [Poetry](https://python-poetry.org/).

```sh
poetry add git+https://github.com/123jimin/ckp.git
```

### Using

Write your code using CKP, like this:

```py
from ckp.number_theory.primality_test import is_prime_naive

N = int(input())
print(is_prime_naive(N))
```

Run your code like this:

```sh
poetry run python test.py
```

### Packing

To pack CKP into the source code, install [impacker](https://github.com/123jimin/impacker).

```sh
poetry add git+https://github.com/123jimin/impacker.git
```

Pack CKP by using impacker (assuming that your source code's name is `code.py`, and you wish the result file's name to be `out.py`):

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
