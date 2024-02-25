# CKP - Code Kit for Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!CAUTION]
> This library is currently work-in-progress.

CKP is a collection of pure Python implementations of various algorithms for competitive programming.

CKP aims to provide versatile interface, without hurting performance.

CKP is compatible with [impacker](https://github.com/123jimin/impacker), a library (currently WIP) for packing a code and its dependencies into one file. Therefore, CKP can be used for online judges which cannot accept more than one source file.

## Notes

Implementations of `SortedList` and `SortedDict` are based on `sortedcontainers` (https://github.com/grantjenks/python-sortedcontainers), which is originally under Apache License, version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

Using CKP for purposes other than competitive programming is not recommended, as this library is written in pure Python, which is much slower than C extensions.

Please implement your own C extensions, or use another language, if your application doesn't require you to write code in pure Python.

## Usage

```py
from ckp.number_theory import is_prime_naive

N = int(input())
print(is_prime_naive(N))
```
