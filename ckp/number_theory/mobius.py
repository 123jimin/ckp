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
        if n%p == 0:
            n //= p
            if n%p == 0: return 0
            m = -m
        if n%(q := p+4) == 0:
            n //= q
            if n%q == 0: return 0
            m = -m
        psq += 12*p + 36
        p += 6
    if n > 1: m = -m
    return m
