"""
    Various functions related to modular arithmetic.
"""

from math import gcd
from .misc import factorial_prime_power

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

def sum_floor_linear(a:int, b:int, m:int, n:int) -> int:
    """ Computes sum((a*x + b) // m for x in range(n)) """
    if n <= 0: return 0
    if m == 1: return b*n + a*(n*(n-1)//2)
    if m < 0: a, b, m = -a, -b, -m

    add = 0
    while True:
        if not 0 <= a < m:
            d, a = divmod(a, m)
            add += d*(n*(n-1)//2)

        if a == 0:
            return add + (b//m) * n

        if not 0 <= b < m:
            d, b = divmod(b, m)
            add += n*d

        if (v := a*n + b) <= m:
            return add

        n, b = divmod(v, m)
        m, a = a, m

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

def jacobi_symbol(a: int, n: int) -> int:
    """ Returns the Jacobi symbol (a/n) for an odd integer `n`. """
    assert(n > 0 and n%2 == 1)

    if a == 1 or n == 1: return 1
    
    a %= n
    if not a: return 0
    if a == 1: return 1

    if gcd(a, n) != 1: return 0

    j = 1
    while a:
        n8 = n%8
        if n8 == 3 or n8 == 5:
            while not (a%2): a //= 2; j = -j
        else:
            while not (a%2): a //= 2
        a, n = n, a
        if a%4 == n%4 == 3: j = -j
        a %= n
    return j

def any_non_quadratic_residue_mod_prime(p:int) -> int:
    """ Given a prime number p >= 3, returns an arbitrary non quadratic residue. """
    
    if p%8 == 3 or p%8 == 5: return 2
    if p%12 == 5 or p%12 == 7: return 3
    if p%5 == 2 or p%5 == 3: return 5
    
    for a in range(7, p-2):
        if pow(a, (p-1)//2, p) == p-1:
            return a
    
    raise AssertionError(f"Failed to get a non quadratic residue for {p}.")

class ZMod:
    """
        Class for dealing Z/mZ. 

        Using this class, at the expense of performance (4x slower than simply using `%`), may simplify codes involving modular arithmetic and circular objects.

        Still, as the performance hit is severe, other functions involving modular arithmetic does *not* support this class.
    """

    __slots__ = ('x', 'm')
    x: int; m: int

    def __init__(self, x, m): self.x, self.m = x % m, m

    def __repr__(self): return f"ZMod({self.x}, {self.m})"
    def __str__(self): return f"{self.x} (mod {self.m})"

    def __bool__(self): return self.x != 0
    def __index__(self): return self.x

    def __eq__(self, other):
        if isinstance(other, ZMod) and self.m == other.m: return self.x == other.x
        elif isinstance(other, int): return self.x == other % self.m
        else: return NotImplemented
        
    def __ne__(self, other):
        if isinstance(other, ZMod) and self.m == other.m: return self.x != other.x
        elif isinstance(other, int): return self.x != other % self.m
        else: return NotImplemented

    def __add__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m: return ZMod(self.x + other.x, m)
        elif isinstance(other, int): return ZMod(self.x + other, m)
        else: return NotImplemented

    def __iadd__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m:
            self.x = (self.x + other.x) % m
            return self
        if isinstance(other, int):
            self.x = (self.x + other) % m
            return self
        return NotImplemented
    
    def __radd__(self, other):
        m = self.m
        if isinstance(other, int): return ZMod(self.x + other, m)
        else: return NotImplemented

    def __sub__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m: return ZMod(self.x - other.x, m)
        elif isinstance(other, int): return ZMod(self.x - other, m)
        else: return NotImplemented

    def __isub__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m:
            self.x = (self.x - other.x) % m
            return self
        if isinstance(other, int):
            self.x = (self.x - other) % m
            return self
        return NotImplemented
    
    def __neg__(self): return ZMod(self.m - self.x if self.x else 0, self.m)

    def __rsub__(self, other):
        m = self.m
        if isinstance(other, int): return ZMod(other - self.x, m)
        else: return NotImplemented

    def __mul__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m: return ZMod(self.x * other.x, m)
        elif isinstance(other, int): return ZMod(self.x * other, m)
        else: return NotImplemented

    def __imul__(self, other):
        m = self.m
        if isinstance(other, ZMod) and m == other.m:
            self.x = (self.x * other.x) % m
            return self
        if isinstance(other, int):
            self.x = (self.x * other) % m
            return self
        return NotImplemented
    
    def __rmul__(self, other):
        m = self.m
        if isinstance(other, int): return ZMod(other * self.x, m)
        else: return NotImplemented

    def __pow__(self, other):
        m = self.m
        if isinstance(other, int): return ZMod(pow(self.x, other, m), m)
        return NotImplemented
    
    def __ipow__(self, other):
        m = self.m
        if isinstance(other, int):
            self.x = pow(self.x, other, m)
            return self
        return NotImplemented