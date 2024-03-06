"""
    Various functions related to modular arithmetic.
"""

from collections import Counter
from math import gcd
from .misc import factorial_prime_power
from .factor import factor

def solve_linear_mod(a:int, b:int, m:int) -> int:
    """ Returns the minimal x >= 0 such that `(ax + b) % m == 0`, or -1 if no such x exists. """
    if m == 1: return 0
    a %= m
    b = (-b) % m
    if a == 0: return 0 if b == 0 else -1
    if b == 0: return 0
    g = gcd(a, m)
    if g > 1:
        if b % g != 0: return -1
        a, b, m = a//g, b//g, m//g
    if a == 1: return b
    return (b * pow(a, -1, m)) % m

def count_zero_mod(a:int, b:int, m:int, l:int, r:int) -> int:
    """ Efficiently computes `sum((a*x + b)%m == 0 for x in range(l, r))`. Assumes that m > 0. """
    if l >= r: return 0
    if m == 1: return r - l
    a %= m
    b %= m
    g = gcd(a, m)
    if g > 1:
        if b % g != 0: return 0
        a, b, m = a//g, b//g, m//g
    x0 = solve_linear_mod(a, a*l + b, m)
    if x0 == -1: return 0
    x0 += l
    if x0 >= r: return 0
    return (r - 1 - x0) // m + 1

# TODO: implement it more efficiently.
def sum_floor_linear(a:int, b:int, m:int, n:int) -> int:
    """ Computes sum((a*x + b) // m for x in range(n)) """
    if n <= 0: return 0
    if m == 1: return b*n + a*(n*(n-1)//2)
    if m < 0: return sum_floor_linear(-a, -b, -m, n)

    if a == 0:
        return (b//m) * n

    if not 0 <= a < m:
        ad, ar = divmod(a, m)
        return sum_floor_linear(ad, 0, 1, n) + sum_floor_linear(ar, b, m, n)

    if not 0 <= b < m:
        bd, br = divmod(b, m)
        return n*bd + sum_floor_linear(a, br, m, n)

    h = (a*(n-1)+b) // m
    s = (n-1) * h - sum_floor_linear(m, m-b, a, h) + count_zero_mod(a, b, m, 1, n)

    return s

def _comb_mod_prime_small_k(n:int, k:int, p:int):
    """
        Given that p is a prime number, and k < min(n, p-1), returns nCk mod p.
        
        Time complexity: O(min(k, n-k, p))
    """
    n %= p
    if not 0 <= k <= n: return 0
    if k == 0 or k == n: return 1
    k = min(k, n-k)

    x, y = n, 1
    while k > 1:
        n -= 1
        x = (x*n) % p
        y = (y*k) % p
        k -= 1
    
    return (x * pow(y, -1, p)) % p

def _comb_mod_prime_large_k(n:int, k:int, p:int) -> int:
    """ Internal function for comb_mod_prime. """
    if k < p: return _comb_mod_prime_small_k(n, k, p)
    return (_comb_mod_prime_small_k(n%p, k%p, p) * _comb_mod_prime_large_k(n//p, k//p, p)) % p

def comb_mod_prime(n:int, k:int, p:int) -> int:
    """ Given that p is a prime number, returns nCk mod p. """
    if not 0 <= k <= n: return 0
    if k == 0 or k == n: return 1
    if factorial_prime_power(n, p) > factorial_prime_power(k, p) + factorial_prime_power(n-k, p): return 0
    m = 1
    while k >= p:
        n, nr = divmod(n, p)
        k, kr = divmod(k, p)
        m = (m * _comb_mod_prime_small_k(nr, kr, p)) % p
    return (m * _comb_mod_prime_small_k(n, k, p)) % p

def chinese_mod(*l) -> int:
    """ Given (a1, m1), (a2, m2), ..., where 0 <= ai < mi and every pairs of (mi, mj) for i != j are coprime, returns x < m1*m2*... such that x = ai mod mi for every i. """
    if len(l) == 1: return l[0][0]

    total_m = 1
    for (_, m) in l: total_m *= m
    
    x = 0
    for (a, m) in l:
        n = total_m // m
        x += a * n * pow(n, -1, m)

    return x % total_m

def legendre_symbol(a:int, p:int) -> int:
    """
        For a prime number p, returns the Legendre symbol (a/p).
        * When a mod p == 0, returns 0.
        * When a is a quadratic residue of p, returns 1. Otherwise, returns -1.
    """
    if a%p == 0: return 0
    if p == 2: return 1
    return (-1, 1)[pow(a, p//2, p) == 1]

def any_non_quadratic_residue_mod_prime(p:int) -> int:
    """ Given a prime number p >= 3, returns an arbitrary non quadratic residue. """
    
    if p%8 == 3 or p%8 == 5: return 2
    if p%12 == 5 or p%12 == 7: return 3
    if p%5 == 2 or p%5 == 3: return 5
    
    for a in range(7, p-2):
        if pow(a, (p-1)//2, p) == p-1:
            return a
    
    raise AssertionError(f"Failed to get a non quadratic residue for {p}.")

def sqrt_mod_prime(n:int, p:int) -> int:
    """
        For a prime number p, either returns x such that x^2 = n mod p, or returns 0 if there's no such x.
        
        This function implements the Tonelli-Shanks algorithm.
    """

    if p == 2: return n % 2
    if legendre_symbol(n, p) != 1: return 0

    q = p-1
    s = 0

    while q%2 == 0:
        q //= 2
        s += 1

    z = any_non_quadratic_residue_mod_prime(p)
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q+1)//2, p)

    while t >= 2:
        ti = pow(t, 2, p)
        i = 1
        while ti != 1:
            ti = pow(ti, 2, p)
            i += 1
        b = c
        for _ in range(m-i-1):
            b = pow(b, 2, p)
        m = i
        c = pow(b, 2, p)
        t = (t*c) % p
        r = (r*b) % p
    
    return 0 if t == 0 else r

def sqrt_mod_prime_power(n:int, p:int, k:int) -> int:
    """
        For a prime number p, either returns x such that x^2 = n mod p^k, or returns 0 if there's no such x.
    """
    if k == 1: return sqrt_mod_prime(n, p)
    if n%p == 0:
        if k > 2 and n%(p*p) == 0: return p * sqrt_mod_prime_power(n//(p*p), p, k-2)
        else: return 0

    pk2 = p ** (k-2)
    pk1 = pk2 * p
    pk = pk1 * p
    n %= pk

    if p == 2:
        if n%8 != 1: return 0
        if k == 2 or k == 3: return 1

        x = sqrt_mod_prime_power(n, p, k-1)
        xsq = (x*x) % pk

        if xsq == n: return x
        else: return x + pk2

    x = sqrt_mod_prime(n, p)
    if x == 0: return 0

    return (pow(x, pk1, pk) * pow(n, (pk - 2*pk1 + 1)//2, pk)) % pk

def sqrt_mod(n:int, m:int, m_factors:Counter|list[int]|None = None) -> int:
    """
        Given an integer m >= 2, either returns x such that x^2 = n mod m, or returns 0 if there's no such x.
        
        When `n_factors` is given, it would be regarded as the factorization of `m`.
        In this case, the provided m can either be the original value or 0.
    """

    if m_factors is None: m_factors = factor(m)
    if not isinstance(m_factors, Counter): m_factors = Counter(m_factors)
    
    crt_mods = []

    for (p, k) in m_factors.items():
        v = sqrt_mod_prime_power(n, p, k)
        pk = p**k
        if v == 0 and n % pk != 0:
            return 0
        crt_mods.append((v, pk))

    return chinese_mod(*crt_mods)