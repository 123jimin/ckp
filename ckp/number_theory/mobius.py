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
