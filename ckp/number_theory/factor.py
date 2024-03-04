import math
from .primality_test import is_prime

def factor_naive(n: int):
    """
        Naive factoring. Yields every prime factors of `n` (with duplicates), in no particular order.
    """
    if n < 2: return

    while n%2 == 0:
        yield 2
        n //= 2
    if n == 1: return
    while n%3 == 0:
        yield 3
        n //= 3
    if n == 1: return
    while n%5 == 0:
        yield 5
        n //= 5
    if n == 1: return

    p = 7
    psq = 49

    while psq <= n:
        while n%p == 0:
            yield p
            n //= p
        if n <= psq:
            if 1 < n: yield n
            return
        p += 4
        while n%p == 0:
            yield p
            n //= p
        psq += 12*(p - 1)
        p += 2
    if n > 1: yield n

def pollard_rho_find_divisor(n:int, start:int = 2):
    """ Using a proper divisor of `n` , using Pollard's rho algorithm. """
    if 1 < math.gcd(n, start) < n: return start
    x, y = 0, start
    d = 1
    l = [start]
    while d == 1:
        # This is much faster than using `pow(y, 2, n)`.
        y = (y*y+1) % n
        l.append(y)
        y = (y*y+1) % n
        l.append(y)
        x += 1
        d = math.gcd(l[x]-y, n)
    return 0 if d == n else d

def factor_pollard_rho(n: int):
    """
        Using Pollard's rho algorithm, yields every prime factors of `n` (with duplicates), in no particular order.
    """
    if n < 2: return

    while n%2 == 0:
        yield 2
        n //= 2
    if n == 1: return
    while n%3 == 0:
        yield 3
        n //= 3
    if n == 1: return
    while n%5 == 0:
        yield 5
        n //= 5
    if n == 1: return

    if is_prime(n):
        yield n
        return
    
    nsq = math.isqrt(n)
    if nsq*nsq == n:
        for nsq_factor in factor(nsq):
            yield nsq_factor
            yield nsq_factor
        return
    
    start = 2
    while (d := pollard_rho_find_divisor(n, start)) == 0:
        start += 1
    
    yield from factor(d)
    yield from factor(n // d)

def factor(n:int):
    """
        Yields every prime factors of `n` (with duplicates), in no particular order.

        The emperically best algorithm is selected based on `n`.
    """

    if n < 2: return
    if n < 900_000: yield from factor_naive(n)
    else: yield from factor_pollard_rho(n)

    
