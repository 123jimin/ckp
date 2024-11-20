"""
    This module contains functions for computing functions related to combinatorics.
"""

from math import log, comb

def log_comb(n: int, k: int) -> float:
    """ Computes `math.log(math.comb(n, k))`, accurately for large n and/or k. """
    # Degenerate case
    if n == 0: return 1
    # Exact for small values
    if n <= 30: return log(comb(n, k))
    # TODO
    raise NotImplementedError()

def normalized_log_comb(n: int, k: int) -> float:
    """ Computes `math.log(math.comb(n, k))/n`, accurately for large n and/or k. """
    # Degenerate case
    if n == 0: return 1
    # Exact for small values
    if n <= 30: return log(comb(n, k)) / n
    # TODO
    raise NotImplementedError()

def harmonic_series(n: int, *, _cache: list[int] = [0, 1, 1.5]) -> float:
    """ Computes `sum(1/i for i in range(1, n+1))`, accurately for large n. """
    if n <= 0: return 0
    if n == 1: return 1
    if n < len(_cache): return _cache[n]
    if n <= 100:
        s = _cache[-1]
        for i in range(len(_cache), n+1):
            s += 1/i
            _cache.append(s)
        return s
    # TODO
    raise NotImplementedError()

def coupon_collector_expected(n: int, k: int) -> float:
    """ Computes `n*(H(n) - H(n-k))`, the expected number of coupons collected for collecting `k` of `n` coupons. """
    if k == 0: return 0
    if n == k: return n * harmonic_series(n)
    if k <= 100: return n * sum(1/(n-i) for i in range(k))
    if n-k <= 100: return n * (harmonic_series(n) - harmonic_series(n-k))
    # TODO
    raise NotImplementedError()