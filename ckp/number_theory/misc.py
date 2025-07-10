def iterate_idiv(x: int):
    """
        Yields tuples of ([x/i], i_begin, i_end), in a decreasing order for [x/i].

        In other words, values `(q, a, b)` represent that `x//i == q` holds for all `i` precisely in `range(a, b)`. 

        Note that using this function is about 25% slower than using `q = x//a; b = x//q+1; a = b`.

        Time complexity: O(sqrt(x))
    """
    yield(x, 1, 2)

    if x <= 3:
        if x == 2: yield (1, 2, 3)
        elif x == 3: yield (1, 2, 4)
        return
    
    prev_q = x//2
    
    for i in range(3, x+1):
        if (q := x//i) == prev_q: break
        yield (prev_q, i-1, i)
        prev_q = q
    
    i -= 1
    
    for q in range(prev_q, 1, -1):
        next_i = x//q + 1
        yield (q, i, next_i)
        i = next_i
    
    yield(1, i, x+1)

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
    """ Given that p is a prime number, returns max i >= 0 such that p^i divides n!. """
    k = 0
    while n > 0:
        n //= p
        k += n
    return k

def comb_prime_power(n:int, k:int, p:int) -> int:
    """ Given that p is a prime number, returns max i >= 0 such that p^i divides nCk. """
    return factorial_prime_power(n, p) - factorial_prime_power(k, p) - factorial_prime_power(n-k, p)