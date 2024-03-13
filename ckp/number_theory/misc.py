def iterate_idiv(x):
    """
        Yields tuples of ([x/i], i_begin, i_end), in a decreasing order for [x/i].

        In other words, when this function yields `(a, b, c)`, then `x//i == a` holds for all `i` precisely in `range(b, c)`. 

        Time complexity: O(sqrt(x))
    """
    prev_val = x
    prev_i = 1
    if x == 2:
        yield (2, 1, 2)
        yield (1, 2, 3)
        return
    for i in range(2, x+1):
        curr_val = x // i
        if curr_val == prev_val:
            prev_i = i-1
            break
        yield (prev_val, i-1, i)
        prev_val = curr_val
    for k in range(prev_val, 0, -1):
        ub = x//k
        yield (k, prev_i, ub+1)
        prev_i = ub+1

def extended_gcd(x:int, y:int) -> tuple[int, int, int]:
    """ Returns `(g, a, b)` such that `g == math.gcd(x, y)`, and `x*a + y*b = g`."""
    if not y: return (x, 1, 0)
    ps, s, pr, r = 1, 0, x, y
    while r:
        m, d = divmod(pr, r)
        pr, r = r, d
        ps, s = s, ps - m*s
    
    return (pr, ps, (pr - ps*x)//y)

def factorial_prime_power(n:int, p:int) -> int:
    """ Given that p is a prime number, returns max i >= 0 such that p^i divides n. """
    k = 0
    while n > 0:
        n //= p
        k += n
    return k

def comb_prime_power(n:int, k:int, p:int) -> int:
    """ Given that p is a prime number, returns max i >= 0 such that p^i divides nCk. """
    return factorial_prime_power(n, p) - factorial_prime_power(k, p) - factorial_prime_power(n-k, p)