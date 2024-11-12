# CKP

CKP is a Python library implementing various algorithms for competitive programming.

## Features

- **Pure Python**
- **No Dependency**
- **Online Judge-friendly**: [Using impacker](impacker.md), codes using CKP can be submitted to various online judge services.
- **Modular and Versatile**
- **Performant**

### Example

Here's a simple code for computing sum of all prime numbers under $10^7$:

```py
from ckp.number_theory import PrimeSieve

print(sum(PrimeSieve(10_000_000).primes())) # 3203324994356
```

## Caveats

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