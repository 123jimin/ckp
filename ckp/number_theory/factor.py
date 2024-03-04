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

    p, psq = 7, 49

    while psq <= n:
        if n%p == 0:
            yield p
            n //= p
            while n%p == 0:
                yield p
                n //= p
            if n < psq:
                if 1 < n: yield n
                return
        p += 4
        while n%p == 0:
            yield p
            n //= p
        p += 2
        psq += 12*(p - 3)
    if 1 < n: yield n

def pollard_rho_find_divisor(n:int, start:int = 2):
    """ Using a proper divisor of `n` , using Pollard's rho algorithm. """
    if 1 < (d := math.gcd(n, start)) < n: return d

    x = start

    # Doing `(y*y + 1) % n` is 10% faster than using `pow(y, 2, n)`.
    x1 = (x*x + 1) % n
    if (d := math.gcd((x2 := (x1*x1 + 1) % n) - x1, n)) != 1: return 0 if d == n else d

    x3 = (x2*x2 + 1) % n
    if (d := math.gcd((x4 := (x3*x3 + 1) % n) - x2, n)) != 1: return 0 if d == n else d

    x5 = (x4*x4 + 1) % n
    if (d := math.gcd((x6 := (x5*x5 + 1) % n) - x3, n)) != 1: return 0 if d == n else d
    
    x7 = (x6*x6 + 1) % n
    if (d := math.gcd((x8 := (x7*x7 + 1) % n) - x4, n)) != 1: return 0 if d == n else d

    # Memory usage incurred by storing past trajectory isn't a big deal in practice.
    # Also, pre-allocating `l` doesn't seem to affect overall performance.
    i, i4, l = 0, 4, [x5, x6, x7, x8]
    while True:
        p0, p1, p2, p3 = l[i:i4]
        x1 = (x8*x8 + 1) % n
        if (d := math.gcd((x2 := (x1*x1 + 1) % n) - p0, n)) != 1: return 0 if d == n else d

        x3 = (x2*x2 + 1) % n
        if (d := math.gcd((x4 := (x3*x3 + 1) % n) - p1, n)) != 1: return 0 if d == n else d

        x5 = (x4*x4 + 1) % n
        if (d := math.gcd((x6 := (x5*x5 + 1) % n) - p2, n)) != 1: return 0 if d == n else d
        
        x7 = (x6*x6 + 1) % n
        if (d := math.gcd((x8 := (x7*x7 + 1) % n) - p3, n)) != 1: return 0 if d == n else d

        l.extend((x1, x2, x3, x4, x5, x6, x7, x8))
        i, i4 = i4, i4 + 4

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
    if n < 1500: yield from factor_naive(n)
    else: yield from factor_pollard_rho(n)