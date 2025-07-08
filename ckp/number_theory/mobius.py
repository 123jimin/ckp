from collections import Counter

def mobius_naive(n: int) -> int:
    """
        Computes the mobius value for `n`, by factoring `n` in-place.
    """
    if n < 2: return 1
    m = 1
    if not(n&1):
        n //= 2
        if not(n&1): return 0
        m = -m
    if not(n%3):
        n //= 3
        if not(n%3): return 0
        m = -m
    if not(n%5):
        n //= 5
        if not(n%5): return 0
        m = -m
    p, psq = 7, 49
    while psq <= n:
        if not(n%p):
            n //= p
            if not(n%p): return 0
            m = -m
        if not(n%(q := p+4)):
            n //= q
            if not(n%q): return 0
            m = -m
        psq += 12*p + 36
        p += 6
    if n > 1: m = -m
    return m

def mobius_from_factors(factors: Counter|list[int]):
    """
        Computes the mobius value for `n`, given its factors.
    """
    if isinstance(factors, Counter):
        if any(v > 1 for v in factors.values()): return 0
        return -1 if (len(factors)&1) else 1
    else:
        s = set(); a = s.add
        for f in factors:
            if f in s: return 0
            a(f)
        return -1 if (len(s)&1) else 1

class MobiusSieveData:
    """ An implementation of Mobius sieve. """
    __slots__ = ('mu', 'is_prime', 'odd_primes')

    mu: list[int]
    """ `mu[k]` contains the Mobius function value for `2k+1`. """

    is_prime: list[bool]
    odd_primes: list[int]

def mobius_sieve_init(max_n: int) -> MobiusSieveData:
    data = MobiusSieveData()
    L = (max_n+1) // 2

    mu = data.mu = [1] * L
    
    is_prime = data.is_prime = [True] * L
    is_prime[0] = False

    odd_primes = data.odd_primes = []

    for n in range(1, L):
        m = 2*n + 1
        if is_prime[n]: odd_primes.append(m); mu[n] = -1
        mu_n = mu[n]
        for p in odd_primes:
            if (x := m*p//2) >= L: break
            is_prime[x] = False
            if m%p: mu[x] = -mu_n
            else: mu[x] = 0; break

    return data

def mobius_sieve_query(sieve: MobiusSieveData, n: int) -> int:
    return (-sieve.mu[n//4] if m == 2 else sieve.mu[n//2]) if (m := n&3) else 0