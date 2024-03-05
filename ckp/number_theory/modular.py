"""
    Various functions related to modular arithmetic.
"""

from .misc import factorial_prime_power

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
