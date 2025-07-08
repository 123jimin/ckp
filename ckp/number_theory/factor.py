import math
from .primality_test import is_prime

def factor_trial_division(n: int):
    """ Factor `n` using trial division.. Yields every prime factors of `n` (with duplicates), in no particular order. """
    if n < 2: return

    while not(n&1): yield 2; n //= 2
    if n == 1: return

    while not(n%3): yield 3; n //= 3
    if n == 1: return
    
    while not(n%5): yield 5; n //= 5
    if n == 1: return

    while not(n%7): yield 7; n //= 7
    if n == 1: return

    p, psq = 11, 121

    while psq <= n:
        if not(n%p):
            yield p; n //= p
            while not(n%p): yield p; n //= p
            if psq <= n: continue
            if 1 < n: yield n
            return
        p += 2
        while not(n%p): yield p; n //= p
        psq += 12*(p + 1)
        p += 4
    
    if 1 < n: yield n

def pollard_rho_find_divisor(n: int, start: int = 2):
    """ Using a proper divisor of `n` , using Pollard's rho algorithm. """
    g = math.gcd
    if 1 < (d := g(n, start)) < n: return d

    l = [x:=start*start%n+1]
    for p in l:
        if (d := g((y:=x*x%n+1) - p, n)) != 1: return 0 if d == n else d
        l += (y, x:=y*y%n+1)

def factor_pollard_rho(n: int):
    """
        Using Pollard's rho algorithm, yields every prime factors of `n` (with duplicates), in no particular order.
    """
    if n < 2: return

    while not(n&1): yield 2; n //= 2
    if n == 1: return

    while not(n%3): yield 3; n //= 3
    if n == 1: return
    
    while not(n%5): yield 5; n //= 5
    if n == 1: return

    while not(n%7): yield 7; n //= 7
    if n == 1: return

    if is_prime(n): yield n; return
    
    nsq = math.isqrt(n)
    if nsq*nsq == n:
        for nsq_factor in factor(nsq):
            yield nsq_factor
            yield nsq_factor
        return
    
    start = 2
    while not(d := pollard_rho_find_divisor(n, start)):
        start += 1
    
    yield from factor(d)
    yield from factor(n // d)

def factor(n:int):
    """
        Yields every prime factors of `n` (with duplicates), in no particular order.

        The empirically best algorithm is selected based on `n`.
    """

    if n < 2: return
    if n < 1500: yield from factor_trial_division(n)
    else: yield from factor_pollard_rho(n)

import itertools
from collections import Counter

def divisors(n:int, n_factors:Counter|list[int]|None = None):
    """
        Yields every divisors of n, in no particular order.
        
        When `n_factors` is given, it would be regarded as the factorization of `n`.
        In this case, the provided n can either be the original value or 0.
    """
    if not n:
        if n_factors is None: raise ValueError("`n_factors` must be provided when n is zero.")
    elif n == 1:
        yield 1; return
    elif n < 4:
        yield 1; yield n; return

    if n_factors is None: n_factors = Counter(factor(n))
    elif not isinstance(n_factors, Counter): n_factors = Counter(n_factors)

    for ks in itertools.product(*([p**i for i in range(k+1)] for (p, k) in n_factors.items())):
        m = 1
        for pk in ks: m *= pk
        yield m