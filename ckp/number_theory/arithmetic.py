"""
    Common arithmetic functions.
"""

from .factor import factor
from collections import Counter

def num_divisors(n:int, n_factors:Counter|list[int]|None = None):
    """
        Returns the \# of divisors of n, equivalent but a bit faster than `len(list(divisors(n)))`.
        
        When `n_factors` is given, it would be regarded as the factorization of `n`.
    """
    if n <= 12: return (0, 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6)[n]

    if n_factors is None: n_factors = Counter(factor(n))
    elif not isinstance(n_factors, Counter): n_factors = Counter(n_factors)

    m = 1
    for k in n_factors.values(): m *= k+1
    
    return m

def sum_divisors(n:int, n_factors:Counter|list[int]|None = None):
    """
        Returns sum of every divisors of n, equivalent but a bit faster than `sum(divisors(n))`.
        
        When `n_factors` is given, it would be regarded as the factorization of `n`.
    """
    if n <= 12: return (0, 1, 3, 4, 7, 6, 12, 8, 15, 13, 18, 12, 28)[n]

    if n_factors is None: n_factors = Counter(factor(n))
    elif not isinstance(n_factors, Counter): n_factors = Counter(n_factors)

    m = 1
    for (p, k) in n_factors.items():
        m *= (p**(k+1) - 1) // (p-1) # TODO: check whether this is faster than summation `1 + sum(p**i for i in range(1, k+1))`.
    
    return m

def euler_phi(n:int, n_factors:Counter|list[int]|None = None):
    """
        Returns \# of numbers x coprime to n, such that 1 <= x < n.

        When `n_factors` is given, it would be regarded as the factorization of `n`.
    """
    if n <= 12: return (0, 1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4)[n]

    m = 1
    if isinstance(n_factors, Counter):
        for (p, k) in n_factors.items():
            m *= (p-1) * p**(k-1)
        return m
    if n_factors is None:
        n_factors = factor(n)

    ps = set()
    for p in n_factors:
        if p in ps:
            m *= p
        else:
            ps.add(p)
            m *= p-1
    
    return m