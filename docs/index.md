# CKP

CKP is a Python library implementing various algorithms for competitive programming.

- [GitHub repository](https://github.com/123jimin/ckp)
- [License](https://github.com/123jimin/ckp/blob/main/LICENSE)
- [Contributing](https://github.com/123jimin/ckp/blob/main/CONTRIBUTING.md)

## Features

- **Pure Python 3**
  - CKP does not use any C extensions. 
  - CKP supports both CPython and PyPy.
- **No Dependency**
  - CKP does not have any dependency.
- **Online Judge-friendly**
  - [Using impacker](impacker.md), codes using CKP can be submitted to various online judge services.
- **Performant**
  - Codes in CKP are micro-optimized on CPython.
  - There are [micro-benchmarks](./benchmark/index.md) for testing run-times.
- **Modular and Versatile**
  - The API of CKP is designed to be performant while being modular.
  - Each API function and class can be used in multiple scenarios.

### Example

Here's a simple code for computing sum of all prime numbers under $10^7$:

```py
from ckp.number_theory import PrimeSieve

print(sum(PrimeSieve(10_000_000).primes())) # 3203324994356
```

## Caveats

**Many parts of the library are work-in-progress.**

**There's no guarantee on API stability. No backwards compatibility is provided.**

Using CKP for purposes other than competitive programming is not recommended. Consider using another library, implementing your own C extension, or using another language.

## Library Index

### [Number Theory: `ckp.number_theory`](./number_theory/index.md)

### Linear Algebra: `ckp.linear_algebra`

### Strings: `ckp.string`

### Data Structures: `ckp.data_structure`

### Graph Theory: `ckp.graph_theory`

### Fourier Transformation: `ckp.fourier`

### Automata: `ckp.automata`

### Geometry: `ckp.geometry`

### Miscellaneous: `ckp.misc`

## License

CKP is licensed under the MIT license: <https://github.com/123jimin/ckp/blob/main/LICENSE>

- `ckp.data_structure.sorted_containers`: also check <https://github.com/grantjenks/python-sortedcontainers/blob/master/LICENSE>.
- `ckp.geometry.delaunay`: also check <https://github.com/mkirc/delaunay/blob/main/LICENSE>.