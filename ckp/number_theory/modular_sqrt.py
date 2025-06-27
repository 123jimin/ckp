from collections import Counter
from .modular import chinese_mod, legendre_symbol, any_non_quadratic_residue_mod_prime
from .factor import factor

def sqrt_mod_prime(n:int, p:int) -> int:
    """
        For a prime number p, either returns x such that x^2 = n mod p, or returns 0 if there's no such x.
        
        This function implements the Tonelli-Shanks algorithm.
    """

    if p == 2: return n & 1
    if legendre_symbol(n, p) != 1: return 0

    q = p-1
    s = 0

    while not(q&1):
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
    
    return r if t else 0

def sqrt_mod_prime_power(n:int, p:int, k:int) -> int:
    """
        For a prime number p, either returns x such that x^2 = n mod p^k, or returns 0 if there's no such x.
    """
    if k == 1: return sqrt_mod_prime(n, p)
    if not(n%p):
        psq = p*p
        if k > 2 and not(n%psq): return p * sqrt_mod_prime_power(n//psq, p, k-2)
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

    if not(x := sqrt_mod_prime(n, p)): return 0

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
        if (not v) and (n%pk):
            return 0
        crt_mods.append((v, pk))

    return chinese_mod(*crt_mods)