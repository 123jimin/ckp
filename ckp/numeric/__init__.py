"""
    This package deals with various numeric functions that's not contained in Python's `math` or `cmath` packages.
    Functions are named with specific rules:
    - `foo() -> float` returns a float value.
    - `foo_exact() -> int or fractions.Fraction` returns an exact value.
    - `foo_decimal() -> decimal.Decimal` returns an approximated decimal value.
"""

from .const import *
from .combinatorics import *