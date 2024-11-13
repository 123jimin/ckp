# CKP

CKP is a Python library providing various algorithms for solving competitive programming problems.

## Features

- **Online Judge-Friendly**
  - [Using impacker](impacker.md), codes that uses CKP can be submitted to online judge services, which usually only accept one source file without dependency.
- **Pure Python 3**
  - CKP does not use any C extensions.
  - CKP supports both CPython and PyPy.
- **No Dependency**
  - CKP does not have any dependency.
- **Performant**
  - CKP is micro-optimized for CPython.
  - There are [micro-benchmarks](./benchmark/index.md) for testing CKP's performance.
- **Modular and Versatile**
  - CKP is designed to be modular, while remaining performant.
  - Each API function and class can be used in multiple scenarios.

### Examples

Here's a simple code for computing sum of all prime numbers under $10^7$:

```py
from ckp.number_theory import PrimeSieve

# Prints "3203324994356".
print(sum(PrimeSieve(10_000_000).primes()))
```

## Installation

CKP is not yet on PyPI, so you need to get CKP from GitHub.

### Using PIP

```sh
pip install git+https://github.com/123jimin/ckp.git
```

### Using Poetry

I recommend using [Poetry](https://python-poetry.org/) to manage Python packages.

```sh
poetry add git+https://github.com/123jimin/ckp.git
```

## Library Index

Below is the list of submodules CKP provides. Click on a header to check API available under the module.

It's generally preferred to import one or more of the sub-packages, rather than doing `import ... from ckp`.

### [Number Theory: `ckp.number_theory`](./number_theory/index.md)

Contains various functions related to number theory, mostly for working on a finite field $\mathbb{F}_p$.

- Primality Test
- Prime Sieve
- Factorization
- Modular Arithmetic

### Linear Algebra: `ckp.linear_algebra`

### Strings: `ckp.string`

### Data Structures: `ckp.data_structure`

- Disjoint Set
- Segmented Tree
- Sorted Containers

### Graph Theory: `ckp.graph_theory`

Note: graph data structures themselves are under `ckp.data_structure.graph`, not under this module.

- Bipartite Marching

#### Tree Graphs: `ckp.graph_theory.tree`

- Least Common Ancestor
- Heavy-Light Decomposition

### Fourier Transformation: `ckp.fourier`

Contains various functions for discrete Fourier transformation (DFT).

- Cooley-Tukey FFT on $\mathbb{C}$

### Automata: `ckp.automata`

Contains algorithms related to finite-state automata.

- Regular Expression
  - Note: It's for converting theoretical regular expressions into DFAs, and not for typical regular expressions.
- DFA and NFA

### Geometry: `ckp.geometry`

Contains various algorithms and functions for 2D and 3D geometry.

- 2D and 3D Vectors
- Circumcircle and Circumsphere
- Convex Hull
- Delaunay Triangulation

### Nimber: `ckp.nimber`

Contains nimber arithmetic, which is just an another name for the Galois field $GF(2^{2^k})$.

### Miscellaneous: `ckp.misc`

Contains several niche algorithms that aren't used much.

- Longest Increasing Subsequence
- Rubik's Cube
- 3x3 Sudoku Solver

### Not in CKP

Following algorithms are not implemented in CKP, mostly because the Python Standard Library already provides an implementation.

- Memoization: Use [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache).
- Topological Sorting: Use [`graphlib.TopologicalSorter`](https://docs.python.org/3/library/graphlib.html#graphlib.TopologicalSorter).
- Balanced Trees (such as Red-Black Tree): Trees are generally slow on Python. Check `ckp.data_structure.sorted_containers`.

## Caveats

**Many parts of CKP are work-in-progress.**

**There's no guarantee on API stability. No backwards compatibility is provided.**

Using CKP for purposes other than competitive programming is not recommended. Consider using another library, implementing your own C extension, or using another language.

## License

CKP is licensed under the MIT license: <https://github.com/123jimin/ckp/blob/main/LICENSE>

- `ckp.data_structure.sorted_containers`: also check <https://github.com/grantjenks/python-sortedcontainers/blob/master/LICENSE>.
- `ckp.geometry.delaunay`: also check <https://github.com/mkirc/delaunay/blob/main/LICENSE>.